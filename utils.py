import os
from typing import List

"""
Utility functions for the version control system.
Focuses on file pattern matching and ignore rules.
Implements a simplified version of .gitignore pattern matching.
"""

def load_ignore_patterns(repo_dir: str) -> List[str]:
    """Load .gitignore patterns."""
    ignore_file = os.path.join(repo_dir, 'ignore')
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def should_ignore(path: str, repo_path: str, ignore_patterns: List[str]) -> bool:
    """Check if a file should be ignored."""
    relative_path = os.path.relpath(path, repo_path)
    return any(
        pattern in relative_path or 
        relative_path.startswith(pattern) or 
        relative_path.endswith(pattern)
        for pattern in ignore_patterns
    ) 