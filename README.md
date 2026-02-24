# Text-to-ggwave Converter

A simple Python tool that converts text into FSK-encoded `.wav` audio files using frequency-shift keying modulation.

## Features

- **Pure Python**: No C++ compiler required
- **Easy to use**: One-line command to convert text to audio
- **ASCII sanitization**: Automatically removes non-ASCII characters
- **Timestamp filenames**: Output files are auto-named with timestamps
- **Error handling**: Clear error messages for invalid inputs

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Text-to-ggwave-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python main.py
```

Enter your text when prompted:
```
Text-to-ggwave Converter
----------------------------------------
Enter text to convert: Hello World
Success! Audio saved to: output/output_20260224_105022.wav
```

The `.wav` file will be saved in the `output/` folder.

## Limits

- **Maximum text length**: 250 characters
- **Character set**: ASCII only (non-ASCII characters are removed)

## How It Works

The tool encodes text using **FSK (Frequency-Shift Keying)**:
- Each character is converted to 8 binary bits
- Bits are encoded as frequencies:
  - `1` → 2400 Hz (mark)
  - `0` → 1200 Hz (space)
- Audio is generated at 48 kHz sample rate with volume 50

## Project Structure

```
Text-to-ggwave-main/
├── README.md
├── requirements.txt
├── main.py              # Entry point
├── src/
│   ├── __init__.py
│   └── encoder.py       # Encoding logic
└── output/              # Generated audio files
```

## Example

```python
from src.encoder import encode_text_to_wav

encode_text_to_wav("Hello", "output/hello.wav")
```

## Error Messages

- `Text too long` - Reduce text to 250 characters or fewer
- `Text is empty` - Ensure input contains at least one ASCII character
- File permission errors - Check that output directory is writable

## Dependencies

- **scipy** - WAV file writing
- **numpy** - Audio sample generation

## License

MIT