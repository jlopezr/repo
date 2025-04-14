#!/usr/bin/env python3
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

        statuses = set(line[:2].strip() for line in output.splitlines() if not line.startswith('##'))
        branch_status = output.splitlines()[0]

        # print("=====================================")
        # print(output)
        # print("=====================================")

        # print("BRANCH STATUS:")
        # print(branch_status)
        # print("STATUSES:")
        # # print set as a list
        # print(list(statuses))        
        # print("=====================================")

        status = ""
        if len(statuses) == 0:
            status = "Clean"
        else:
            result = []

            if '??' in statuses:
                result.append("Untracked Files")

            if 'UU' in statuses:
                result.append("Unmerged Files")
            
            # if statuses has one of M,A,D,R,C then append "Modified Files"
            if any(status in {'M', 'A', 'D', 'R', 'C'} for status in statuses):
                result.append("Modified Files")
        
            # Return all the elements of the separated by " | "
            status =  " | ".join(result)

        if 'ahead' in branch_status and 'behind' in branch_status:
            return status + " || Diverged"
        elif 'ahead' in branch_status:
            return status + " || Ahead"
        elif 'behind' in branch_status:
            return status + " || Behind"
        else:
            return status
        
        # Clean || Ahead => Yellow
        # Clean || Behind => Yellow
        # Clean || Diverged => Red
        
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