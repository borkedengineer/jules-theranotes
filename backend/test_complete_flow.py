#!/usr/bin/env python3
"""
Test script for the complete therapy session processing flow
"""

import requests
import json
import os
from pathlib import Path

def test_complete_flow():
    """Test the complete end-to-end flow"""
    
    # API endpoints
    MAIN_API_URL = "http://localhost:8002"
    TRANSCRIBER_URL = "http://localhost:8000"
    NOTARY_URL = "http://localhost:8001"
    
    print("Testing Complete Therapy Session Processing Flow")
    print("=" * 60)
    
    # Test 1: Health checks
    print("\n1. Testing service health...")
    try:
        response = requests.get(f"{MAIN_API_URL}/health")
        print(f"✅ Main API: {response.status_code}")
        
        response = requests.get(f"{TRANSCRIBER_URL}/health")
        print(f"✅ Transcriber: {response.status_code}")
        
        response = requests.get(f"{NOTARY_URL}/health")
        print(f"✅ Notary: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Test with sample transcript (no audio file needed)
    print("\n2. Testing NLP extraction with sample transcript...")
    
    sample_transcript = """
    Today I met with Sarah Johnson for our weekly session on March 15th, 2024. 
    The goal of today's session was to work on her depression management and 
    discuss her recent medication changes.
    
    We discussed her recent struggles with motivation and how she's been feeling
    more isolated since her job change. Sarah mentioned that she's been having
    trouble sleeping and feels overwhelmed by daily tasks.
    
    I conducted a brief assessment using the PHQ-9 scale, and she scored 15,
    indicating moderate to severe depression. We also reviewed her previous
    diagnosis of major depressive disorder and generalized anxiety disorder.
    
    During the session, I used cognitive behavioral therapy techniques to help
    her identify negative thought patterns. Sarah responded well to the intervention
    and was able to identify specific triggers for her depressive episodes.
    
    For our next session, we plan to continue working on behavioral activation
    techniques and develop a daily routine. Sarah agreed to practice mindfulness
    exercises and keep a mood journal. We also discussed increasing her therapy
    sessions to twice weekly.
    """
    
    try:
        response = requests.post(
            f"{NOTARY_URL}/api/format-therapy-note",
            json={"transcript": sample_transcript}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ NLP extraction successful!")
            print("\nGenerated Therapy Note:")
            print("-" * 40)
            print(data["therapy_note"])
        else:
            print(f"❌ NLP extraction failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ NLP extraction error: {e}")
    
    # Test 3: Test with audio file (if available)
    print("\n3. Testing complete flow with audio file...")
    
    # Look for test audio files
    test_audio_files = [
        "test_audio.mp3",
        "test_audio.wav",
        "test_audio.m4a",
        "sample_audio.mp3"
    ]
    
    audio_file_path = None
    for filename in test_audio_files:
        if os.path.exists(filename):
            audio_file_path = filename
            break
    
    if audio_file_path:
        print(f"Found test audio file: {audio_file_path}")
        try:
            with open(audio_file_path, 'rb') as f:
                files = {'audio_file': f}
                response = requests.post(
                    f"{MAIN_API_URL}/api/generate-therapy-note",
                    files=files
                )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Complete flow successful!")
                print("\nGenerated Therapy Note:")
                print("-" * 40)
                print(data["therapy_note"])
                
                print("\nProcessing Summary:")
                summary = data.get("processing_summary", {})
                for key, value in summary.items():
                    print(f"  {key}: {value}")
            else:
                print(f"❌ Complete flow failed: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Complete flow error: {e}")
    else:
        print("ℹ️  No test audio file found. Skipping audio test.")
        print("   To test with audio, place an MP3/WAV file in the backend directory")
    
    print("\n" + "=" * 60)
    print("Test completed!")

def show_api_endpoints():
    """Show available API endpoints"""
    print("\nAvailable API Endpoints:")
    print("-" * 30)
    print("Main API (Port 8002):")
    print("  POST /api/generate-therapy-note  - Complete end-to-end processing")
    print("  POST /api/transcribe             - Transcribe audio only")
    print("  POST /api/extract-session-data   - Extract session data only")
    print("  GET  /health                     - Health check")
    print("  GET  /docs                       - API documentation")
    
    print("\nTranscriber Service (Port 8000):")
    print("  POST /api/transcribe             - Transcribe audio file")
    print("  GET  /health                     - Health check")
    print("  GET  /docs                       - API documentation")
    
    print("\nNotary Service (Port 8001):")
    print("  POST /api/extract-session-data   - Extract structured data")
    print("  POST /api/format-therapy-note    - Generate therapy note")
    print("  GET  /api/supported-fields       - Get supported fields")
    print("  GET  /health                     - Health check")
    print("  GET  /docs                       - API documentation")

if __name__ == "__main__":
    show_api_endpoints()
    test_complete_flow()
