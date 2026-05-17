#!/usr/bin/env python3
import exceptions
import utils
from pathlib import Path
import json
import sys


def get_entered_origin() -> str | None:
    """Retrieve the origin entered by the user."""
    return sys.argv[2] if len(sys.argv) > 2 else None


def resolve_entered_origin(origin: str = get_entered_origin()) -> str:
    """
    Resolve the entered origin by adding 'https://' if missing and appending '/clone' 
    if missing."""
    if origin is None:
        print("No origin entered.")
        raise exceptions.InvalidArgumentError("No origin entered.")
    else:
        origin = origin

    if not origin.startswith("http://") and not origin.startswith("https://"):
        origin = "http://" + origin
        
    
    strs = ["/clone", "/clone/", "/publish", "/publish/"]

    for str in strs:
        if origin.endswith(str):
            origin = origin[:-len(str)]

    return origin


def main() -> None:
    """Run functions for the <sccs clone> command."""

    utils.write_key_to_config("api_url", resolve_entered_origin())


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
