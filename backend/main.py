"""
Jules Theranotes Backend Orchestrator
Main FastAPI application that routes requests to specialized services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import httpx
from typing import Dict, Any

from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Jules Theranotes API",
    description="AI-powered therapy session note-taking backend",
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

# Service URLs
TRANSCRIBER_URL = "http://localhost:8000"
NOTARY_URL = "http://localhost:8001"

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Jules Theranotes API",
        "version": "0.1.0",
        "services": {
            "transcriber": f"{TRANSCRIBER_URL}/docs",
            "notary": f"{NOTARY_URL}/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "jules-theranotes-orchestrator"}

@app.post("/api/transcribe")
async def transcribe_audio(audio_file):
    """Proxy transcription requests to transcriber service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TRANSCRIBER_URL}/api/transcribe",
                files={"audio_file": audio_file}
            )
            return response.json()
    except Exception as e:
        logger.error(f"Transcription proxy error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/api/extract-session-data")
async def extract_session_data(request: Dict[str, Any]):
    """Proxy session data extraction to notary service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{NOTARY_URL}/api/extract-session-data",
                json=request
            )
            return response.json()
    except Exception as e:
        logger.error(f"Session data extraction proxy error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Session data extraction failed: {str(e)}")

@app.post("/api/process-session")
async def process_session(audio_file):
    """
    Complete session processing: transcribe audio and extract session data
    """
    try:
        # Step 1: Transcribe audio
        async with httpx.AsyncClient() as client:
            transcribe_response = await client.post(
                f"{TRANSCRIBER_URL}/api/transcribe",
                files={"audio_file": audio_file}
            )
            
            if transcribe_response.status_code != 200:
                raise HTTPException(
                    status_code=transcribe_response.status_code,
                    detail="Transcription failed"
                )
            
            transcript_data = transcribe_response.json()
            transcript = transcript_data.get("transcript", "")
            
            if not transcript:
                raise HTTPException(
                    status_code=400,
                    detail="No transcript generated from audio"
                )
            
            # Step 2: Extract session data
            extract_response = await client.post(
                f"{NOTARY_URL}/api/extract-session-data",
                json={"transcript": transcript}
            )
            
            if extract_response.status_code != 200:
                raise HTTPException(
                    status_code=extract_response.status_code,
                    detail="Session data extraction failed"
                )
            
            session_data = extract_response.json()
            
            # Combine results
            return JSONResponse(
                status_code=200,
                content={
                    "transcript": transcript_data,
                    "session_data": session_data
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Session processing failed: {str(e)}")

@app.post("/api/generate-therapy-note")
async def generate_therapy_note(audio_file):
    """
    Complete end-to-end processing: Audio → Transcript → Therapy Note
    
    This is the main endpoint for the complete workflow:
    1. Transcribe audio file
    2. Extract structured session data
    3. Format into therapy session note
    
    Args:
        audio_file: Audio file upload
        
    Returns:
        Complete therapy session note ready for use
    """
    try:
        async with httpx.AsyncClient() as client:
            # Step 1: Transcribe audio
            logger.info("Starting audio transcription...")
            transcribe_response = await client.post(
                f"{TRANSCRIBER_URL}/api/transcribe",
                files={"audio_file": audio_file}
            )
            
            if transcribe_response.status_code != 200:
                raise HTTPException(
                    status_code=transcribe_response.status_code,
                    detail="Transcription failed"
                )
            
            transcript_data = transcribe_response.json()
            transcript = transcript_data.get("transcript", "")
            
            if not transcript:
                raise HTTPException(
                    status_code=400,
                    detail="No transcript generated from audio"
                )
            
            logger.info(f"Transcription completed. Transcript length: {len(transcript)} characters")
            
            # Step 2: Generate therapy note
            logger.info("Generating therapy note...")
            note_response = await client.post(
                f"{NOTARY_URL}/api/format-therapy-note",
                json={"transcript": transcript}
            )
            
            if note_response.status_code != 200:
                raise HTTPException(
                    status_code=note_response.status_code,
                    detail="Therapy note generation failed"
                )
            
            note_data = note_response.json()
            
            logger.info("Therapy note generation completed successfully")
            
            # Return complete results
            return JSONResponse(
                status_code=200,
                content={
                    "therapy_note": note_data.get("therapy_note", ""),
                    "transcript": transcript_data,
                    "session_data": note_data.get("session_data", {}),
                    "processing_summary": {
                        "audio_duration": transcript_data.get("duration", 0),
                        "transcript_length": len(transcript),
                        "language": transcript_data.get("language", "unknown"),
                        "confidence": transcript_data.get("confidence", 0)
                    }
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Therapy note generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Therapy note generation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
