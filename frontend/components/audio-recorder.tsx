"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Mic,
  Square,
  Play,
  Pause,
  Download,
  ChevronDown,
  ChevronUp,
  RotateCcw,
  Loader2,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function AudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [transcriptError, setTranscriptError] = useState<string | null>(null);
  const [showTranscript, setShowTranscript] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number | null>(null);

  // Format time as HH:MM:SS.ssss
  const formatTime = (milliseconds: number) => {
    const totalSeconds = milliseconds / 1000;
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = Math.floor(totalSeconds % 60);
    const ms = Math.floor((milliseconds % 1000) / 10); // Show centiseconds

    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}.${ms
      .toString()
      .padStart(2, "0")}`;
  };

  // Get the best supported audio format for recording
  const getSupportedMimeType = (): string => {
    const types = [
      'audio/mp4; codecs="mp4a.40.2"', // MP4/AAC - closest to MP3
      "audio/webm; codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg; codecs=opus",
      "audio/ogg",
    ];

    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }
    return "audio/webm"; // fallback
  };

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
        },
      });

      streamRef.current = stream;

      // Get the best supported MIME type
      const mimeType = getSupportedMimeType();
      console.log("Using MIME type:", mimeType);

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: mimeType,
      });

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mimeType });
        setAudioBlob(blob);
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);

        // Clean up stream
        if (streamRef.current) {
          streamRef.current.getTracks().forEach((track) => track.stop());
        }
      };

      mediaRecorder.start(100); // Collect data every 100ms
      setIsRecording(true);
      setRecordingTime(0);
      startTimeRef.current = Date.now();

      // Start high-precision timer
      timerRef.current = setInterval(() => {
        if (startTimeRef.current) {
          const elapsed = Date.now() - startTimeRef.current;
          setRecordingTime(elapsed);
        }
      }, 10); // Update every 10ms for smooth display
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Unable to access microphone. Please check permissions.");
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);

      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  // Play/pause audio
  const togglePlayback = () => {
    if (!audioRef.current || !audioUrl) return;

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  // Handle audio playback events
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleEnded = () => setIsPlaying(false);
    const handlePause = () => setIsPlaying(false);
    const handlePlay = () => setIsPlaying(true);

    audio.addEventListener("ended", handleEnded);
    audio.addEventListener("pause", handlePause);
    audio.addEventListener("play", handlePlay);

    return () => {
      audio.removeEventListener("ended", handleEnded);
      audio.removeEventListener("pause", handlePause);
      audio.removeEventListener("play", handlePlay);
    };
  }, [audioUrl]);

  // Download audio file
  const downloadAudio = () => {
    if (!audioBlob || !audioUrl) return;

    const link = document.createElement("a");
    link.href = audioUrl;

    // Determine file extension based on MIME type
    const mimeType = audioBlob.type;
    let extension = "mp3"; // Default to mp3

    if (mimeType.includes("mp4")) {
      extension = "m4a"; // MP4 audio files
    } else if (mimeType.includes("webm")) {
      extension = "webm";
    } else if (mimeType.includes("ogg")) {
      extension = "ogg";
    } else if (mimeType.includes("wav")) {
      extension = "wav";
    }

    link.download = `recording-${new Date()
      .toISOString()
      .slice(0, 19)
      .replace(/:/g, "-")}.${extension}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Transcribe audio using backend API
  const transcribeAudio = async () => {
    if (!audioBlob) return;

    setIsTranscribing(true);
    setTranscriptError(null);
    setTranscript(null);

    try {
      const formData = new FormData();
      formData.append("audio_file", audioBlob, "recording.mp3");

      const response = await fetch("http://localhost:8000/api/transcribe", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Transcription failed");
      }

      const data = await response.json();
      setTranscript(data.transcript);
      setShowTranscript(true);
    } catch (error) {
      console.error("Transcription error:", error);
      setTranscriptError(
        error instanceof Error ? error.message : "Transcription failed"
      );
    } finally {
      setIsTranscribing(false);
    }
  };

  // Reset recording state
  const resetRecording = () => {
    setIsRecording(false);
    setIsPlaying(false);
    setRecordingTime(0);
    setAudioBlob(null);
    setAudioUrl(null);
    setIsTranscribing(false);
    setTranscript(null);
    setTranscriptError(null);
    setShowTranscript(false);

    // Stop any ongoing playback
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <div className="min-h-screen flex">
      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md mx-auto">
          {/* Timer Display */}
          <div className="text-center mb-8">
            <div
              className={cn(
                "text-6xl md:text-7xl font-mono font-bold transition-colors mb-4",
                isRecording
                  ? "text-red-500 dark:text-red-400"
                  : audioUrl
                  ? "text-green-500 dark:text-green-400"
                  : "text-muted-foreground"
              )}
            >
              {formatTime(recordingTime)}
            </div>

            {isRecording && (
              <div className="flex items-center justify-center gap-2">
                <div className="w-3 h-3 bg-red-500 dark:bg-red-400 rounded-full animate-pulse"></div>
                <span className="text-lg text-red-500 dark:text-red-400 font-medium">
                  Recording...
                </span>
              </div>
            )}

            {audioUrl && !isRecording && (
              <p className="text-lg text-green-500 dark:text-green-400 font-medium">
                Recording Complete
              </p>
            )}
          </div>

          {/* Main Action Button */}
          <div className="flex justify-center mb-8">
            {!audioUrl ? (
              // Recording State
              <Button
                onClick={isRecording ? stopRecording : startRecording}
                size="lg"
                className={cn(
                  "w-32 h-32 rounded-full text-lg font-semibold transition-all",
                  isRecording
                    ? "bg-red-500 hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700"
                    : "bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700"
                )}
              >
                {isRecording ? (
                  <Square className="h-8 w-8" />
                ) : (
                  <Mic className="h-8 w-8" />
                )}
              </Button>
            ) : (
              // Playback State
              <div className="space-y-4">
                <div className="flex gap-3 justify-center">
                  <Button
                    onClick={togglePlayback}
                    size="lg"
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    {isPlaying ? (
                      <>
                        <Pause className="h-4 w-4" />
                        Pause
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4" />
                        Play
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={downloadAudio}
                    size="lg"
                    className="flex items-center gap-2 bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700"
                  >
                    <Download className="h-4 w-4" />
                    Download
                  </Button>
                </div>

                <div className="flex gap-3 justify-center">
                  <Button
                    onClick={transcribeAudio}
                    disabled={isTranscribing}
                    size="lg"
                    className="flex items-center gap-2 bg-purple-500 hover:bg-purple-600 dark:bg-purple-600 dark:hover:bg-purple-700 disabled:opacity-50"
                  >
                    {isTranscribing ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Transcribing...
                      </>
                    ) : (
                      <>
                        <span className="text-sm font-bold">AI</span>
                        Transcribe
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={resetRecording}
                    size="lg"
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    <RotateCcw className="h-4 w-4" />
                    Record Again
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Instructions */}
          <div className="text-center">
            {!audioUrl ? (
              <p className="text-muted-foreground">
                {isRecording
                  ? "Click the stop button to end recording"
                  : "Click the microphone to start recording"}
              </p>
            ) : (
              <p className="text-muted-foreground">
                Review your recording and choose an action
              </p>
            )}
          </div>

          {/* Hidden audio element for playback */}
          {audioUrl && (
            <audio ref={audioRef} src={audioUrl} className="hidden" />
          )}
        </div>
      </div>

      {/* Side Panel for Transcript */}
      {(transcript || transcriptError || isTranscribing) && (
        <div className="w-96 border-l bg-card/50 backdrop-blur-sm">
          <div className="p-6 h-full">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold">Transcript</h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowTranscript(!showTranscript)}
                className="h-8 w-8 p-0"
              >
                {showTranscript ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
              </Button>
            </div>

            {showTranscript && (
              <div className="space-y-4">
                {isTranscribing && (
                  <div className="flex items-center justify-center py-12">
                    <div className="text-center">
                      <Loader2 className="h-8 w-8 animate-spin text-purple-500 mx-auto mb-3" />
                      <p className="text-muted-foreground">
                        Transcribing your audio...
                      </p>
                      <p className="text-sm text-muted-foreground mt-1">
                        This may take a few moments
                      </p>
                    </div>
                  </div>
                )}

                {transcriptError && (
                  <div className="p-4 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg">
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                      <div>
                        <p className="text-red-600 dark:text-red-400 font-medium">
                          Transcription Failed
                        </p>
                        <p className="text-red-600 dark:text-red-400 text-sm mt-1">
                          {transcriptError}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {transcript && !isTranscribing && (
                  <div className="space-y-4">
                    <div className="p-4 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
                      <div className="flex items-start gap-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                        <div>
                          <p className="text-green-600 dark:text-green-400 font-medium mb-2">
                            Transcription Complete
                          </p>
                          <p className="text-green-800 dark:text-green-200 leading-relaxed">
                            {transcript}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="pt-4 border-t">
                      <Button
                        onClick={() =>
                          navigator.clipboard.writeText(transcript)
                        }
                        variant="outline"
                        size="sm"
                        className="w-full"
                      >
                        Copy Transcript
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
