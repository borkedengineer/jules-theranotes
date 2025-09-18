"use client";

import React from "react";
import AudioRecorder from "@/components/audio-recorder";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <AudioRecorder />
    </div>
  );
}
