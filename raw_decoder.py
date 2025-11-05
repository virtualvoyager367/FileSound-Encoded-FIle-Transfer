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
frequencies = [1154, 1187, 1207, 1232, 1309, 1533, 1587, 1676, 1940, 1987, 2062, 2103, 2153, 2257, 2307, 2403, 3010, 3052, 3055, 3244, 3246, 3342, 3416, 3528, 3559, 3668, 3772, 3777, 3857, 3910, 4098, 4220, 4304, 4448, 4521, 4543, 4672, 4681, 4786, 4800, 4899, 5043, 5157, 5281, 5722, 5745, 5753, 5857, 5969, 6047, 6198, 6282, 6662, 6793, 6874, 7008, 7009, 7172, 7367, 7626, 7725, 7763, 7847, 7980]

t_samples = int(fs * symbol_duration)
t = np.linspace(0, symbol_duration, t_samples, endpoint=False)
base_waves = np.array([
    np.sin(2 * np.pi * f * t)
    for f in frequencies
])

def decode_audio_to_symbols_streaming(input_wav, frequencies):
    symbols = []
    with sf.SoundFile(input_wav) as wavfile:
        total_frames = wavfile.frames
        total_symbols = total_frames // t_samples
        print(f"🎧 Decoding {total_symbols} symbols...")
        for _ in tqdm(range(total_symbols), desc="📡 Matching tones"):
            segment = wavfile.read(frames=t_samples, dtype='float32')
            if len(segment) < t_samples:
                break
            correlations = np.dot(base_waves, segment)
            symbols.append(int(np.argmax(correlations)))
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

    input_wav = filedialog.askopenfilename(title="📁 Select the encoded WAV to inspect", filetypes=[("WAV files", "*.wav")])
    if not input_wav:
        print("No file selected. Exiting.")
        sys.exit(0)

    symbols = decode_audio_to_symbols_streaming(input_wav, frequencies)
    bits = symbols_to_bits(symbols, bits_per_symbol)
    byte_data = bits_to_bytes(bits)

    try:
        metadata, file_data = decode_metadata_and_data(byte_data)
        print("\n🔍 Metadata Found:")
        print(f"  Size (bytes): {len(metadata)}")
        print(f"  Raw Metadata (UTF-8): {metadata.decode('utf-8', errors='replace')}")
    except Exception as e:
        print(f"\n⚠️ Metadata extraction error: {e}")
        metadata = b""
        file_data = byte_data

    # Write the full dump to a text file
    dump_path = os.path.splitext(input_wav)[0] + "_rawdump.txt"
    print(f"\n💾 Writing full raw data dump to: {dump_path}")

    hex_dump = file_data.hex(' ')
    with open(dump_path, "w", encoding="utf-8") as f:
        f.write(hex_dump)

    print(f"✅ Dump complete! ({len(file_data)} bytes written to file)")
    input("Press Enter to exit...")