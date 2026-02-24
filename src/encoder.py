import numpy as np
from scipy.io import wavfile
import os
from src.config import PROTOCOLS, VOLUME, SAMPLE_RATE


def sanitize_text(text):
    """
    Sanitize input text to ASCII-only characters.
    Removes or replaces non-ASCII characters.
    """
    # Encode to ASCII, replacing non-ASCII characters
    sanitized = text.encode('ascii', errors='ignore').decode('ascii')
    return sanitized


def select_protocol(text_length):
    """
    Select the appropriate protocol based on text length.
    Returns the protocol with the smallest max_length that can fit the text,
    ensuring highest robustness for the given payload size.
    """
    # Sort protocols by max_length in ascending order (highest robustness first)
    sorted_protocols = sorted(PROTOCOLS.values(), key=lambda p: p["max_length"])
    
    for protocol in sorted_protocols:
        if text_length <= protocol["max_length"]:
            return protocol
    
    # If text is too long for all protocols, return None
    return None


def encode_text_fsk(text, protocol_id, volume, sample_rate):
    """
    Encode text using FSK (Frequency Shift Keying) modulation.
    This is a pure Python implementation that doesn't require C++ compilation.
    
    Args:
        text (str): Text to encode (ASCII only)
        protocol_id (int): Protocol ID (affects encoding parameters)
        volume (int): Volume level (0-100)
        sample_rate (int): Audio sample rate (Hz)
    
    Returns:
        np.ndarray: 16-bit signed integer array of audio samples
    """
    # Protocol-based encoding parameters
    protocol_params = {
        1: {"freq_mark": 2400, "freq_space": 1200, "baud_rate": 8},
        2: {"freq_mark": 2400, "freq_space": 1200, "baud_rate": 16},
        3: {"freq_mark": 2400, "freq_space": 1200, "baud_rate": 32},
    }
    
    params = protocol_params.get(protocol_id, protocol_params[1])
    freq_mark = params["freq_mark"]   # High frequency (bit=1)
    freq_space = params["freq_space"]  # Low frequency (bit=0)
    baud_rate = params["baud_rate"]   # Bits per second
    
    # Convert volume (0-100) to amplitude (0-32767 for 16-bit)
    amplitude = int((volume / 100.0) * 32767)
    
    # Calculate samples per bit
    samples_per_bit = sample_rate // baud_rate
    
    # Convert text to binary
    binary_string = ""
    for char in text:
        binary_string += format(ord(char), '08b')
    
    # Generate audio samples
    total_samples = len(binary_string) * samples_per_bit
    samples = np.zeros(total_samples, dtype=np.int16)
    
    time = np.arange(samples_per_bit) / sample_rate
    
    for bit_idx, bit in enumerate(binary_string):
        # Select frequency based on bit value
        frequency = freq_mark if bit == '1' else freq_space
        
        # Generate sine wave for this bit
        bit_samples = np.sin(2 * np.pi * frequency * time)
        
        # Apply amplitude
        bit_samples = (bit_samples * amplitude).astype(np.int16)
        
        # Add to output
        start_idx = bit_idx * samples_per_bit
        end_idx = start_idx + samples_per_bit
        samples[start_idx:end_idx] = bit_samples
    
    # Add silence at the beginning and end for better encoding/decoding
    silence_samples = int(sample_rate * 0.1)  # 100ms of silence
    silence = np.zeros(silence_samples, dtype=np.int16)
    
    samples = np.concatenate([silence, samples, silence])
    
    return samples


def encode_text_to_wav(text, output_path):
    """
    Encode text to FSK audio and save as WAV file.
    
    Args:
        text (str): Text to encode
        output_path (str): Path to save the WAV file
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        ValueError: If text is too long or invalid
    """
    # Sanitize input text
    sanitized_text = sanitize_text(text)
    
    if not sanitized_text:
        raise ValueError("Text is empty after sanitization")
    
    text_length = len(sanitized_text)
    
    # Select appropriate protocol
    protocol = select_protocol(text_length)
    
    if protocol is None:
        raise ValueError(
            f"Text is too long ({text_length} chars). "
            f"Maximum supported length is {max(p['max_length'] for p in PROTOCOLS.values())} characters."
        )
    
    # Encode text to FSK waveform
    try:
        samples = encode_text_fsk(sanitized_text, protocol["id"], VOLUME, SAMPLE_RATE)
    except Exception as e:
        raise ValueError(f"Failed to encode text with FSK: {str(e)}")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to WAV file
    try:
        wavfile.write(output_path, SAMPLE_RATE, samples)
        return True
    except Exception as e:
        raise IOError(f"Failed to write WAV file: {str(e)}")
