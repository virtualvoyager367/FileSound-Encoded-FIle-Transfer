# **FileSound**
Encodes Files by converting them into sounds that uses 64 different Frequencies for each generated pair of both an encoder and decoder.
It is Extremely unlikely to generate a specific set of frequencies twice since the **number of possible sets of combinations is 54 undecillion**
but if you want to know the exact number its **54,204,153,136,379,052,093,556,100,127,711,666,460,939,540,181,254,490,007,193,190,634,237,965,004,712,629,811,635,632,850**
possible sets of random frequencies.

# **Things to Know**
**The encoded WAV version will be approximately 500 times larger than the original file
for now, i will work on shrinking it. Keep in mind this is just a Proof-of-Concept for now.**

**The .py file in the repository is just meant for open-sourcing it, if you want to run it download the newest EXE version.
yes, the executable is safe, it's just the python script converted to an exe file.**

**This is in being Actively Worked on so dont expect it to be Perfectly Smooth.**

**This may appear to be a virus to any anti-virus, this happens with the Exe since I converted the
python generator script to an executable and now it's having false positives.**

# **How it works**

FileSound has a generator that generates an encoder and decoder, and it generates **64** different sounds frequencies 
that the encoder and decoder uses to encode and decode the file.
When it Encodes a file it converts the file into bits and then converts it into symbols, 
which is then converted into a WAV audio file that is on a spectrum people can hear, when the WAV audio file is
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

**Step 5: As the receiver open the Decoder and select the .wav file that you were sent or given, it will let you choose where
to save it to once it finishes converting.**
