#Skeleton for assembling MIDI

#Read in MIDI file
notes = [80,50]

channels = [0,1,2]

outputClip = []

for channel in channels:
    #Read in sound file
    sound = read("hi")
    
    #analyze sound for pitch
    pitch = findPitch(sound)

    #Create pydub clip
    soundClip = []

    for note in notes:
        #Get length of note
        #noteDur = note #in seconds

        #Adjust audio file to size of note
        #Note: Will this change pitch of sound??

        #Adjust audio to correct pitch
        newSound = shiftup(newSound,20)

        soundClip+=newSound

    #overlay that sound clip with all others
    outputClip.overlay(soundClip)

#Write the sound to file
write(outputClip,"out.wav")

