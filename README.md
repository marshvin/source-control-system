# Source Control System

A Git-like distributed version control system implemented in Python. This system provides basic version control functionality including file staging, committing, branching, and merging.

## Features

- Repository initialization with `.giclone` structure
- File staging and committing
- Branch creation and management
- Commit history viewing
- Branch diffing and merging
- Basic conflict detection
- File ignoring patterns
- Local repository cloning

## Highlights of the Version Control System

### Unique Features

- **Simplified Ignore Pattern Matching**: 
  - The system implements a straightforward method for ignoring files and directories using a `.giclone/ignore` file. This allows users to easily specify which files should not be tracked, similar to `.gitignore` in Git, enhancing user experience by reducing clutter in version control.


- **Content-Addressable Storage**: 
  - Files are stored as content-addressable objects using SHA-256 hashing. This ensures data integrity and allows for efficient storage and retrieval of file contents, as files are uniquely identified by their content rather than their names.

- **Modular Architecture**: 
  - The system is structured into distinct components (e.g., `main.py`, `repository.py`, `utils.py`), promoting maintainability and scalability. Each module has a clear responsibility, making it easier to extend functionality in the future.

- **User-Friendly CLI**: 
  - The command-line interface is designed to be intuitive, with straightforward commands similar to the Git commands for initializing repositories, staging files, committing changes, and managing branches. This lowers the barrier to entry for users unfamiliar with version control systems.


## Installation

1. Clone the repository:
```bash
git clone https://github.com/marshvin/source-control-system.git
cd source-control-system
```


## Usage

### Initialize a Repository
```bash
python main.py init /path/to/project
```

### Stage Files
```bash
python main.py add file1.txt file2.py
```

### Commit Changes
```bash
python main.py commit -m "Your commit message"
```

### Create a Branch
```bash
python main.py branch feature-branch
```

### Switch Branches
```bash
python main.py checkout feature-branch
```

### View Commit History
```bash
python main.py log
```

## Project Structure
- `source-control-system/`
  - `main.py`: CLI interface
  - `repository.py`: Core repository functionality
  - `utils.py`: Utility functions

## Implementation Details

### Repository Structure
The system creates a `.giclone` directory with the following structure:

- `giclone/`
  - `objects/`: Stores file contents and commits
  - `refs/`
    - `heads/`: Branch references
  - `branches/`: Branch information
  - `HEAD`: Points to current branch
  - `ignore`: Ignore patterns file

## Function Explanations

### Utility Functions

- **`load_ignore_patterns(repo_dir: str) -> List[str]`**
  - Loads ignore patterns from the `.giclone/ignore` file. This function reads the file, strips whitespace, and ignores comments (lines starting with `#`). It returns a list of patterns that specify which files or directories should be ignored by the version control system.

- **`should_ignore(path: str, repo_path: str, ignore_patterns: List[str]) -> bool`**
  - Checks if a given file path should be ignored based on the loaded ignore patterns. It compares the relative path of the file to the patterns and returns `True` if the file matches any of the ignore rules, otherwise returns `False`.

### Repository Class Methods

- **`add(paths: List[str])`**
  - Stages files for commit. It checks each file against the ignore patterns and skips any that should be ignored. For files that are not ignored, it computes a SHA-256 hash of the file content, stores the file in the objects directory, and updates the staging area.

- **`commit(message: str)`**
  - Creates a commit with the currently staged files. It generates a commit object that includes the commit message, the list of staged files, and the parent commit hash. The commit is then saved in the objects directory, and the HEAD reference is updated to point to the new commit.

- **`log()`**
  - Displays the commit history. It traverses the linked list of commits starting from the current HEAD and prints out the commit hash, message, and files associated with each commit.

- **`branch(name: str)`**
  - Creates a new branch at the current HEAD. It saves the current commit hash to a new file in the `refs/heads` directory corresponding to the new branch name.

- **`checkout(branch_or_commit: str)`**
  - Checks out a specified branch or commit. If a branch name is provided, it updates the HEAD to point to that branch. If a commit hash is provided, it restores the files from that commit to the working directory.

- **`merge(branch_name: str)`**
  - Merges another branch into the current branch. It compares the file hashes between the two branches, detects conflicts, and creates a merge commit if there are no conflicts. If conflicts exist, it lists the conflicting files and does not complete the merge.

### Key Components

1. **Object Storage**: Files are stored as content-addressable objects using SHA-256 hashing
2. **Staging Area**: Tracks files ready for commit
3. **Branch Management**: Supports multiple branches with conflict detection
4. **Commit History**: Maintains a linked history of commits

## Limitations

- No network functionality (local-only)
- Basic conflict detection without resolution
- No interactive rebase functionality
- Simple ignore pattern matching

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

