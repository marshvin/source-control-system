#!/usr/bin/env python3
import sys
import argparse
from repository import Repository

def main():
    """
    Command-line interface for the version control system.
    Implements a Git-like command structure using argparse.
    Each command maps to a corresponding Repository class method.

    Design Pattern:
    1. Command parsing with subparsers for different operations
    2. Repository instance maintains state
    3. Commands follow Git-like syntax for familiarity
    """
    parser = argparse.ArgumentParser(description='Git-like version control system')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # init command
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('path', nargs='?', default='.', help='Repository path')

    # add command
    add_parser = subparsers.add_parser('add', help='Add files to staging area')
    add_parser.add_argument('files', nargs='+', help='Files to add')

    # commit command
    commit_parser = subparsers.add_parser('commit', help='Commit staged changes')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')

    # branch command
    branch_parser = subparsers.add_parser('branch', help='Create a new branch')
    branch_parser.add_argument('name', help='Branch name')

    # checkout command
    checkout_parser = subparsers.add_parser('checkout', help='Checkout a branch')
    checkout_parser.add_argument('branch', help='Branch name')

    # log command
    subparsers.add_parser('log', help='Show commit history')

    args = parser.parse_args()
    
    if args.command == 'init':
        repo = Repository(args.path)
        print(f"Initialized empty repository in {args.path}")
    else:
        # Use the project directory instead of current directory
        repo = Repository(r'C:\Users\vince\Documents\my_project')
        if args.command == 'add':
            repo.add(args.files)
        elif args.command == 'commit':
            repo.commit(args.message)
        elif args.command == 'branch':
            repo.branch(args.name)
        elif args.command == 'checkout':
            repo.checkout(args.branch)
        elif args.command == 'log':
            repo.log()

if __name__ == '__main__':
    main()