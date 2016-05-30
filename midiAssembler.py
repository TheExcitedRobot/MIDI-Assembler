import midoTimes
from midi_note import midi_from_file

#Skeleton for assembling MIDI

#Read in MIDI file
notes = [80,50]

channels = [0,1,2]

outputClip = []

for channel in channels:
    #Read in sound file
    channelFile = "filename here"
    sound = AudioSegment.from_wav(channelFile)

    #analyze sound for pitch
    pitch = midi_from_file(channelFile)

    #Create pydub clip
    soundClip = []

    for note in notes:

        newSound = sound.copy()

        #Get length of note
        #noteDur = note #in seconds

        inNote = # midi note
        inTicks = # midi note duration

        audioSize = ticksToSeconds(inTicks)
        audioSize = int(round(1000*audioSize)) # Seconds to miliseconds

        #Adjust audio file to size of note
        #Note: Will this change pitch of sound??
        newSound = newSound[:audioSize]

        #Adjust audio to correct pitch
        pitchCorrection = inNote - pitch
        newSound = shiftup(newSound,pitchCorrection)

        soundClip+=newSound

    #overlay that sound clip with all others
    outputClip.overlay(soundClip)

#Write the sound to file
write(outputClip,"out.wav")
