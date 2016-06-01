# MIDI-Assembler
Converts MIDI instructions to music based on provided sound files


## Project Required Packages
MIDO, for reading MIDI objects
https://github.com/olemb/mido

A cool article about pitch shifting
http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/

Bregman, for doing FFR and finding the pitch
http://digitalmusics.dartmouth.edu/~mcasey/bregman/

Pydub, for stitching audio files together, shortening/lengthening them
https://github.com/jiaaro/pydub

NumPy/SciPy, for lots of operations
https://www.scipy.org/

## Other Packages of Interest
http://scikits.appspot.com/audiolab

http://arrowtheory.com/software/hypersonic/index.html

### Python Music Packages
https://wiki.python.org/moin/PythonInMusic

## General Process ideas
1. read in different sound clips
2. get pitches for each sound clips
3. read in MIDI, with pitch & duration of each pitch
4. combine sounds, shifted into MIDI pattern
5. export sound


