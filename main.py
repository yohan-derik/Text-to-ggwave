#!/usr/bin/env python3
"""Text-to-ggwave converter - Convert text to FSK-encoded WAV audio."""

import sys
from datetime import datetime
from src.encoder import encode_text_to_wav


def main():
    print("Text-to-ggwave Converter")
    print("-" * 40)
    
    user_text = input("Enter text to convert: ").strip()
    
    if not user_text:
        print("Error: No text provided")
        sys.exit(1)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output/output_{timestamp}.wav"
    
    try:
        encode_text_to_wav(user_text, output_path)
        print(f"Success! Audio saved to: {output_path}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"File error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
