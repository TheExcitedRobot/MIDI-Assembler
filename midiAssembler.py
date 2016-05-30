#Skeleton for assembling MIDI
import mido

#Read in MIDI file
midiSong = mido.MidiFile('inMidi2.mid')

outputClip = []

#Loop through all the channels of the midi song
#Track 0 has meta data, but otherwise each channel seems to be on distinct track
for c in xrange(1,len(midiSong.tracks)):
    
    print "Converting channel ",c

    #MIDI notes have multiple parts per same note
    #ex, 20 ticks of 'down' beat, then 220 ticks of holding that note
    #Combine those together into one long section of 240 ticks
    #Also take out all the meta messages, just get notes
    track = midiSong.tracks[c]
    #print "track len before ",len(track)
    for i in reversed(xrange(0,len(track))):
        #print "msg[",i,"]:",track[i]
        if not hasattr(track[i],'velocity'):
            track.pop(i)
        elif track[i].velocity == 0:
            if i>0 and hasattr(track[i-1],'velocity') and track[i-1].velocity!=0:
                curMsg = track.pop(i)
                track[i-1].time += curMsg.time
    #print "track len after",len(track)

    #Read in sound file
    #sound = read("hi")
    
    #analyze sound for pitch
    #pitch = findPitch(sound)

    #Create pydub clip
    soundClip = []

    for midiMsg in track:
        #print "note time ",midiMsg.time
        #Get length of note
        #noteDur = note #in seconds

        #Adjust audio file to size of note
        #Note: Will this change pitch of sound??

        #Adjust audio to correct pitch
        #newSound = shiftup(newSound,20)

        #soundClip+=newSound

    #overlay that sound clip with all others
    #outputClip.overlay(soundClip)

#Write the sound to file
#write(outputClip,"out.wav")

