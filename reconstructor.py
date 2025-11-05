import tkinter as tk
from tkinter import filedialog
from binascii import unhexlify
import re
import os
import sys

def reconstruct_file():
    print("🔧 File Reconstructor")
    print("====================\n")

    output_filename = input("Enter output filename (e.g., output.pdf): ").strip()
    if not output_filename:
        print("❌ No filename provided. Exiting.")
        sys.exit(0)

    root = tk.Tk()
    root.withdraw()
    dump_path = filedialog.askopenfilename(
        title="📁 Select the hex dump .txt file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not dump_path:
        print("❌ No dump file selected. Exiting.")
        sys.exit(0)

    print(f"📄 Reading hex dump: {dump_path}")

    with open(dump_path, "r", encoding="utf-8", errors="ignore") as f:
        hex_text = f.read()

    hex_clean = re.sub(r'[^0-9A-Fa-f]', '', hex_text)

    if len(hex_clean) % 2 != 0:
        print("⚠️ Warning: Hex length is odd, padding with 0.")
        hex_clean += "0"

    try:
        binary_data = unhexlify(hex_clean)
    except Exception as e:
        print(f"❌ Error converting hex to binary: {e}")
        sys.exit(1)

    output_path = os.path.join(os.path.dirname(dump_path), output_filename)
    with open(output_path, "wb") as f:
        f.write(binary_data)

    size = os.path.getsize(output_path)
    print(f"\n✅ Successfully reconstructed: {output_path}")
    print(f"📏 File size: {size} bytes")

    header = binary_data[:8]
    print(f"🔍 First 8 bytes: {header.hex(' ')}")
    if binary_data.startswith(b'%PDF'):
        print("🧾 Detected: PDF file header.")
    elif binary_data.startswith(b'\x89PNG'):
        print("🖼️ Detected: PNG file header.")
    elif binary_data.startswith(b'PK'):
        print("📦 Detected: ZIP or DOCX file header.")
    elif binary_data.startswith(b'\xFF\xD8\xFF'):
        print("📸 Detected: JPEG file header.")
    else:
        print("ℹ️ Header type unknown (might be binary or custom format).")

    input("\nPress Enter to exit...")

if __name__ == "__main__":

    reconstruct_file()
