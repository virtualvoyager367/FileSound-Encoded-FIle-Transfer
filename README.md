# **FileSound**
Encrypts Files by converting them into sounds that uses different Frequencies for each generated pair of an encoder and decoder.

# **Things to Know**
**This is in being Active Worked on so dont expect it to be Perfectly Smooth.**

**THIS IS NOT A VIRUS, I converted the python generator script to an executable
and now it's having false positives.**

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

**Step 3: Run the Encoder and select the file, it will then convert it into a .wav audio file and say the path its stored at**

**Step 4: send the wav to a friend or someone else, also send the decoder in a more secure way like a USB drive if
you can**

**Step 5: As the receiver open the Decoder and select the .wav file that you were sent or given, it will let you choose where
to save it to once it finishes converting.**
