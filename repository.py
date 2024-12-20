import os
import json
import hashlib
import shutil
import pickle
from typing import Dict, List, Optional
from utils import load_ignore_patterns, should_ignore

class Repository:
    """
    Core class that handles all version control operations.
    Implements a Git-like structure with:
    - Object storage for content-addressable files
    - Staging area for pending changes
    - Branch management with refs/heads structure
    - Commit history as a linked list of commits
    """
    def __init__(self, path: str):
        """Initialize a new repository or load an existing one."""
        self.path = os.path.abspath(path)
        self.repo_dir = os.path.join(path, '.giclone')
        
        if not os.path.exists(self.repo_dir):
            print(f"Creating directory: {self.repo_dir}")
            os.makedirs(self.repo_dir)
            
            print("Creating objects directory")
            os.makedirs(os.path.join(self.repo_dir, 'objects'))
            
            print("Creating refs directory")
            os.makedirs(os.path.join(self.repo_dir, 'refs'))
            
            print("Creating heads directory")
            os.makedirs(os.path.join(self.repo_dir, 'refs', 'heads'))  # Ensure heads directory exists
            
            print("Creating branches directory")
            os.makedirs(os.path.join(self.repo_dir, 'branches'))
            
            print("Creating initial HEAD")
            with open(os.path.join(self.repo_dir, 'HEAD'), 'w') as f:
                f.write('refs/heads/main')
            
            print("Creating initial branch file")
            with open(os.path.join(self.repo_dir, 'refs', 'heads', 'main'), 'w') as f:
                f.write('')  # Create an empty file for the main branch
            
            # Create .gitignore
            with open(os.path.join(self.repo_dir, 'ignore'), 'w') as f:
                f.write('.giclone\n')
        
        # Load ignore patterns
        self.ignore_patterns = load_ignore_patterns(self.repo_dir)
    def add(self, paths: List[str]):
        """
        Stage files for commit.
        Implementation strategy:
        1. Use content-addressable storage with SHA-256 hashing
        2. Store actual file content in objects directory
        3. Maintain staging area as a dictionary of path -> hash mappings
        4. Handle ignored files based on .giclone/ignore patterns
        """
        staging_area = os.path.join(self.repo_dir, 'index')
        staged_files = {}
        
        # Load existing staged files if index exists
        if os.path.exists(staging_area):
            with open(staging_area, 'rb') as f:
                staged_files = pickle.load(f)
        
        for path in paths:
            full_path = os.path.join(self.path, path)
            
            # Skip ignored files
            if should_ignore(full_path, self.path, self.ignore_patterns):
                print(f"Ignoring {path}")
                continue
            
            # Compute file hash
            with open(full_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Store file object
            object_path = os.path.join(self.repo_dir, 'objects', file_hash)
            shutil.copy2(full_path, object_path)
            
            # Update staging area
            staged_files[path] = file_hash
        
        # Save staging area
        with open(staging_area, 'wb') as f:
            pickle.dump(staged_files, f)
    
    def commit(self, message: str):
        """
        Create a commit with staged files.
        Design decisions:
        1. Commits are immutable snapshots of staged files
        2. Each commit stores:
           - Complete file list (not just changes)
           - Parent commit hash (for history tracking)
           - Commit message
        3. Branch refs are updated to point to new commit
        """
        staging_area = os.path.join(self.repo_dir, 'index')
        
        if not os.path.exists(staging_area):
            print("No changes to commit.")
            return
        
        # Load staged files
        with open(staging_area, 'rb') as f:
            staged_files = pickle.load(f)
        
        # Create commit object
        commit = {
            'message': message,
            'files': staged_files,
            'parent': self.get_head_commit()
        }
        
        # Hash and save commit
        commit_hash = hashlib.sha256(json.dumps(commit).encode()).hexdigest()
        commit_path = os.path.join(self.repo_dir, 'objects', commit_hash)
        
        with open(commit_path, 'w') as f:
            json.dump(commit, f)
        
        # Update HEAD to point to this commit
        head_path = os.path.join(self.repo_dir, 'HEAD')
        with open(head_path, 'r') as f:
            current_branch = f.read().strip()
        
        branch_path = os.path.join(self.repo_dir, current_branch)
        with open(branch_path, 'w') as f:
            f.write(commit_hash)
        
        # Clear staging area
        os.remove(staging_area)
        print(f"Committed {len(staged_files)} files with message: {message}")
    
    def log(self):
        """Show commit history."""
        current_commit_hash = self.get_head_commit()
        
        while current_commit_hash:
            commit_path = os.path.join(self.repo_dir, 'objects', current_commit_hash)
            
            with open(commit_path, 'r') as f:
                commit = json.load(f)
            
            print(f"Commit: {current_commit_hash}")
            print(f"Message: {commit['message']}")
            print("Files:", ", ".join(commit['files'].keys()))
            print()
            
            current_commit_hash = commit.get('parent')
    
    def branch(self, name: str):
        """Create a new branch at the current HEAD."""
        branch_path = os.path.join(self.repo_dir, 'refs', 'heads', name)
        
        # Use current HEAD commit for new branch
        current_commit = self.get_head_commit()
        
        with open(branch_path, 'w') as f:
            f.write(current_commit)
    
    def checkout(self, branch_or_commit: str):
        """Checkout a branch or commit."""
        # Check if it's a branch
        branch_path = os.path.join(self.repo_dir, 'refs', 'heads', branch_or_commit)
        
        if os.path.exists(branch_path):
            with open(branch_path, 'r') as f:
                commit_hash = f.read().strip()
            
            # Update HEAD
            head_path = os.path.join(self.repo_dir, 'HEAD')
            with open(head_path, 'w') as f:
                f.write(f'refs/heads/{branch_or_commit}')
        else:
            # Assume it's a commit hash
            commit_hash = branch_or_commit
        
        # Restore files from the commit
        commit_path = os.path.join(self.repo_dir, 'objects', commit_hash)
        
        with open(commit_path, 'r') as f:
            commit = json.load(f)
        
        # Restore files from the commit
        for path, file_hash in commit['files'].items():
            src = os.path.join(self.repo_dir, 'objects', file_hash)
            dest = os.path.join(self.path, path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            
            shutil.copy2(src, dest)
    
    def diff(self, branch1: str, branch2: str):
        """Show differences between two branches."""
        # Get commit hashes for branches
        branch1_commit = self._get_branch_commit(branch1)
        branch2_commit = self._get_branch_commit(branch2)
        
        # Load commits
        commit1_path = os.path.join(self.repo_dir, 'objects', branch1_commit)
        commit2_path = os.path.join(self.repo_dir, 'objects', branch2_commit)
        
        with open(commit1_path, 'r') as f:
            commit1 = json.load(f)
        
        with open(commit2_path, 'r') as f:
            commit2 = json.load(f)
        
        # Compare files
        files1 = set(commit1['files'].keys())
        files2 = set(commit2['files'].keys())
        
        added = files2 - files1
        removed = files1 - files2
        
        print(f"Diff between {branch1} and {branch2}:")
        print("Added files:", ", ".join(added))
        print("Removed files:", ", ".join(removed))
        
        # Check for conflicting changes
        common_files = files1 & files2
        conflicting_files = [
            f for f in common_files 
            if commit1['files'][f] != commit2['files'][f]
        ]
        
        if conflicting_files:
            print("Conflicting files:", ", ".join(conflicting_files))
    
    def clone(self, destination: str):
        """Clone the repository to a new location."""
        shutil.copytree(self.path, destination)
    
    def get_head_commit(self) -> Optional[str]:
        """Get the current HEAD commit."""
        head_path = os.path.join(self.repo_dir, 'HEAD')
        
        if not os.path.exists(head_path):
            return None
        
        with open(head_path, 'r') as f:
            current_branch = f.read().strip()
        
        branch_path = os.path.join(self.repo_dir, current_branch)
        
        if not os.path.exists(branch_path):
            return None
        
        with open(branch_path, 'r') as f:
            return f.read().strip()
    
    def _get_branch_commit(self, branch: str) -> str:
        """Get commit hash for a given branch."""
        branch_path = os.path.join(self.repo_dir, 'refs', 'heads', branch)
        
        with open(branch_path, 'r') as f:
            return f.read().strip()
    
    def merge(self, branch_name: str):
        """
        Merge another branch into the current branch.
        Merge strategy:
        1. Compare file hashes between branches
        2. Auto-merge when no conflicts exist
        3. Detect conflicts when same file has different hashes
        4. Create merge commit after successful merge
        Note: Does not handle conflict resolution - user must resolve manually
        """
        # Get commit hashes
        current_commit = self.get_head_commit()
        branch_commit = self._get_branch_commit(branch_name)
        
        # Load both commits
        with open(os.path.join(self.repo_dir, 'objects', current_commit), 'r') as f:
            current_files = json.load(f)['files']
        
        with open(os.path.join(self.repo_dir, 'objects', branch_commit), 'r') as f:
            branch_files = json.load(f)['files']
        
        # Combine files
        merged_files = current_files.copy()
        
        # Check for conflicts
        conflicts = []
        for file_path, file_hash in branch_files.items():
            if file_path in merged_files and merged_files[file_path] != file_hash:
                conflicts.append(file_path)
            else:
                merged_files[file_path] = file_hash
        
        if conflicts:
            print(f"Merge conflicts in files: {', '.join(conflicts)}")
            return False
        
        # Create staging area with merged files
        staging_area = os.path.join(self.repo_dir, 'index')
        with open(staging_area, 'wb') as f:
            pickle.dump(merged_files, f)
        
        # Create merge commit
        self.commit(f"Merge branch '{branch_name}'")
        return True
