import ast
import sys
import os
import argparse

__version__ = "0.1.0"

from print_statement_hook.constants import COLOR_YELLOW, COLOR_RESET, COLOR_BOLD, COLOR_RED, COLOR_GREEN


def check_file_for_prints(file_path):
    """
    Check a single Python file for print statements using AST.
    Returns a list of (lineno, col_offset) if found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"{COLOR_YELLOW}Warning: Error parsing {file_path}: {e}{COLOR_RESET}")
        return []

    locations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'print':
                locations.append((node.lineno, node.col_offset))

    return locations


def is_excluded(path, exclude_list):
    """
    Check if a path or any of its parents are in the exclude list.
    """
    if not exclude_list:
        return False

    abs_path = os.path.abspath(path)
    for exclude in exclude_list:
        abs_exclude = os.path.abspath(exclude)
        if abs_path == abs_exclude or abs_path.startswith(abs_exclude + os.sep):
            return True
    return False


def get_all_python_files(directory, exclude_list):
    """
    Recursively find all .py files in a directory, skipping excluded ones.
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Filter directories in-place to prevent os.walk from entering them
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclude_list)]

        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                if not is_excluded(full_path, exclude_list):
                    python_files.append(full_path)
    return python_files


def check_print_statements():
    """
    Entry point for the console script and hook.
    """
    parser = argparse.ArgumentParser(description="Check Python files for forbidden print statements.")
    parser.add_argument('filenames', nargs='*', help='Files to check. If empty, checks entire directory.')
    parser.add_argument('--exclude', action='append', help='Files or directories to exclude from check.')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    files_to_check = []
    exclude_list = args.exclude or []

    if not args.filenames:
        # Check current directory recursively
        files_to_check = get_all_python_files('.', exclude_list)
    else:
        for item in args.filenames:
            if os.path.isdir(item):
                files_to_check.extend(get_all_python_files(item, exclude_list))
            elif os.path.isfile(item) and item.endswith('.py'):
                if not is_excluded(item, exclude_list):
                    files_to_check.append(item)

    total_findings = 0
    files_with_prints = 0

    for file_path in files_to_check:
        findings = check_file_for_prints(file_path)
        if findings:
            files_with_prints += 1
            total_findings += len(findings)
            for lineno, col in findings:
                # Format: file:line:col: Issue
                print(
                    f"{COLOR_RED}FAIL{COLOR_RESET} {file_path}:{lineno}: {COLOR_BOLD}print(){COLOR_RESET} statement found.")

    if total_findings > 0:
        print(
            f"\n{COLOR_RED}{COLOR_BOLD}FAILED{COLOR_RESET}: Found {total_findings} print statements across {files_with_prints} files.")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    check_print_statements()
