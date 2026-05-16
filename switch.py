from sccs_layout_check import check_sccs, directory_path, path
import sys

check_sccs()

branch_to_switch = sys.argv[2] if len(sys.argv) > 2 else None

if not branch_to_switch:
    print("No branch specified. Please provide a branch name to switch to.")
    sys.exit(1)

