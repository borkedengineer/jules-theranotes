"""
Validation utilities for audio files
"""

import mimetypes
from typing import List
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

class AudioValidator:
    def __init__(self):
        """Initialize audio validator with supported formats"""
        self.supported_audio_types = {
            # MIME types
            "audio/mpeg",  # MP3
            "audio/mp4",   # MP4/M4A
            "audio/wav",   # WAV
            "audio/wave",  # WAV alternative
            "audio/x-wav", # WAV alternative
            "audio/webm",  # WebM
            "audio/ogg",   # OGG
            "audio/x-m4a", # M4A
            "audio/mp3",   # MP3 alternative
        }
        
        self.supported_extensions = {
            ".mp3", ".mp4", ".m4a", ".wav", ".webm", ".ogg", ".flac", ".aac"
        }
    
    def is_valid_audio_file(self, upload_file: UploadFile) -> bool:
        """
        Validate if uploaded file is a supported audio format
        
        Args:
            upload_file: FastAPI UploadFile object
            
        Returns:
            True if file is a valid audio format
        """
        try:
            # Check filename
            if not upload_file.filename:
                logger.warning("No filename provided")
                return False
            
            # Check file extension
            filename_lower = upload_file.filename.lower()
            has_valid_extension = any(
                filename_lower.endswith(ext) for ext in self.supported_extensions
            )
            
            if not has_valid_extension:
                logger.warning(f"Unsupported file extension: {upload_file.filename}")
                return False
            
            # Check MIME type if available
            if upload_file.content_type:
                content_type_lower = upload_file.content_type.lower()
                if content_type_lower not in self.supported_audio_types:
                    # Try to guess MIME type from extension
                    guessed_type, _ = mimetypes.guess_type(upload_file.filename)
                    if guessed_type and guessed_type.lower() not in self.supported_audio_types:
                        logger.warning(f"Unsupported MIME type: {upload_file.content_type}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating audio file: {str(e)}")
            return False
    
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported audio formats
        
        Returns:
            List of supported file extensions
        """
        return list(self.supported_extensions)
    
    def get_supported_mime_types(self) -> List[str]:
        """
        Get list of supported MIME types
        
        Returns:
            List of supported MIME types
        """
        return list(self.supported_audio_types)
    
    def validate_file_size(self, file_size: int, max_size_mb: int = 25) -> bool:
        """
        Validate file size
        
        Args:
            file_size: File size in bytes
            max_size_mb: Maximum allowed size in MB
            
        Returns:
            True if file size is within limits
        """
        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
