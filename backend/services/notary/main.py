"""
Therapy Session Notary Service
FastAPI service for extracting structured data from therapy session transcripts
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging
from typing import Dict, Any

from nlp_extractor import TherapySessionExtractor
from note_formatter import TherapyNoteFormatter
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Therapy Session Notary API",
    description="Extract structured data from therapy session transcripts",
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
nlp_extractor = TherapySessionExtractor()
note_formatter = TherapyNoteFormatter()

# Request/Response models
class TranscriptRequest(BaseModel):
    transcript: str

class SessionDataResponse(BaseModel):
    goal: str
    content: str
    assessment: str
    diagnoses: list
    intervention_response: str
    plan: str
    client_name: str
    session_date: str
    raw_transcript: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Therapy Session Notary API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "therapy-session-notary"}

@app.post("/api/extract-session-data", response_model=SessionDataResponse)
async def extract_session_data(request: TranscriptRequest):
    """
    Extract structured data from therapy session transcript
    
    Args:
        request: TranscriptRequest containing the transcript text
    
    Returns:
        SessionDataResponse with extracted session data
    """
    try:
        if not request.transcript or not request.transcript.strip():
            raise HTTPException(
                status_code=400,
                detail="Transcript cannot be empty"
            )
        
        logger.info(f"Processing transcript of length: {len(request.transcript)} characters")
        
        # Extract structured data
        session_data = nlp_extractor.extract_session_data(request.transcript)
        
        # Format the therapy note
        formatted_output = note_formatter.format_json_output(session_data)
        
        logger.info("Session data extraction and formatting completed successfully")
        
        return JSONResponse(
            status_code=200,
            content=formatted_output
        )
        
    except Exception as e:
        logger.error(f"Session data extraction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Session data extraction failed: {str(e)}"
        )

@app.post("/api/format-therapy-note")
async def format_therapy_note(request: TranscriptRequest):
    """
    Extract session data and return formatted therapy note
    
    Args:
        request: TranscriptRequest containing the transcript text
    
    Returns:
        Formatted therapy session note
    """
    try:
        if not request.transcript or not request.transcript.strip():
            raise HTTPException(
                status_code=400,
                detail="Transcript cannot be empty"
            )
        
        logger.info(f"Formatting therapy note from transcript of length: {len(request.transcript)} characters")
        
        # Extract structured data
        session_data = nlp_extractor.extract_session_data(request.transcript)
        
        # Format the therapy note
        formatted_note = note_formatter.format_therapy_note(session_data)
        
        logger.info("Therapy note formatting completed successfully")
        
        return JSONResponse(
            status_code=200,
            content={
                "therapy_note": formatted_note,
                "session_data": session_data
            }
        )
        
    except Exception as e:
        logger.error(f"Therapy note formatting failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Therapy note formatting failed: {str(e)}"
        )

@app.get("/api/supported-fields")
async def get_supported_fields():
    """Get information about supported extraction fields"""
    return {
        "supported_fields": [
            "goal",
            "content", 
            "assessment",
            "diagnoses",
            "intervention_response",
            "plan",
            "client_name",
            "session_date"
        ],
        "description": "Extracts structured data from therapy session transcripts"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
