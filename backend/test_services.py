#!/usr/bin/env python3
"""
Test script to verify services can start without import errors
"""

import sys
import os
import importlib.util

def test_import(module_path, module_name):
    """Test if a module can be imported"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ {module_name} imports successfully")
        return True
    except Exception as e:
        print(f"❌ {module_name} import failed: {e}")
        return False

def main():
    """Test all service imports"""
    print("Testing Service Imports")
    print("=" * 40)
    
    # Test transcriber service
    print("\n1. Testing Transcriber Service:")
    transcriber_main = "services/transcriber/main.py"
    transcriber_transcription = "services/transcriber/transcription.py"
    
    test_import(transcriber_transcription, "transcription")
    test_import(transcriber_main, "transcriber_main")
    
    # Test notary service
    print("\n2. Testing Notary Service:")
    notary_main = "services/notary/main.py"
    notary_nlp = "services/notary/nlp_extractor.py"
    notary_formatter = "services/notary/note_formatter.py"
    
    test_import(notary_nlp, "nlp_extractor")
    test_import(notary_formatter, "note_formatter")
    test_import(notary_main, "notary_main")
    
    # Test main orchestrator
    print("\n3. Testing Main Orchestrator:")
    main_orchestrator = "main.py"
    test_import(main_orchestrator, "main_orchestrator")
    
    print("\n" + "=" * 40)
    print("Import tests completed!")

if __name__ == "__main__":
    main()
