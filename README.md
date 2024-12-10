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

