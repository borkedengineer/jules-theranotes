# Jules Theranotes

A local-first webapp for therapists to streamline session note-taking with AI-powered transcription and structured data extraction.

## Architecture

This project follows a microservices architecture with clear separation of concerns:

- **Frontend**: Next.js React application for audio recording and UI
- **Backend**: FastAPI Python microservice for speech-to-text transcription
- **Communication**: RESTful API between frontend and backend

## Features

- 🎤 **Audio Recording**: High-quality audio recording using MediaRecorder API
- ⏱️ **Real-time Timer**: Visual feedback during recording with timer display
- 🎵 **Playback Controls**: Review recordings with play/pause functionality
- 📁 **File Management**: Download recordings as MP3/MP4 audio files
- 🔄 **AI Processing**: Speech-to-text transcription using OpenAI Whisper
- 📄 **Document Generation**: Create Word/PDF documents from structured data
- 🎨 **Modern UI**: Built with ShadCN components and Tailwind CSS
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔒 **Privacy-First**: Local processing with minimal cloud exposure

## Tech Stack

### Frontend

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS + ShadCN UI components
- **Audio**: MediaRecorder API for high-quality audio recording
- **Icons**: Lucide React

### Backend

- **Framework**: FastAPI with Uvicorn
- **Speech-to-Text**: OpenAI Whisper
- **Audio Processing**: librosa, soundfile, pydub
- **File Handling**: Python multipart uploads
- **Validation**: Pydantic models

## Getting Started

### Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.11+** (for backend)
- **npm or yarn** (for frontend)
- **pip** (for backend)

### Quick Start

1. **Clone the repository**:

```bash
git clone <repository-url>
cd jules-theranotes
```

2. **Choose your setup method**:

#### Option A: Docker (Recommended)

```bash
# Start with Docker Compose
docker-compose up --build

# Access the application at: http://localhost:3000
# Backend API at: http://localhost:8000
```

#### Option B: Local Development

```bash
# Install dependencies
cd frontend && npm install

# Start development server
cd frontend && npm run dev

# Access the application at: http://localhost:3000
# Backend API at: http://localhost:8000
```

### Individual Service Development

#### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

#### Backend Only

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation at: http://localhost:8000/docs
```

## Project Structure

```
jules-theranotes/
├── frontend/                 # Next.js React application
│   ├── app/                 # Next.js app directory
│   ├── components/          # React components
│   ├── lib/                 # Utility functions
│   ├── package.json         # Frontend dependencies
│   ├── next.config.js       # Next.js configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   ├── tsconfig.json        # TypeScript configuration
│   └── Dockerfile          # Frontend container
├── backend/                 # FastAPI Python microservice
│   ├── app/                 # Application modules
│   ├── models/              # ML model files
│   ├── services/            # Core services
│   ├── utils/               # Utility functions
│   ├── tests/               # Test files
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── docker-compose.yml       # Multi-service orchestration
└── README.md               # This file
```

## Development Commands

### Docker Commands

```bash
# Start the application
docker-compose up --build

# Start in background
docker-compose up -d --build

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild without cache
docker-compose build --no-cache
```

### Local Development Commands

```bash
# Install dependencies
cd frontend && npm install

# Start development server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Run tests
cd frontend && npm test

# Run linting
cd frontend && npm run lint
```

## Usage

1. **Start Recording**: Click the "Start Recording" button to begin capturing audio
2. **Monitor Progress**: Watch the timer and recording indicator during capture
3. **Stop Recording**: Click "Stop Recording" when finished
4. **Review Audio**: Use the playback controls to listen to your recording
5. **Download**: Save the recording as an MP3 file to your device
6. **Transcribe**: Upload the audio to the backend for speech-to-text processing

## Audio Format

- **Format**: MP3/MP4 (AAC codec) - optimized for backend processing
- **Quality**: High-quality compressed audio for efficient storage and transmission
- **File Size**: Compressed format reduces file size while maintaining quality

## Browser Compatibility

- Chrome/Chromium 47+
- Firefox 25+
- Safari 14.1+
- Edge 79+

## Security & Privacy

- All audio processing happens locally in the browser
- No audio data is sent to external servers without explicit user action
- Recordings are stored temporarily in browser memory only
- Full local-first approach for maximum privacy

## Development

### Project Structure

```
jules-theranotes/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # ShadCN UI components
│   └── audio-recorder.tsx # Main audio recording component
├── lib/                  # Utility functions
│   └── utils.ts          # Tailwind class utilities
└── public/               # Static assets
```

### Key Components

- **AudioRecorder**: Main component handling recording, playback, and file management
- **Button**: Reusable button component with multiple variants
- **Card**: Container components for organized layouts
- **Progress**: Progress bar for upload feedback

## API Endpoints

### Backend API (http://localhost:8000)

- `POST /api/transcribe` - Transcribe audio file to text
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### Example Usage

```bash
# Transcribe an audio file
curl -X POST "http://localhost:8000/api/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@recording.mp3"
```

## Next Steps

- [x] Backend API for speech-to-text transcription
- [ ] Frontend integration with backend API
- [ ] NLP processing for structured data extraction
- [ ] Session notes template system
- [ ] Document generation (Word/PDF)
- [ ] Email and Google Drive integration
- [ ] Local storage with encryption
- [ ] User authentication and session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
