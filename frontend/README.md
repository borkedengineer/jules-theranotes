# Jules Theranotes Frontend

Next.js React application for therapy session note-taking with audio recording capabilities.

## Features

- 🎤 **Audio Recording**: High-quality audio recording using MediaRecorder API
- ⏱️ **Real-time Timer**: Visual feedback during recording
- 🎵 **Playback Controls**: Review recordings before processing
- 📁 **File Management**: Download recordings as MP3/MP4 audio files
- 🔄 **Backend Integration**: Upload audio for transcription processing
- 🎨 **Modern UI**: Built with ShadCN components and Tailwind CSS
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS + ShadCN UI components
- **Audio**: MediaRecorder API for high-quality audio recording
- **Icons**: Lucide React
- **State Management**: React hooks

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies**:

```bash
npm install
```

2. **Start development server**:

```bash
npm run dev
```

3. **Open in browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # ShadCN UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── progress.tsx
│   └── audio-recorder.tsx # Main audio recording component
├── lib/                  # Utility functions
│   └── utils.ts          # Tailwind class utilities
├── public/               # Static assets
├── package.json          # Dependencies and scripts
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── Dockerfile           # Container configuration
```

## Key Components

### AudioRecorder

Main component handling audio recording functionality:

- **Recording**: Uses MediaRecorder API for high-quality audio recording
- **Timer**: Real-time recording duration display
- **Playback**: Built-in audio player for review
- **Download**: Export recordings as MP3/MP4 audio files
- **Upload**: Integration with backend API

### UI Components

Built with ShadCN UI for consistent design:

- **Button**: Reusable button with multiple variants
- **Card**: Container components for organized layouts
- **Progress**: Progress bar for upload feedback

## Audio Recording

### Technical Implementation

- **MediaRecorder API**: Captures audio data in real-time
- **Audio Encoding**: MP4/AAC or WebM/Opus encoding for optimal compression
- **Quality**: 44.1kHz sample rate with echo cancellation and noise suppression
- **File Format**: MP3/MP4 audio files for backend processing compatibility

### Browser Compatibility

- Chrome/Chromium 47+
- Firefox 25+
- Safari 14.1+
- Edge 79+

## Backend Integration

The frontend communicates with the backend API for:

- **Audio Upload**: Send MP3/MP4 audio files for transcription
- **Progress Tracking**: Monitor upload and processing status
- **Error Handling**: Graceful error handling and user feedback

### API Endpoints

- `POST /api/transcribe` - Upload audio for transcription
- `POST /api/extract-data` - Process transcript for structured data
- `POST /api/generate-document` - Generate documents

## Development

### Code Style

- TypeScript for type safety
- ESLint for code quality
- Prettier for code formatting
- Tailwind CSS for styling

### Environment Variables

Create a `.env.local` file:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Development settings
NODE_ENV=development
```

## Docker

### Build and run with Docker Compose

```bash
# From project root
docker-compose up --build frontend
```

### Build standalone Docker image

```bash
docker build -t jules-theranotes-frontend .
docker run -p 3000:3000 jules-theranotes-frontend
```

## Security & Privacy

- **Local Processing**: Audio recording happens entirely in browser
- **No External Dependencies**: Pure browser APIs for recording
- **Temporary Storage**: Audio only stored in memory during session
- **Permission-Based**: Requires explicit microphone access

## Performance

- **Optimized Builds**: Next.js automatic optimizations
- **Code Splitting**: Automatic code splitting for faster loads
- **Image Optimization**: Built-in image optimization
- **Bundle Analysis**: Use `npm run build` to analyze bundle size

## Testing

```bash
# Run tests (when implemented)
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run linting and type checking
6. Submit a pull request

## License

This project is licensed under the MIT License.
