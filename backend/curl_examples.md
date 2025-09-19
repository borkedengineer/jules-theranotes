# API Testing Examples

## Complete End-to-End Flow

### Generate Therapy Note from Audio File

```bash
# Complete workflow: Audio → Transcript → Therapy Note
curl -X POST "http://localhost:8002/api/generate-therapy-note" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@your_audio_file.mp3"
```

**Response:**

```json
{
  "therapy_note": "THERAPY SESSION NOTE\n\nClient: Sarah Johnson\nDate: March 15th, 2024\n...",
  "transcript": {
    "transcript": "Today I met with Sarah Johnson...",
    "language": "en",
    "confidence": 0.95,
    "duration": 30.5
  },
  "session_data": {
    "goal": "work on her depression management",
    "content": "We discussed her recent struggles...",
    "assessment": "PHQ-9 scale, and she scored 15",
    "diagnoses": ["major depressive disorder", "generalized anxiety disorder"],
    "intervention_response": "cognitive behavioral therapy techniques",
    "plan": "continue working on behavioral activation techniques"
  },
  "processing_summary": {
    "audio_duration": 30.5,
    "transcript_length": 1250,
    "language": "en",
    "confidence": 0.95
  }
}
```

## Individual Service Testing

### 1. Transcribe Audio Only

```bash
curl -X POST "http://localhost:8000/api/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@your_audio_file.mp3"
```

### 2. Extract Session Data from Transcript

```bash
curl -X POST "http://localhost:8001/api/extract-session-data" \
     -H "Content-Type: application/json" \
     -d '{"transcript": "Today I met with Sarah Johnson for our weekly session..."}'
```

### 3. Generate Therapy Note from Transcript

```bash
curl -X POST "http://localhost:8001/api/format-therapy-note" \
     -H "Content-Type: application/json" \
     -d '{"transcript": "Today I met with Sarah Johnson for our weekly session..."}'
```

## Health Checks

```bash
# Check all services
curl http://localhost:8000/health  # Transcriber
curl http://localhost:8001/health  # Notary
curl http://localhost:8002/health  # Main API
```

## API Documentation

```bash
# Access interactive API docs
open http://localhost:8000/docs  # Transcriber docs
open http://localhost:8001/docs  # Notary docs
open http://localhost:8002/docs  # Main API docs
```
