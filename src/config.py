# Configuration for text-to-ggwave encoding

# Protocol definitions with increasing robustness
# Each protocol has a protocol ID, max payload length, and description
PROTOCOLS = {
    1: {
        "id": 1,
        "max_length": 250,
        "description": "Standard robustness"
    },
    2: {
        "id": 2,
        "max_length": 150,
        "description": "Higher robustness"
    },
    3: {
        "id": 3,
        "max_length": 50,
        "description": "Highest robustness"
    }
}

# Fixed high-robustness volume level (0-100)
VOLUME = 50

# Sample rate for WAV files (ggwave standard)
SAMPLE_RATE = 48000
