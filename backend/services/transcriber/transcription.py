"""
Transcription service using OpenAI Whisper
"""

import whisper
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any
import torch

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the transcription service with Whisper model
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise RuntimeError(f"Could not load Whisper model: {str(e)}")
    
    async def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription results
        """
        try:
            # Run transcription in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._transcribe_sync, 
                audio_file_path
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise RuntimeError(f"Transcription failed: {str(e)}")
    
    def _transcribe_sync(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Synchronous transcription method
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription results
        """
        try:
            # Check if file exists
            if not Path(audio_file_path).exists():
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            logger.info(f"Starting transcription of: {audio_file_path}")
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_file_path,
                verbose=False,
                language=None,  # Auto-detect language
                task="transcribe"
            )
            
            # Extract relevant information
            transcript_text = result["text"].strip()
            language = result.get("language", "unknown")
            
            # Calculate confidence (average of segment confidences if available)
            confidence = 0.0
            if "segments" in result and result["segments"]:
                confidences = [seg.get("avg_logprob", 0) for seg in result["segments"] if "avg_logprob" in seg]
                if confidences:
                    # Convert log probability to confidence (rough approximation)
                    confidence = max(0, min(1, (sum(confidences) / len(confidences) + 5) / 5))
            
            # Get audio duration
            duration = 0.0
            if "segments" in result and result["segments"]:
                last_segment = result["segments"][-1]
                duration = last_segment.get("end", 0.0)
            
            logger.info(f"Transcription completed. Language: {language}, Duration: {duration:.2f}s")
            
            return {
                "text": transcript_text,
                "language": language,
                "confidence": confidence,
                "duration": duration,
                "segments": result.get("segments", [])
            }
            
        except Exception as e:
            logger.error(f"Sync transcription failed: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_size": self.model_size,
            "model_loaded": self.model is not None,
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        }
