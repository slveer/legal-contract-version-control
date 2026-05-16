"""Publish a SCCS repository to a hosted API"""

from pathlib import Path
import requests
import zipfile
import io
import os
import exceptions
import sys


def zip_cwd():
    """Zip the current working directory."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk("."):
            for file in files:
                zip_file.write(Path(root) / file)
    buffer.seek(0)
    return buffer


def post_repo(buffer):
    """Post the repository to the hosted API."""
    response = requests.post(
    "http://127.0.0.1:8000/publish",
    files={
        "file": (Path.cwd().name + ".zip",
        buffer, "application/zip")
        }
    )
    return response


def main():
    """Run functions for the <sccs publish> command."""
    
    response = post_repo(zip_cwd())

    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    try:
        main()

    except exceptions.SCCSException as e:
        print(f"An error occurred:\n{e}\n")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred:\n\n{type(e).__name__}: {e}\n")
        sys.exit(2)
else:
    raise exceptions.FileImportedAsModuleError(
        "This file cannot be run as a module. Please run it as a script."
    )