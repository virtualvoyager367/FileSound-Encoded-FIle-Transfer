# **FileSound**

Encodes Files by converting them into sounds that uses 64 different Frequencies for each generated pair of both an encoder and decoder.
It is Extremely unlikely to generate a specific set of frequencies twice since the number of possible sets of combinations is **Half a Centillion**
but if you want to know the exact number its **949781856816046480879985431476587946820182495951089363483256890911015256222585882604349706787457291376018831753840960425644298151199888739395272954815972793910300324236857799744382955464823610670298870754094336231329433470407922948634949183831090442621311803505990401585969721252930623763593366899946196776219851387259495211333742746717124946456942040377310872829863979174397809196031615797224562175862025381930071752325334644119867743204197977367504164451715750793505411356596563556591629737767476053503159816549284526226982195826834183855685843294891058467338337767102397944290297875517193312349441708674585447472977616273557990591804022947183656577725681247309666128246335713271590749495529281830009026133348184529776069134099467760305179794351787070517470853004359169485929684940626672008406966428049877480958085764379658156923540914776031627306582705213714846** possible sets of random frequencies.

# **Things to Know**

**DISCLAIMER:** Sometimes the decrypted file may have issues, if this happens regenerate the encoder and decoder and encode and decode the file again, at the bottom is a in depth explanation of why this could happen.

**The encoded WAV version is approximately 295 times larger than the original file, so stick to smaller files unless you have what you need to
convert larger files.**

**The .py file in the repository is just meant for open-sourcing it, if you want to run it download the newest EXE version.
yes, the executable is safe, it's just the python script converted to an exe file.**

**This is being Actively Worked on so dont expect it to be Perfectly Smooth.**

**This may trigger false positives from some anti-viruses, this happens with the Exe since I converted the
python generator script to an executable**

# **How it works**

FileSound has a generator that generates an encoder and decoder, and it generates **64** different sound frequencies 
that the encoder and decoder uses to encode and decode the file.
When it Encodes a file it converts the file into bits and then converts it into symbols, 
which is then converted into a WAV audio file that is within the audible range that people can hear, when the WAV audio file is
put into the decoder it uses those frequencies to convert the sound back into symbols, then to bits,
and then back into bytes which is then translated into the original file.
The encoder also encodes the file name and extension into the WAV file. The encoded metadata is then filtered out
of the conversion by the Decoder and then translated back into the name and extension,
which is used when saving the decoded file into a path.

# **How to Setup**

**Step 1: Download the Executable generator, this will generate your encoder and decoder
With a Unique set of Frequencies.**

**Step 2: Run the executable, it does NOT need administrative privileges, only try if you encounter problems.**

**Step 3: Run the Encoder and select the file, it will then convert it into a .wav audio file and say the path its stored
In on your Device.**

**Step 4: send the wav to a friend or someone else, also send the decoder in a more secure way like a USB drive if
you can.**

**Step 5: As the receiver open the Decoder and select the .wav file that you received, it will let you choose where
to save it to once it finishes converting.**

# **What went into the Process of making this.**

FileSound started as a fun project but became difficult over time as more features were being developed to make a new way to transfer files using audio. The idea was to encode any file into a sequence of audio tones and with each tone representing a chunk of bits and then decode it back perfectly without errors, making file transfer easily possible through just sound.
One of the biggest challenges was managing large files without exhausting system memory. Initially, encoding needed to load the entire file into RAM, which quickly became impractical for bigger files.

To fix this issue, I added streaming audio encoding and decoding, which processes files chunk-by-chunk. This means that the program reads a small piece of the file, encodes it into audio right as the pieces are generated, and then moves on to the next chunk. This way, memory usage stays low, and FileSound can encode and decode much larger files with almost no errors.

**Here’s a key snippet from the encoder showing this chunked approach:**


```python
def encode_chunk(chunk):
    bits = bytes_to_bits(chunk)
    symbols = bits_to_symbols(bits
    audio_signal = symbols_to_audio(symbols)
    sf.write(output_path, audio_signal, fs, subtype='PCM_16', append=True)  



with open(input_path, "rb") as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        encode_chunk(chunk)
```

This method uses the append=True flag in the soundfile.write function to write the audio data as it's generated to the output WAV file without loading everything into memory.
The result is a very efficient, scalable file-to-audio encoder and decoder that maintains perfect file fidelity, even for very large files. I’m excited to keep building onto this project with many more features coming over time.
The result is a very efficient, scalable file-to-audio encoder and decoder that maintains perfect file fidelity, even for very large files. I’m excited to keep building onto this foundation with new features like hardware integration and advanced encryption layers.

If you read the disclaimer, you will know what this is for. The reason why you may need to regenerate the python files is because sometimes when the frequencies are generated, they can be similar or close to other frequencies, causing overlap or misinterpretation, these lead the decoder to misinterpret the frequencies leading to the decoder getting incorrect output, which is why you need to regenerate the scripts as different frequency lists work better than others, the less similar the frequencies the lower the chances are of misinterpretation.
