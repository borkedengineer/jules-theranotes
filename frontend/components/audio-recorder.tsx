"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Mic, Square, Play, Pause, Upload, Download } from "lucide-react";
import { cn } from "@/lib/utils";

interface AudioRecorderProps {
  onUpload?: (audioBlob: Blob) => void;
}

export default function AudioRecorder({ onUpload }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const audioDataRef = useRef<Float32Array[]>([]);

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  // Convert Float32Array to WAV format
  const floatTo16BitPCM = (float32Array: Float32Array): Int16Array => {
    const buffer = new ArrayBuffer(float32Array.length * 2);
    const view = new DataView(buffer);
    let offset = 0;
    for (let i = 0; i < float32Array.length; i++, offset += 2) {
      let s = Math.max(-1, Math.min(1, float32Array[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    }
    return new Int16Array(buffer);
  };

  const writeString = (view: DataView, offset: number, string: string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  const encodeWAV = (
    samples: Float32Array,
    sampleRate: number = 44100
  ): ArrayBuffer => {
    const length = samples.length;
    const buffer = new ArrayBuffer(44 + length * 2);
    const view = new DataView(buffer);

    // WAV header
    writeString(view, 0, "RIFF");
    view.setUint32(4, 36 + length * 2, true);
    writeString(view, 8, "WAVE");
    writeString(view, 12, "fmt ");
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(view, 36, "data");
    view.setUint32(40, length * 2, true);

    // Convert float samples to 16-bit PCM
    const pcmData = floatTo16BitPCM(samples);
    for (let i = 0; i < pcmData.length; i++) {
      view.setInt16(44 + i * 2, pcmData[i], true);
    }

    return buffer;
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

      // Create AudioContext for WAV recording
      const audioContext = new (window.AudioContext ||
        (window as any).webkitAudioContext)({
        sampleRate: 44100,
      });
      audioContextRef.current = audioContext;

      const source = audioContext.createMediaStreamSource(stream);
      sourceRef.current = source;

      // Create ScriptProcessorNode to capture audio data
      const processor = audioContext.createScriptProcessor(4096, 1, 1);
      processorRef.current = processor;
      audioDataRef.current = [];

      processor.onaudioprocess = (event) => {
        const inputData = event.inputBuffer.getChannelData(0);
        audioDataRef.current.push(new Float32Array(inputData));
      };

      source.connect(processor);
      processor.connect(audioContext.destination);

      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Unable to access microphone. Please check permissions.");
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (isRecording) {
      setIsRecording(false);

      if (timerRef.current) {
        clearInterval(timerRef.current);
      }

      // Stop audio processing
      if (processorRef.current) {
        processorRef.current.disconnect();
      }
      if (sourceRef.current) {
        sourceRef.current.disconnect();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }

      // Convert audio data to WAV
      if (audioDataRef.current.length > 0) {
        // Calculate total length
        const totalLength = audioDataRef.current.reduce(
          (acc, chunk) => acc + chunk.length,
          0
        );

        // Create a single Float32Array with all audio data
        const audioData = new Float32Array(totalLength);
        let offset = 0;
        for (const chunk of audioDataRef.current) {
          audioData.set(chunk, offset);
          offset += chunk.length;
        }

        // Encode as WAV
        const wavBuffer = encodeWAV(audioData, 44100);
        const wavBlob = new Blob([wavBuffer], { type: "audio/wav" });

        setAudioBlob(wavBlob);
        const url = URL.createObjectURL(wavBlob);
        setAudioUrl(url);
      }

      // Clean up stream
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
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

  // Upload audio to backend
  const uploadAudio = async () => {
    if (!audioBlob || !onUpload) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Call the upload handler
      await onUpload(audioBlob);

      setUploadProgress(100);
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 500);
    } catch (error) {
      console.error("Upload failed:", error);
      setIsUploading(false);
      setUploadProgress(0);
      alert("Upload failed. Please try again.");
    }
  };

  // Download audio file
  const downloadAudio = () => {
    if (!audioBlob || !audioUrl) return;

    const link = document.createElement("a");
    link.href = audioUrl;

    // Since we're now using WAV format, always use .wav extension
    link.download = `recording-${new Date()
      .toISOString()
      .slice(0, 19)
      .replace(/:/g, "-")}.wav`;
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
      if (processorRef.current) {
        processorRef.current.disconnect();
      }
      if (sourceRef.current) {
        sourceRef.current.disconnect();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Mic className="h-5 w-5" />
            Audio Recorder
          </CardTitle>
          <CardDescription>
            Record your session summary. Click start to begin recording.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Timer Display */}
          <div className="text-center">
            <div
              className={cn(
                "text-4xl font-mono font-bold transition-colors",
                isRecording ? "text-red-500" : "text-gray-500"
              )}
            >
              {formatTime(recordingTime)}
            </div>
            {isRecording && (
              <div className="flex items-center justify-center gap-2 mt-2">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-red-500">Recording...</span>
              </div>
            )}
          </div>

          {/* Recording Controls */}
          <div className="flex justify-center gap-4">
            {!isRecording ? (
              <Button
                onClick={startRecording}
                size="lg"
                className="bg-red-500 hover:bg-red-600 text-white"
              >
                <Mic className="h-5 w-5 mr-2" />
                Start Recording
              </Button>
            ) : (
              <Button onClick={stopRecording} size="lg" variant="destructive">
                <Square className="h-5 w-5 mr-2" />
                Stop Recording
              </Button>
            )}
          </div>

          {/* Playback Controls */}
          {audioUrl && (
            <div className="space-y-4">
              <div className="flex justify-center gap-4">
                <Button onClick={togglePlayback} variant="outline" size="lg">
                  {isPlaying ? (
                    <Pause className="h-5 w-5 mr-2" />
                  ) : (
                    <Play className="h-5 w-5 mr-2" />
                  )}
                  {isPlaying ? "Pause" : "Play"}
                </Button>

                <Button onClick={downloadAudio} variant="outline" size="lg">
                  <Download className="h-5 w-5 mr-2" />
                  Download
                </Button>
              </div>

              <audio
                ref={audioRef}
                src={audioUrl}
                className="w-full"
                controls
              />
            </div>
          )}

          {/* Upload Section */}
          {audioBlob && onUpload && (
            <div className="space-y-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-2">
                  Ready to process your recording
                </p>
                <Button
                  onClick={uploadAudio}
                  disabled={isUploading}
                  size="lg"
                  className="w-full"
                >
                  <Upload className="h-5 w-5 mr-2" />
                  {isUploading ? "Uploading..." : "Upload for Processing"}
                </Button>
              </div>

              {isUploading && (
                <div className="space-y-2">
                  <Progress value={uploadProgress} className="w-full" />
                  <p className="text-sm text-center text-muted-foreground">
                    Uploading... {uploadProgress}%
                  </p>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
