import random
import textwrap

# Constants
FREQ_COUNT = 1  # Only one frequency now
FREQ_MIN = 1000
FREQ_MAX = 8000

# Seed for reproducibility
random.seed()

# Pick a single frequency
frequencies = [random.randint(FREQ_MIN, FREQ_MAX)]

# Encoder template
ENCODER_TEMPLATE = textwrap.dedent("""
import numpy as np
import soundfile as sf
import os
import sys
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

fs = 22050
symbol_duration = 0.005
bits_per_symbol = 6
frequencies = {frequencies}

samples_per_symbol = int(fs * symbol_duration)
t = np.linspace(0, symbol_duration, samples_per_symbol, endpoint=False)
# Base waveform now only has one waveform
base_waveforms = {{
    0: np.sin(2 * np.pi * frequencies[0] * t)
}}

def bytes_to_bits(data):
    return [(byte >> (7 - i)) & 1 for byte in tqdm(data, desc="📊 Converting bytes to bits") for i in range(8)]

def bits_to_symbols(bits):
    symbols = []
    for i in tqdm(range(0, len(bits), bits_per_symbol), desc="🔄 Converting bits to symbols"):
        chunk = bits[i:i+bits_per_symbol]
        if len(chunk) < bits_per_symbol:
            chunk += [0] * (bits_per_symbol - len(chunk))
        val = 0
        for bit in chunk:
            val = (val << 1) | bit
        # Since only one frequency, all symbols map to 0
        symbols.append(0)
    return symbols

def get_file_metadata(path):
    name = os.path.basename(path)
    return name.encode("utf-8")

def encode_metadata_and_data(metadata, data):
    size = len(metadata)
    if size > 65535:
        raise ValueError("Metadata too large!")
    size_bytes = size.to_bytes(2, "big")
    return size_bytes + metadata + data

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    input_path = filedialog.askopenfilename(title="📁 Select the file to encode")
    if not input_path:
        print("No file selected. Exiting.")
        sys.exit(0)

    print(f"📂 Reading input file: {{input_path}}")
    with open(input_path, "rb") as f:
        file_data = f.read()

    metadata = get_file_metadata(input_path)
    payload = encode_metadata_and_data(metadata, file_data)

    print("📊 Encoding to bits...")
    bits = bytes_to_bits(payload)
    print("🔄 Converting to symbols...")
    symbols = bits_to_symbols(bits)

    output_path = os.path.splitext(input_path)[0] + ".wav"
    print(f"🔊 Streaming encoding to {{output_path}}...")
    with sf.SoundFile(output_path, mode='w', samplerate=fs, channels=1, subtype='PCM_16') as wavfile:
        for sym in tqdm(symbols, desc="🔊 Writing symbols to file"):
            wavfile.write(base_waveforms[sym])

    print("✅ Encoding complete!")
    input("Press Enter to exit...")
""").format(frequencies=frequencies)

# Decoder template with streaming read
DECODER_TEMPLATE = textwrap.dedent("""
import numpy as np
import soundfile as sf
import os
import sys
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

fs = 22050
symbol_duration = 0.005
bits_per_symbol = 6
frequencies = {frequencies}

t_samples = int(fs * symbol_duration)
t = np.linspace(0, symbol_duration, t_samples, endpoint=False)
# Only one base wave
base_waves = np.array([
    np.sin(2 * np.pi * frequencies[0] * t)
])

def decode_audio_to_symbols_streaming(input_wav, frequencies):
    symbols = []
    with sf.SoundFile(input_wav) as wavfile:
        total_frames = wavfile.frames
        total_symbols = total_frames // t_samples
        print(f"🎧 Decoding {{total_symbols}} symbols...")
        for _ in tqdm(range(total_symbols), desc="📡 Matching tones"):
            segment = wavfile.read(frames=t_samples, dtype='float32')
            if len(segment) < t_samples:
                break
            # Only one frequency, all segments map to symbol 0
            symbols.append(0)
    return symbols

def symbols_to_bits(symbols, bits_per_symbol):
    bits = []
    for sym in tqdm(symbols, desc="🔄 Symbols to bits"):
        for bit_pos in reversed(range(bits_per_symbol)):
            bits.append((sym >> bit_pos) & 1)
    return bits

def bits_to_bytes(bits):
    out = []
    for i in tqdm(range(0, len(bits), 8), desc="🔁 Bits to bytes"):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits += [0] * (8 - len(byte_bits))
        val = 0
        for b in byte_bits:
            val = (val << 1) | b
        out.append(val)
    return bytes(out)

def decode_metadata_and_data(data):
    if len(data) < 2:
        raise ValueError("Data too short to contain metadata size!")
    size = int.from_bytes(data[:2], "big")
    if len(data) < 2 + size:
        raise ValueError("Data too short for metadata size!")
    metadata = data[2:2+size]
    file_data = data[2+size:]
    return metadata, file_data

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    input_wav = filedialog.askopenfilename(title="📁 Select the encoded WAV to decode", filetypes=[("WAV files", "*.wav")])
    if not input_wav:
        print("No file selected. Exiting.")
        sys.exit(0)

    symbols = decode_audio_to_symbols_streaming(input_wav, frequencies)
    bits = symbols_to_bits(symbols, bits_per_symbol)
    byte_data = bits_to_bytes(bits)

    try:
        metadata, file_data = decode_metadata_and_data(byte_data)
        filename = metadata.decode('utf-8')
        print(f"ℹ️ Original filename: {{filename}}")
    except Exception as e:
        print(f"⚠️ Metadata error: {{e}}")
        filename = "decoded_output.bin"
        file_data = byte_data

    save_path = filedialog.asksaveasfilename(title="💾 Save decoded file", initialfile=filename)
    if not save_path:
        sys.exit(0)
    with open(save_path, "wb") as f:
        f.write(file_data)

    print("✅ Decoding complete!")
    input("Press Enter to exit...")
""").format(frequencies=frequencies)

def main():
    with open("generated_encoder.py", "w", encoding="utf-8") as f:
        f.write(ENCODER_TEMPLATE)
    with open("generated_decoder.py", "w", encoding="utf-8") as f:
        f.write(DECODER_TEMPLATE)
    print("✅ Generated streaming encoder and decoder scripts with a single frequency.")

if __name__ == "__main__":
    main()
