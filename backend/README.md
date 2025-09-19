# Jules Theranotes Backend

Microservices architecture for AI-powered therapy session note-taking with speech-to-text transcription and NLP data extraction.

## Features

- 🎤 **Speech-to-Text**: Audio transcription using OpenAI Whisper
- 🧠 **NLP Processing**: Extract structured data from therapy session transcripts
- 📁 **File Upload**: Support for multiple audio formats (MP3, MP4, WAV, etc.)
- 🔒 **Error Handling**: Comprehensive validation and error handling
- 🚀 **FastAPI**: High-performance async API framework
- 🐳 **Docker Ready**: Containerized microservices deployment

## Architecture

The backend is organized into three microservices:

### **Transcriber Service** (Port 8000)

- **Speech-to-Text**: OpenAI Whisper
- **Audio Processing**: librosa, soundfile, pydub
- **File Handling**: Python multipart uploads

### **Notary Service** (Port 8001)

- **NLP Processing**: spaCy for named entity recognition
- **Text Analysis**: Regex patterns for therapy session data extraction
- **Structured Output**: JSON format for session notes

### **Main Orchestrator** (Port 8002)

- **API Gateway**: Routes requests to appropriate services
- **Service Coordination**: Combines transcription and NLP processing
- **Client Interface**: Single endpoint for complete session processing

## Tech Stack

- **Framework**: FastAPI with Uvicorn
- **Speech-to-Text**: OpenAI Whisper
- **NLP**: spaCy, HuggingFace Transformers
- **Audio Processing**: librosa, soundfile, pydub
- **File Handling**: Python multipart uploads
- **Validation**: Pydantic models

## API Endpoints

### Main Orchestrator (Port 8002)

- `POST /api/transcribe` - Transcribe audio file to text
- `POST /api/extract-session-data` - Extract structured data from transcript
- `POST /api/process-session` - Complete session processing (transcribe + extract)
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Transcriber Service (Port 8000)

- `POST /api/transcribe` - Transcribe audio file to text
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Notary Service (Port 8001)

- `POST /api/extract-session-data` - Extract structured data from transcript
- `GET /api/supported-fields` - Get supported extraction fields
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Request/Response Format

**POST /api/transcribe**

```bash
curl -X POST "http://localhost:8000/api/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@recording.mp3"
```

**Response:**

```json
{
  "transcript": "This is the transcribed text from the audio file.",
  "language": "en",
  "confidence": 0.95,
  "duration": 30.5,
  "filename": "recording.mp3",
  "file_size": 1024000
}
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. **Create virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Start development server**:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access API documentation**:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build backend

# Or build standalone
docker build -t jules-theranotes-backend .
docker run -p 8000:8000 jules-theranotes-backend
```

## Configuration

The backend can be configured using environment variables:

- `WHISPER_MODEL_SIZE`: Whisper model size (tiny, base, small, medium, large)
- `MAX_FILE_SIZE_MB`: Maximum file size in MB (default: 25)
- `DEBUG`: Enable debug mode (default: True)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

## Supported Audio Formats

- MP3 (.mp3)
- MP4/M4A (.mp4, .m4a)
- WAV (.wav)
- WebM (.webm)
- OGG (.ogg)
- FLAC (.flac)
- AAC (.aac)

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid file format or corrupted file
- **413 Payload Too Large**: File exceeds size limit
- **500 Internal Server Error**: Transcription processing error

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_transcription.py
```

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── services/           # Business logic
│   └── transcription.py # Whisper transcription service
├── utils/              # Utility functions
│   ├── file_handler.py  # File upload handling
│   └── validators.py    # Audio file validation
└── tests/              # Test files
    └── test_transcription.py
```

## License

This project is licensed under the MIT License.
