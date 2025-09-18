"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Mic, Square, Play, Pause, Download } from "lucide-react";
import { cn } from "@/lib/utils";

interface AudioRecorderProps {}

export default function AudioRecorder({}: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

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
    <div className="min-h-screen flex items-center justify-center p-4">
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
            <div className="flex gap-4">
              <Button
                onClick={togglePlayback}
                size="lg"
                variant="outline"
                className="w-20 h-20 rounded-full"
              >
                {isPlaying ? (
                  <Pause className="h-6 w-6" />
                ) : (
                  <Play className="h-6 w-6" />
                )}
              </Button>

              <Button
                onClick={downloadAudio}
                size="lg"
                className="w-20 h-20 rounded-full bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700"
              >
                <Download className="h-6 w-6" />
              </Button>
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
              Use the play button to review your recording, or download it as an
              MP3
            </p>
          )}
        </div>

        {/* Hidden audio element for playback */}
        {audioUrl && <audio ref={audioRef} src={audioUrl} className="hidden" />}
      </div>
    </div>
  );
}
