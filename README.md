# MIDI-Assembler
Converts MIDI instructions to music based on provided sound files


## Project Required Packages
MIDO, for reading MIDI objects
https://github.com/olemb/mido

Python Pitch Shifting:
http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/

Bregman, for FFT and pitch identification:
http://digitalmusics.dartmouth.edu/~mcasey/bregman/

Pydub, for stitching audio files together and adjusting duration:
https://github.com/jiaaro/pydub

NumPy/SciPy, for lots of operations:
https://www.scipy.org/

## Other Packages of Interest
http://scikits.appspot.com/audiolab

http://arrowtheory.com/software/hypersonic/index.html

### Python Music Packages
https://wiki.python.org/moin/PythonInMusic

## General Process ideas
1. Read in sound clips for specific tracks
2. Find the pitch for each sound clip
3. Read in MIDI file, with pitch & duration instructions for each pitch
4. Modify sounds to fit MIDI instructions for duration and pitch
5. Combine modified sounds, into MIDI pattern
6. Export song

## Future Work
This project could be continued and improved upon through better sound characterization and collection. Different MIDI files required many tests to find the right sounds. These sounds required pitches and durations that sound good with the duration and pitch changes applied throughout the song. Further work in analyzing the MIDI piece to suggest sounds or give feedback on the right sounds to provide could improve the final output of the songs. 

Additional work could also provide better insight into the use of multi pitch sounds. For this project, the program assigns each sound a pitch based on a normal distribution applied to a fourier transform. Sounds that span multiple pitches are represented by a single pitch, and may not fit into the piece. Better scanning and characterization of the input pitch could use these multi-pitch sounds by identifying the pitches in the sound. This give options for cutting up the sound or shifting the pitches within the sound. Work must be done to keep the sound as natural as possible, but would allow for a greater range of sounds to be used. 

