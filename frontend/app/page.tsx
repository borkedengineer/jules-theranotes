"use client";

import React from "react";
import AudioRecorder from "@/components/audio-recorder";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileText, Shield, Zap } from "lucide-react";

export default function Home() {
  const handleAudioUpload = async (audioBlob: Blob) => {
    // For now, just log the blob - we'll implement actual upload later
    console.log("Audio blob received:", audioBlob);
    console.log("Audio size:", audioBlob.size, "bytes");
    console.log("Audio type:", audioBlob.type);

    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Here you would typically send the blob to your backend
    // const formData = new FormData()
    // formData.append('audio', audioBlob, 'recording.webm')
    // const response = await fetch('/api/upload', {
    //   method: 'POST',
    //   body: formData
    // })
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Jules Theranotes
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Streamline your therapy session note-taking with AI-powered
            transcription and structured data extraction
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-blue-500" />
                Fast Recording
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Record session summaries quickly with high-quality audio capture
                and real-time transcription.
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-green-500" />
                Smart Processing
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                AI extracts structured data like client info, interventions, and
                outcomes automatically.
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-purple-500" />
                Privacy First
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                All processing happens locally. Your sensitive client data never
                leaves your device.
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        {/* Audio Recorder */}
        <AudioRecorder onUpload={handleAudioUpload} />

        {/* Instructions */}
        <div className="mt-12 max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>How to Use</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-semibold">
                  1
                </div>
                <div>
                  <h3 className="font-semibold">Record Your Session</h3>
                  <p className="text-sm text-muted-foreground">
                    Click "Start Recording" and speak your session summary. The
                    timer will show your recording duration.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-semibold">
                  2
                </div>
                <div>
                  <h3 className="font-semibold">Review & Playback</h3>
                  <p className="text-sm text-muted-foreground">
                    Listen to your recording to ensure it's complete and
                    accurate before processing.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-semibold">
                  3
                </div>
                <div>
                  <h3 className="font-semibold">Upload for Processing</h3>
                  <p className="text-sm text-muted-foreground">
                    Click "Upload for Processing" to transcribe and extract
                    structured data from your recording.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
