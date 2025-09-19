"""
File handling utilities for audio uploads
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional
import logging
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize file handler
        
        Args:
            temp_dir: Directory for temporary files (defaults to system temp)
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self._ensure_temp_dir()
    
    def _ensure_temp_dir(self):
        """Ensure the temporary directory exists"""
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)
    
    async def save_uploaded_file(self, upload_file: UploadFile) -> str:
        """
        Save uploaded file to temporary location
        
        Args:
            upload_file: FastAPI UploadFile object
            
        Returns:
            Path to the saved temporary file
        """
        try:
            # Create temporary file with proper extension
            file_extension = self._get_file_extension(upload_file.filename)
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension,
                dir=self.temp_dir
            )
            
            # Write uploaded content to temporary file
            content = await upload_file.read()
            temp_file.write(content)
            temp_file.close()
            
            logger.info(f"Saved uploaded file to: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {str(e)}")
            raise RuntimeError(f"Could not save uploaded file: {str(e)}")
    
    def _get_file_extension(self, filename: str) -> str:
        """
        Get file extension from filename
        
        Args:
            filename: Original filename
            
        Returns:
            File extension with dot (e.g., '.mp3')
        """
        if not filename:
            return ".tmp"
        
        # Get extension
        extension = Path(filename).suffix.lower()
        
        # If no extension, try to determine from content type
        if not extension:
            extension = ".tmp"
        
        return extension
    
    def cleanup_file(self, file_path: str):
        """
        Clean up temporary file
        
        Args:
            file_path: Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in bytes
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Failed to get file size for {file_path}: {str(e)}")
            return 0
    
    def is_valid_audio_file(self, file_path: str) -> bool:
        """
        Check if file is a valid audio file
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file exists and is readable
        """
        try:
            return os.path.exists(file_path) and os.access(file_path, os.R_OK)
        except Exception:
            return False
