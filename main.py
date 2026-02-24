#!/usr/bin/env python3
"""
Text-to-ggwave converter
Converts user text input into ggwave-encoded WAV audio files.
"""

import os
import sys
from datetime import datetime
from src.encoder import encode_text_to_wav


def generate_output_filename():
    """Generate a timestamp-based output filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"output_{timestamp}.wav"


def main():
    """Main CLI interface for the text-to-ggwave converter."""
    print("Text-to-ggwave Converter")
    print("-" * 40)
    
    # Prompt user for text input
    user_text = input("Enter the text you want to convert to ggwave: ").strip()
    
    if not user_text:
        print("Error: No text provided.")
        sys.exit(1)
    
    # Generate output filename with timestamp
    output_filename = generate_output_filename()
    output_path = os.path.join("output", output_filename)
    
    try:
        print(f"Encoding text...")
        encode_text_to_wav(user_text, output_path)
        print(f"Success! Audio saved to: {output_path}")
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
