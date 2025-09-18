# Jules Theranotes Backend

FastAPI Python microservice for AI-powered therapy session note-taking.

## Features

- 🎤 **Speech-to-Text**: Audio transcription using OpenAI Whisper
- 🧠 **NLP Processing**: Extract structured data from transcripts
- 📄 **Document Generation**: Create Word/PDF documents from structured data
- 🔒 **Security**: Local-first processing with encryption support

## Tech Stack

- **Framework**: FastAPI with Uvicorn
- **Speech-to-Text**: OpenAI Whisper
- **NLP**: spaCy, HuggingFace Transformers
- **Document Processing**: python-docx, ReportLab
- **Audio Processing**: librosa, soundfile

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

## API Endpoints

- `POST /api/transcribe` - Transcribe audio file to text
- `POST /api/extract-data` - Extract structured data from transcript
- `POST /api/generate-document` - Generate Word/PDF document

## Development

This backend will be developed as a separate microservice with its own:

- Dependencies and requirements
- API endpoints
- ML/NLP processing logic
- Document generation capabilities

## License

This project is licensed under the MIT License.
