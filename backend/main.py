"""
Jules Theranotes Backend API
FastAPI microservice for speech-to-text transcription using Whisper
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Optional
import os
from pathlib import Path

# Import our services
from services.transcription import TranscriptionService
from utils.file_handler import FileHandler
from utils.validators import AudioValidator
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Jules Theranotes API",
    description="AI-powered therapy session note-taking backend with speech-to-text",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
transcription_service = TranscriptionService(model_size=settings.WHISPER_MODEL_SIZE)
file_handler = FileHandler(temp_dir=settings.TEMP_DIR)
audio_validator = AudioValidator()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Jules Theranotes API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "jules-theranotes-backend"}

@app.post("/api/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Transcribe audio file to text using OpenAI Whisper model
    
    Args:
        audio_file: Audio file to transcribe (MP3, MP4, WAV, etc.)
    
    Returns:
        JSON response with transcript and metadata
    """
    try:
        # Validate file
        if not audio_validator.is_valid_audio_file(audio_file):
            raise HTTPException(
                status_code=400, 
                detail="Invalid audio file. Supported formats: MP3, MP4, WAV, M4A, WEBM, OGG"
            )
        
        # Check file size
        if audio_file.size and audio_file.size > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        logger.info(f"Processing audio file: {audio_file.filename}, size: {audio_file.size} bytes")
        
        # Save uploaded file temporarily
        temp_file_path = await file_handler.save_uploaded_file(audio_file)
        
        try:
            # Transcribe audio
            result = await transcription_service.transcribe_audio(temp_file_path)
            
            return JSONResponse(
                status_code=200,
                content={
                    "transcript": result["text"],
                    "language": result.get("language", "unknown"),
                    "confidence": result.get("confidence", 0.0),
                    "duration": result.get("duration", 0.0),
                    "filename": audio_file.filename,
                    "file_size": audio_file.size
                }
            )
            
        finally:
            # Clean up temporary file
            file_handler.cleanup_file(temp_file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
