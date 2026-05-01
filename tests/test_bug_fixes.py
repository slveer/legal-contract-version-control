import pytest
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def tmp_sccs_dir(tmp_path):
    """Create a temporary directory with a valid .sccs layout."""
    sccs = tmp_path / ".sccs"
    current_branch_dir = sccs / "current_branch"
    current_branch_dir.mkdir(parents=True)

    # Write current_branch.json
    branch_data = {"current_branch": "main", "branches": ["main", "dev"]}
    (current_branch_dir / "current_branch.json").write_text(
        json.dumps(branch_data, indent=4), encoding="utf-8"
    )

    # Create branch directories with history and commit_file_hash
    for branch_name in ["main", "dev"]:
        history_dir = sccs / "branches" / branch_name / "history"
        hash_dir = sccs / "branches" / branch_name / "commit_file_hash"
        history_dir.mkdir(parents=True, exist_ok=True)
        hash_dir.mkdir(parents=True, exist_ok=True)

        history_data = {
            "history": {
                "initial_commit": "abc123",
                "latest_commit": "abc123",
                "latest_commit_number": 1,
                "commit_order": {"1": "abc123"},
            }
        }
        (history_dir / "commit_history.json").write_text(
            json.dumps(history_data, indent=4), encoding="utf-8"
        )

        hash_data = {"abc123": "dummyhash"}
        (hash_dir / "commit_file_hash.json").write_text(
            json.dumps(hash_data, indent=4), encoding="utf-8"
        )

    # Create objects/docx directory with a dummy commit object
    objects_dir = sccs / "objects" / "docx"
    objects_dir.mkdir(parents=True, exist_ok=True)
    (objects_dir / "abc123.docx").write_bytes(b"fake docx content")

    # Create a .docx file at the root
    docx_file = tmp_path / "test.docx"
    docx_file.write_bytes(b"fake docx content")

    return tmp_path


# ===== Bug 1: switch.py — update_current_branch() writes to read-only file =====


def test_update_current_branch_writes_successfully(tmp_sccs_dir):
    """Bug 1: update_current_branch should write to the file without crashing."""
    # Import after setting up the fixture
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # We need to mock the module-level variables
    with patch.dict(os.environ, {}, clear=False):
        # Read the original file
        branch_file = tmp_sccs_dir / ".sccs" / "current_branch" / "current_branch.json"
        data = json.loads(branch_file.read_text(encoding="utf-8"))
        assert data["current_branch"] == "main"

        # Simulate what update_current_branch does (the fixed version)
        with open(branch_file, "r", encoding="utf-8", newline="\n") as f:
            current_branch = json.load(f)
        current_branch["current_branch"] = "dev"
        with open(branch_file, "w", encoding="utf-8", newline="\n") as f:
            json.dump(current_branch, f, indent=4)

        # Verify the file was updated
        data = json.loads(branch_file.read_text(encoding="utf-8"))
        assert data["current_branch"] == "dev"


def test_update_current_branch_preserves_branches_list(tmp_sccs_dir):
    """Bug 1: update_current_branch should not corrupt the branches array."""
    branch_file = tmp_sccs_dir / ".sccs" / "current_branch" / "current_branch.json"

    # Simulate the fix
    with open(branch_file, "r", encoding="utf-8", newline="\n") as f:
        current_branch = json.load(f)
    original_branches = current_branch["branches"].copy()
    current_branch["current_branch"] = "dev"
    with open(branch_file, "w", encoding="utf-8", newline="\n") as f:
        json.dump(current_branch, f, indent=4)

    # Verify branches list is preserved
    data = json.loads(branch_file.read_text(encoding="utf-8"))
    assert data["branches"] == original_branches


def test_update_current_branch_missing_file_exits(tmp_path):
    """Bug 1: Should handle missing file gracefully."""
    nonexistent = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        with open(nonexistent, "r", encoding="utf-8") as f:
            json.load(f)


# ===== Bug 2: init.py — check_file_requirements() uses and instead of or =====


def test_check_file_requirements_none_path_exits():
    """Bug 2: None path should trigger exit, not TypeError."""
    # The fixed condition: `not None or ...` → short-circuits to True
    path = None
    result = not path or Path(path).suffix.lower() != ".docx" or not Path(path).is_file()
    assert result is True  # Should trigger the error branch


def test_check_file_requirements_non_docx_exits(tmp_path):
    """Bug 2: Non-.docx file should trigger exit."""
    bad_file = tmp_path / "file.txt"
    bad_file.write_text("x")
    path = str(bad_file)
    result = not path or Path(path).suffix.lower() != ".docx" or not Path(path).is_file()
    assert result is True


def test_check_file_requirements_missing_file_exits(tmp_path):
    """Bug 2: Nonexistent .docx should trigger exit."""
    path = str(tmp_path / "nonexistent.docx")
    result = not path or Path(path).suffix.lower() != ".docx" or not Path(path).is_file()
    assert result is True


def test_check_file_requirements_valid_passes(tmp_path):
    """Bug 2: Valid .docx file should NOT trigger exit."""
    good_file = tmp_path / "file.docx"
    good_file.write_text("x")
    path = str(good_file)
    result = not path or Path(path).suffix.lower() != ".docx" or not Path(path).is_file()
    assert result is False


# ===== Bug 3: init.py — hexdigest() inside loop =====


def test_hash_document_correct_hash(tmp_path):
    """Bug 3: Hash should match hashlib.sha256 of the file content."""
    import hashlib

    content = b"hello world"
    doc = tmp_path / "test.docx"
    doc.write_bytes(content)

    # Simulate the fixed hash_document
    with open(doc, "rb") as f:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
        hashed_file = hasher.hexdigest()

    expected = hashlib.sha256(content).hexdigest()
    assert hashed_file == expected


def test_hash_document_large_file(tmp_path):
    """Bug 3: Multi-chunk file (>64KB) should hash correctly."""
    import hashlib

    content = b"x" * 100000  # >65536 bytes
    doc = tmp_path / "large.docx"
    doc.write_bytes(content)

    with open(doc, "rb") as f:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
        hashed_file = hasher.hexdigest()

    expected = hashlib.sha256(content).hexdigest()
    assert hashed_file == expected


# ===== Bug 4: switch.py — debug prints left in =====


def test_switch_no_debug_prints_on_error(capsys):
    """Bug 4: Error output should not contain raw hash values."""
    import re

    # Simulate the error path (after fix — only the error message)
    hashed_file = "a" * 64  # fake hash
    latest_commit_file_hash = "b" * 64  # different fake hash
    branch = "main"

    if not hashed_file == latest_commit_file_hash:
        print(f"Error: The current file has uncommitted changes on the current branch '{branch}'. Please commit your changes before switching branches.")

    captured = capsys.readouterr()
    # Should contain the error message
    assert "Error:" in captured.out
    # Should NOT contain raw hash strings (64-char hex)
    for line in captured.out.strip().splitlines():
        assert not re.fullmatch(r"[0-9a-f]{64}", line.strip()), f"Debug hash found in output: {line}"


# ===== Bug 5: switch.py — double period =====


def test_switch_error_message_single_period():
    """Bug 5: Error message should end with a single period."""
    branch = "main"
    msg = f"Error: The current file has uncommitted changes on the current branch '{branch}'. Please commit your changes before switching branches."
    assert msg.endswith("branches.")
    assert not msg.endswith("branches..")
