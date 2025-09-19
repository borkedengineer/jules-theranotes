#!/usr/bin/env python3
"""
Test script for therapy session data extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp_extractor import TherapySessionExtractor

def test_extraction():
    """Test the NLP extraction with sample therapy session transcript"""
    
    sample_transcript = """
    Today I met with John Smith for our weekly session on March 15th, 2024. 
    The goal of today's session was to work on his anxiety management techniques.
    
    We discussed his recent panic attacks and how they've been affecting his work performance.
    John mentioned that he's been having trouble sleeping and feels overwhelmed at work.
    
    I conducted a brief assessment using the GAD-7 scale, and he scored 12, indicating moderate anxiety.
    We also reviewed his previous diagnosis of generalized anxiety disorder.
    
    During the session, I used cognitive behavioral therapy techniques to help him identify
    negative thought patterns. John responded well to the intervention and was able to
    identify three specific triggers for his anxiety.
    
    For our next session, we plan to continue working on relaxation techniques and
    develop a coping strategy for work-related stress. John agreed to practice
    deep breathing exercises daily and keep a mood journal.
    """
    
    print("Testing Therapy Session Data Extraction")
    print("=" * 50)
    
    extractor = TherapySessionExtractor()
    result = extractor.extract_session_data(sample_transcript)
    
    print("Extracted Data:")
    print("-" * 30)
    
    for key, value in result.items():
        if key != "raw_transcript":
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_extraction()
