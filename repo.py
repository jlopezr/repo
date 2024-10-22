import os
import argparse
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def find_git_repos(starting_dir):
    git_repos = []
    for root, dirs, files in os.walk(starting_dir):
        if '.git' in dirs:
            git_repos.append(root)
    return git_repos

def scan(args):
    starting_dir = args.directory
    git_repos = find_git_repos(starting_dir)

    if git_repos:
        print("Found git repositories in the following directories:")
        for repo in git_repos:
            print(repo)
    else:
        print("No git repositories found.")

def get_repo_status(repo):
    try:
        result = subprocess.run(['git', '-C', repo, 'status', '--porcelain', '--branch'], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            return "Clean"

        statuses = set(line[:2].strip() for line in output.splitlines())
        branch_status = output.splitlines()[0]

        if any(status in {'??'} for status in statuses):
            return "Untracked Files"
        if any(status in {'M', 'A', 'D', 'R', 'C', 'U'} for status in statuses):
            return "Modified Files"
        if any(status in {'M', 'A', 'D', 'R', 'C'} for status in statuses):
            return "Staged Changes"
        if 'U' in statuses:
            return "Unmerged Paths"

        if 'ahead' in branch_status and 'behind' in branch_status:
            return "Diverged"
        if 'ahead' in branch_status:
            return "Ahead of Remote"
        if 'behind' in branch_status:
            return "Behind Remote"

        return "Unknown status"
    except subprocess.CalledProcessError as e:
        return f"Error getting status: {e}"

def status(args):
    starting_dir = args.directory
    git_repos = find_git_repos(starting_dir)

    if git_repos:
        for repo in git_repos:
            repo_status = get_repo_status(repo)
            color = Fore.GREEN if repo_status == "Clean" else Fore.RED
            print(f"Repository: {repo:<50} - Status: {color}{repo_status}{Style.RESET_ALL}")
    else:
        print("No git repositories found.")

def main():
    parser = argparse.ArgumentParser(description="Tool to scan directories for git repositories.")
    subparsers = parser.add_subparsers(dest='command')

    scan_parser = subparsers.add_parser('scan', help="Scan directories for git repositories.")
    scan_parser.add_argument('directory', nargs='?', default='.', help="The starting directory to scan.")
    scan_parser.set_defaults(func=scan)

    status_parser = subparsers.add_parser('status', help="Print the git status of repositories.")
    status_parser.add_argument('directory', nargs='?', default='.', help="The starting directory to scan.")
    status_parser.set_defaults(func=status)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()