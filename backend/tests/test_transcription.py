"""
Tests for the transcription API
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Jules Theranotes API"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_transcribe_invalid_file():
    """Test transcription with invalid file type"""
    # Create a fake text file
    files = {"audio_file": ("test.txt", b"Hello world", "text/plain")}
    response = client.post("/api/transcribe", files=files)
    assert response.status_code == 400
    assert "Invalid audio file" in response.json()["detail"]

def test_transcribe_no_file():
    """Test transcription without file"""
    response = client.post("/api/transcribe")
    assert response.status_code == 422  # Validation error

def test_api_docs():
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
