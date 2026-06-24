import os
from pathlib import Path
from typing import List

class FileManager:
    """Handles file operations and directory management for usptoXsearch."""
    def __init__(self, base_dir: str = "output"):
        self.base_dir = Path(base_dir)

    def ensure_directory(self, sub_dir: str) -> Path:
        """Ensures that the specified subdirectory exists within the base directory."""
        target_path = self.base_dir / sub_dir.lower().replace(" ", "_")
        target_path.mkdir(parents=True, exist_ok=True)
        return target_path

    def get_source_directory(self, source_name: str) -> Path:
        """Returns the path to the directory for a given source name."""
        return self.ensure_directory(source_name)

    def save_file(self, data: bytes, filename: str, sub_dir: str) -> Path:
        """Saves binary data to a file in the specified subdirectory."""
        target_dir = self.get_source_directory(sub_dir)
        file_path = target_dir / filename
        
        with open(file_path, "wb") as f:
            f.write(data)
        
        return file_path

    def save_text_file(self, content: str, filename: str, sub_dir: str) -> Path:
        """Saves text data to a file in the specified subdirectory."""
        target_dir = self.get_source_directory(sub_dir)
        file_path = target_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return file_path

    def list_files(self, sub_dir: str) -> List[Path]:
        """Lists all files in the specified subdirectory."""
        target_dir = self.get_source_directory(sub_dir)
        if not target_dir.exists():
            return []
        return [f for f in target_dir.iterdir() if f.is_file()]
