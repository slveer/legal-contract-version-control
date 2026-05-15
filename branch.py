import sys

from sccs_layout_check import check_sccs

check_sccs()

subcommand = sys.argv[2] if len(sys.argv) > 2 else None

branch_name = sys.argv[3] if len(sys.argv) > 3 else None

if not subcommand:
    print("No subcommand provided. Please use 'create', 'delete', or 'list' along with required arguments.")
    sys.exit(1)

if subcommand not in ["create", "delete", "list"]:
    print(f"Unknown subcommand: {subcommand}")
    print("Invalid subcommand. Please use 'create', 'delete', or 'list' along with required arguments.")
    sys.exit(1)

if subcommand in ["create", "delete"]:
    if not branch_name:
        print("No branch name provided. Please specify a branch name.")
        sys.exit(1)