import numpy as np
from scipy.io import wavfile
import os

# Configuration
MAX_LENGTH = 250
VOLUME = 50
SAMPLE_RATE = 48000
FREQ_MARK = 2400
FREQ_SPACE = 1200
BAUD_RATE = 16


def sanitize_text(text):
    """Sanitize input text to ASCII-only characters."""
    return text.encode('ascii', errors='ignore').decode('ascii')


def encode_text_fsk(text):
    """
    Encode text using FSK (Frequency Shift Keying) modulation.
    
    Args:
        text (str): ASCII text to encode
    
    Returns:
        np.ndarray: 16-bit signed integer audio samples
    """
    amplitude = int((VOLUME / 100.0) * 32767)
    samples_per_bit = SAMPLE_RATE // BAUD_RATE
    
    # Convert text to binary
    binary_string = "".join(format(ord(char), '08b') for char in text)
    
    # Generate audio samples
    total_samples = len(binary_string) * samples_per_bit
    samples = np.zeros(total_samples, dtype=np.int16)
    time = np.arange(samples_per_bit) / SAMPLE_RATE
    
    for bit_idx, bit in enumerate(binary_string):
        frequency = FREQ_MARK if bit == '1' else FREQ_SPACE
        bit_samples = np.sin(2 * np.pi * frequency * time)
        bit_samples = (bit_samples * amplitude).astype(np.int16)
        
        start_idx = bit_idx * samples_per_bit
        samples[start_idx:start_idx + samples_per_bit] = bit_samples
    
    # Add silence at beginning and end
    silence = np.zeros(int(SAMPLE_RATE * 0.1), dtype=np.int16)
    return np.concatenate([silence, samples, silence])


def encode_text_to_wav(text, output_path):
    """
    Encode text to FSK audio and save as WAV file.
    
    Args:
        text (str): Text to encode
        output_path (str): Path to save the WAV file
    
    Raises:
        ValueError: If text is invalid
        IOError: If file write fails
    """
    sanitized_text = sanitize_text(text)
    
    if not sanitized_text:
        raise ValueError("Text is empty after sanitization")
    
    if len(sanitized_text) > MAX_LENGTH:
        raise ValueError(f"Text too long ({len(sanitized_text)} > {MAX_LENGTH} chars)")
    
    samples = encode_text_fsk(sanitized_text)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wavfile.write(output_path, SAMPLE_RATE, samples)
