"""
NLP service for extracting structured data from therapy session transcripts
"""

import spacy
import re
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TherapySessionExtractor:
    def __init__(self):
        """Initialize the NLP extractor with spaCy model"""
        try:
            # Load spaCy model (download with: python -m spacy download en_core_web_sm)
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_session_data(self, transcript: str) -> Dict[str, Any]:
        """
        Extract structured data from therapy session transcript
        
        Args:
            transcript: Raw transcript text from speech-to-text
            
        Returns:
            Dictionary with extracted session data
        """
        if not transcript or not transcript.strip():
            return self._empty_session_data()
        
        # Clean and preprocess transcript
        cleaned_transcript = self._clean_transcript(transcript)
        
        # Extract different components
        session_data = {
            "goal": self._extract_goal(cleaned_transcript),
            "content": self._extract_content(cleaned_transcript),
            "assessment": self._extract_assessment(cleaned_transcript),
            "diagnoses": self._extract_diagnoses(cleaned_transcript),
            "intervention_response": self._extract_intervention_response(cleaned_transcript),
            "plan": self._extract_plan(cleaned_transcript),
            "client_name": self._extract_client_name(cleaned_transcript),
            "session_date": self._extract_session_date(cleaned_transcript),
            "raw_transcript": transcript
        }
        
        return session_data
    
    def _clean_transcript(self, text: str) -> str:
        """Clean and normalize transcript text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common speech-to-text errors
        text = re.sub(r'\b(uh|um|er|ah)\b', '', text, flags=re.IGNORECASE)
        
        return text
    
    def _extract_goal(self, text: str) -> str:
        """Extract session goal"""
        goal_patterns = [
            r"goal.*?was\s+(.*?)(?:\.|$)",
            r"objective.*?was\s+(.*?)(?:\.|$)",
            r"focus.*?was\s+(.*?)(?:\.|$)",
            r"wanted to\s+(.*?)(?:\.|$)",
            r"hoped to\s+(.*?)(?:\.|$)",
            r"session goal.*?:\s*(.*?)(?:\.|$)",
        ]
        
        for pattern in goal_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return "Goal not explicitly stated"
    
    def _extract_content(self, text: str) -> str:
        """Extract main content discussed"""
        # Look for content indicators
        content_patterns = [
            r"discussed\s+(.*?)(?:\.|assessment|diagnosis|plan)",
            r"talked about\s+(.*?)(?:\.|assessment|diagnosis|plan)",
            r"covered\s+(.*?)(?:\.|assessment|diagnosis|plan)",
            r"session focused on\s+(.*?)(?:\.|assessment|diagnosis|plan)",
        ]
        
        for pattern in content_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # Fallback: extract first few sentences as content
        sentences = text.split('.')[:3]
        return '. '.join(sentences).strip()
    
    def _extract_assessment(self, text: str) -> str:
        """Extract assessment information"""
        assessment_patterns = [
            r"assessment.*?:\s*(.*?)(?:\.|diagnosis|plan)",
            r"evaluated\s+(.*?)(?:\.|diagnosis|plan)",
            r"assessed\s+(.*?)(?:\.|diagnosis|plan)",
            r"testing.*?:\s*(.*?)(?:\.|diagnosis|plan)",
            r"evaluation.*?:\s*(.*?)(?:\.|diagnosis|plan)",
        ]
        
        for pattern in assessment_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return "No formal assessment mentioned"
    
    def _extract_diagnoses(self, text: str) -> List[str]:
        """Extract mental health diagnoses"""
        # Common mental health conditions
        diagnoses = [
            "ADHD", "ADD", "Attention Deficit Hyperactivity Disorder",
            "depression", "major depressive disorder", "MDD",
            "anxiety", "generalized anxiety disorder", "GAD",
            "bipolar", "bipolar disorder", "manic depression",
            "PTSD", "post-traumatic stress disorder",
            "OCD", "obsessive compulsive disorder",
            "autism", "autism spectrum disorder", "ASD",
            "borderline personality disorder", "BPD",
            "schizophrenia", "schizoaffective disorder",
            "eating disorder", "anorexia", "bulimia",
            "substance abuse", "alcoholism", "addiction"
        ]
        
        found_diagnoses = []
        text_lower = text.lower()
        
        for diagnosis in diagnoses:
            if diagnosis.lower() in text_lower:
                found_diagnoses.append(diagnosis)
        
        return found_diagnoses if found_diagnoses else ["No diagnoses mentioned"]
    
    def _extract_intervention_response(self, text: str) -> str:
        """Extract interventions and client responses"""
        intervention_patterns = [
            r"intervention.*?:\s*(.*?)(?:\.|plan)",
            r"used\s+(.*?)(?:\.|plan)",
            r"applied\s+(.*?)(?:\.|plan)",
            r"implemented\s+(.*?)(?:\.|plan)",
            r"client responded\s+(.*?)(?:\.|plan)",
            r"response was\s+(.*?)(?:\.|plan)",
        ]
        
        for pattern in intervention_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return "Interventions not explicitly documented"
    
    def _extract_plan(self, text: str) -> str:
        """Extract future plan and next steps"""
        plan_patterns = [
            r"plan.*?:\s*(.*?)(?:\.|$)",
            r"next steps.*?:\s*(.*?)(?:\.|$)",
            r"homework.*?:\s*(.*?)(?:\.|$)",
            r"follow up.*?:\s*(.*?)(?:\.|$)",
            r"continue.*?:\s*(.*?)(?:\.|$)",
            r"work on\s+(.*?)(?:\.|$)",
        ]
        
        for pattern in plan_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return "Plan not explicitly stated"
    
    def _extract_client_name(self, text: str) -> str:
        """Extract client name using spaCy NER"""
        if not self.nlp:
            return "Client name not extracted (spaCy not available)"
        
        doc = self.nlp(text)
        
        # Look for PERSON entities
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
        
        # Fallback: look for common name patterns
        name_patterns = [
            r"client\s+(\w+)\s+",
            r"patient\s+(\w+)\s+",
            r"(\w+)\s+is\s+(?:the\s+)?client",
            r"(\w+)\s+is\s+(?:the\s+)?patient",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Client name not found"
    
    def _extract_session_date(self, text: str) -> str:
        """Extract session date"""
        if not self.nlp:
            return "Session date not extracted (spaCy not available)"
        
        doc = self.nlp(text)
        
        # Look for DATE entities
        for ent in doc.ents:
            if ent.label_ == "DATE":
                return ent.text.strip()
        
        # Fallback: look for common date patterns
        date_patterns = [
            r"session\s+on\s+(\w+\s+\d{1,2},?\s+\d{4})",
            r"(\w+\s+\d{1,2},?\s+\d{4})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
            r"(\d{4}-\d{2}-\d{2})",
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return "Session date not found"
    
    def _empty_session_data(self) -> Dict[str, Any]:
        """Return empty session data structure"""
        return {
            "goal": "No transcript provided",
            "content": "No transcript provided",
            "assessment": "No transcript provided",
            "diagnoses": ["No transcript provided"],
            "intervention_response": "No transcript provided",
            "plan": "No transcript provided",
            "client_name": "Not specified",
            "session_date": "Not specified",
            "raw_transcript": ""
        }
