import random
import textwrap

# Constants
FREQ_COUNT = 64
FREQ_MIN = 1000
FREQ_MAX = 8000

# Seed for reproducibility
random.seed()

frequencies = sorted(random.sample(range(FREQ_MIN, FREQ_MAX), FREQ_COUNT))

# Encoder template with placeholder for frequencies
ENCODER_TEMPLATE = f'''  
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
        symbols.append(val)
    return symbols

def symbols_to_audio(symbols):
    t = np.linspace(0, symbol_duration, int(fs * symbol_duration), endpoint=False)
    print("🎛 Generating tone map...")
    base_waveforms = {{
        sym: np.sin(2 * np.pi * frequencies[sym] * t)
        for sym in tqdm(range(len(frequencies)), desc="🔊 Building waveforms")
    }}
    print("🎵 Encoding audio...")
    signal_parts = [base_waveforms.get(sym, np.zeros_like(t)) for sym in tqdm(symbols, desc="📡 Creating signal")]
    signal = np.concatenate(signal_parts)
    return signal / np.max(np.abs(signal))

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

    print(f"📦 File size: {{len(file_data)}} bytes")

    metadata = get_file_metadata(input_path)
    full_payload = encode_metadata_and_data(metadata, file_data)

    print("📊 Encoding to bits...")
    bits = bytes_to_bits(full_payload)
    print("🔄 Converting to symbols...")
    symbols = bits_to_symbols(bits)
    print("🎵 Generating audio...")
    audio_signal = symbols_to_audio(symbols)

    output_path = os.path.splitext(input_path)[0] + ".wav"
    print(f"💾 Saving encoded audio to: {{output_path}}")
    sf.write(output_path, audio_signal, fs)

    print("✅ Encoding complete!")
    input("Press Enter to exit...")
'''

# Decoder template with placeholder for frequencies
DECODER_TEMPLATE = f'''  
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

def decode_audio_to_symbols(audio, fs, symbol_duration, frequencies):
    samples_per_symbol = int(fs * symbol_duration)
    total_symbols = len(audio) // samples_per_symbol
    symbols = []

    print(f"🎧 Decoding {{total_symbols}} symbols...")
    t = np.linspace(0, symbol_duration, samples_per_symbol, endpoint=False)
    base_waves = np.array([
        np.sin(2 * np.pi * f * t)
        for f in frequencies
    ])

    for i in tqdm(range(total_symbols), desc="📡 Matching tones"):
        segment = audio[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        if len(segment) < samples_per_symbol:
            break
        correlations = np.dot(base_waves, segment)
        symbol = np.argmax(correlations)
        symbols.append(symbol)

    return symbols

def symbols_to_bits(symbols, bits_per_symbol):
    bits = []
    for sym in tqdm(symbols, desc="🔄 Symbols to bits"):
        for bit_pos in reversed(range(bits_per_symbol)):
            bits.append((sym >> bit_pos) & 1)
    return bits

def bits_to_bytes(bits):
    bytes_out = []
    for i in tqdm(range(0, len(bits), 8), desc="🔁 Bits to bytes"):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits += [0] * (8 - len(byte_bits))
        byte = 0
        for bit in byte_bits:
            byte = (byte << 1) | bit
        bytes_out.append(byte)
    return bytes(bytes_out)

def decode_metadata_and_data(data):
    # first two bytes = metadata size
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

    input_wav = filedialog.askopenfilename(title="📁 Select the encoded WAV file to decode", filetypes=[("WAV files", "*.wav")])
    if not input_wav:
        print("No file selected. Exiting.")
        sys.exit(0)

    print(f"📥 Reading WAV file: {{input_wav}}")
    audio, sr = sf.read(input_wav)
    if sr != fs:
        print(f"⚠️ Sample rate mismatch! Expected {{fs}}, got {{sr}}")

    symbols = decode_audio_to_symbols(audio, fs, symbol_duration, frequencies)
    bits = symbols_to_bits(symbols, bits_per_symbol)
    byte_data = bits_to_bytes(bits)

    try:
        metadata, file_data = decode_metadata_and_data(byte_data)
        filename = metadata.decode("utf-8")
        print(f"ℹ️ Original filename: {{filename}}")
    except Exception as e:
        print(f"⚠️ Error decoding metadata: {{e}}")
        filename = "decoded_input.bin"
        file_data = byte_data

    output_path = filedialog.asksaveasfilename(title="💾 Choose output file location and name", initialfile=filename)
    if not output_path:
        print("No output file selected. Exiting.")
        sys.exit(0)

    print(f"💾 Saving decoded file to: {{output_path}}")
    with open(output_path, "wb") as f:
        f.write(file_data)

    print("✅ Decoding complete!")
    input("Press Enter to exit...")
'''

def main():
    # Write the encoder
    with open("generated_encoder.py", "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(ENCODER_TEMPLATE))

    # Write the decoder
    with open("generated_decoder.py", "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(DECODER_TEMPLATE))

    print("✅ Generated 'generated_encoder.py' and 'generated_decoder.py' with fresh random frequencies.")
    print("Run 'generated_encoder.py' to encode files, and 'generated_decoder.py' to decode them.")

if __name__ == "__main__":
    main()
