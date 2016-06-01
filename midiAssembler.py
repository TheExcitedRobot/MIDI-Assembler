import midoTimes
from midi_note import midi_from_file
import pitchShifting as pitches
import math
import os
from pydub import AudioSegment
import re
from scipy.io import wavfile
#Skeleton for assembling MIDI
import mido

#Read in MIDI file
midiSong = mido.MidiFile('etherealGZ.mid')

outputClip = AudioSegment.silent(duration=.1)

#Pitch the sound
#and shorten its time
def processNote(sound,pitchCorrection,time):
    if(pitchCorrection !=0):
        newSound = pitches.pitchshift(sound,pitchCorrection)
    else:
        newSound = sound
    newSound = pitches.convertSciToPyDub(newSound,frame_rate)#sound.frame_rate)

    #Adjust audio file to size of note
    #Note: Will this change pitch of sound??
    newSound = newSound[:time]
    newSound = newSound.fade(to_gain=-120.0, end=audioSize, duration=audioSize/3)
    return newSound

def drumChannels():
    drumSound = {}
    drumFramerate = {}
    pattern = re.compile(r"(^drums)(\d+)")
    for file in os.listdir "/channels"
        regG = pattern.match(file)
        if (regG != None):
            channelFile = "./channels/"+regG.group(0)+".wav"
            index = int(regG.group(2))
            frame_rate, sound = wavfile.read(channelFile)
            drumSound[index] = sound
            drumSound[index] = frame_rate

    return drumSound, drumFramerate

#Loop through all the channels of the midi song
#Track 0 has meta data, but otherwise each channel seems to be on distinct track
for c in xrange(1,len(midiSong.tracks)):
    print "Converting channel ",c

    #MIDI notes have multiple parts per same note
    #ex, 20 ticks of 'down' beat, then 220 ticks of holding that note
    #Combine those together into one long section of 240 ticks
    #Also take out all the meta messages, just get notes
    track = midiSong.tracks[c]
    allNotes = {}
    #print "track len before ",len(track)
    for i in reversed(xrange(0,len(track))):
        #print "msg[",i,"]:",track[i]
        if not hasattr(track[i],'velocity'):
            track.pop(i)
	else:
            allNotes[track[i]] = [track[i].note]
            #track[i].note = [track[i].note]
    for i in reversed(xrange(0,len(track))):
        if track[i].time == 0:
	    #part of a chord, combine into one
            if i>0 and hasattr(track[i-1],'note'):
                curMsg = track.pop(i)
                #track[i-1].notes = track[i-1].note + curMsg.notes
                #setattr(track[i-1],'notes',track[i-1].notes+curMsg.notes)
                allNotes[track[i-1]] += allNotes[curMsg]
    for i in reversed(xrange(1,len(track))):
        if track[i].velocity == 0:
            #note being held down
            if i>0 and hasattr(track[i-1],'velocity') and track[i-1].velocity!=0:
                curMsg = track.pop(i)
                track[i-1].time += curMsg.time
    #print "track len after",len(track)

    #Read in sound file
    curChannel = track[0].channel
    print "Current Channel ="+curChannel
    if(curChannel != 9):
        channelFile = "./channels/channel"+str(c)+".wav"

        #sound = AudioSegment.from_wav(channelFile)

        frame_rate, sound = wavfile.read(channelFile)

        #analyze sound for pitch
        pitch = midi_from_file(channelFile) % 12

    else:
        drumS, drumF = drumChannels()
        pitch = 0
    #Create pydub clip
    soundClip = AudioSegment.silent(duration=.1)

    # Value for base pitch
    basePitch = -1

    for midiMsg in track:
        #print "note time ",midiMsg.time

        #Get length of note
        #noteDur = note #in seconds

        inNote = midiMsg.note # midi note
        inTicks = midiMsg.time # midi note duration

        audioSize = midoTimes.ticksToSeconds(inTicks,midiSong)
        audioSize = int(round(1000.0*audioSize)) # Seconds to miliseconds

        #Adjust audio to correct pitch
        if (basePitch == -1 && curChannel != 9):
            pitchCorrection = inNote - pitch
            pitchCorrection = int(math.fmod(pitchCorrection, 12))
            basePitch = inNote - pitchCorrection + 12

        #handle chords
        chordSound = AudioSegment.silent(2)
        for n in allNotes[midiMsg]:
            if (curChannel != 9):
                pitchCorrection = n-basePitch
                newSound = processNote(sound,pitchCorrection,audioSize)
            else:
                if n in drumS:
                    newSound = processNote(drumS[n], 0, audioSize)
                    chordSound = newSound.overlay(chordSound)
                else:
                    print 'Percussion Instrument ' + n + ' has no provided sound, will skip'

        soundClip = soundClip + chordSound

    #overlay that sound clip with all others
    #    segment that is overlayed is truncated, so pick longer one as base
    if len(outputClip)>len(soundClip):
    	outputClip = outputClip.overlay(soundClip)
    else:
        outputClip = soundClip.overlay(outputClip)

#Write the sound to file
out_f = open("cmidmeow.wav",'wb')
outputClip.export(out_f,format='wav')
