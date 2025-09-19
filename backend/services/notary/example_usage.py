#!/usr/bin/env python3
"""
Example usage of the therapy session data extraction
"""

import json
from nlp_extractor import TherapySessionExtractor

def main():
    # Sample therapy session transcript
    transcript = """
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
    
    # Initialize the extractor
    extractor = TherapySessionExtractor()
    
    # Extract structured data
    session_data = extractor.extract_session_data(transcript)
    
    # Print results in a nice format
    print("Therapy Session Data Extraction Results")
    print("=" * 50)
    
    for key, value in session_data.items():
        if key != "raw_transcript":
            print(f"\n{key.replace('_', ' ').title()}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"  {value}")
    
    print("\n" + "=" * 50)
    print("JSON Output:")
    print(json.dumps(session_data, indent=2))

if __name__ == "__main__":
    main()
