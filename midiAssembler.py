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
midiSong = mido.MidiFile('twelveBZ.mid')

outputClip = AudioSegment.silent(duration=.1)

#Pitch the sound
#and shorten its time -  time in milliseconds I think
def processNote(sound,pitchCorrection,time,frame_rate):
    if(pitchCorrection !=0):
        newSound = pitches.pitchshift(sound,pitchCorrection)
    else:
        newSound = sound
    
    #try stretching sound
    timeSound = len(newSound)/(frame_rate*1.0) #this is % of second
    timeSound *= 1000.0 #now in milliseconds
    if(timeSound<time):
        #print "sound is shorter by ",time-timeSound,"time: ",time,"timeSound: ",timeSound
    	speedFactor = (time)/timeSound
    	#newSound = pitches.stretch(newSound,speedFactor,2**13,2**11)#good defaults I think
    
    newSound = pitches.convertSciToPyDub(newSound,frame_rate)#sound.frame_rate)

    #Adjust audio file to size of note
    #Note: Will this change pitch of sound??
    newSound = newSound[:time]
    newSound = newSound.fade(to_gain=-120.0, end=audioSize, duration=audioSize/3)
    return newSound

def drumChannels():
    drumSound = {}
    drumFramerate = {}
    baseDir = "./drums/"
    pattern = re.compile(r"(^drum)(\d+)")
    for file in os.listdir(baseDir):
        regG = pattern.match(file)
        if (regG != None):
            channelFile = baseDir+regG.group(0)+".wav"
            index = int(regG.group(2))
            frame_rate, sound = wavfile.read(channelFile)
            drumSound[index] = sound
            drumFramerate[index] = frame_rate

    return drumSound, drumFramerate

#Return dictionary with times of each note (by moving deltaTime to previous Note)
#   useNoteOn0 - whether to count note_on msgs with velocity 0 as note_off msgs
def generateTimes(track,useNoteOn0=0):
    #set time for each note based on note_off signals
    allTimes = {}
    for i in reversed(xrange(0,len(track))):
        if(track[i].type=='note_off' or (useNoteOn0 and track[i].type=='note_on' and track[i].velocity==0)):
            startNote = track[i].note
            timeSoFar = track[i].time
            j = i-1
            while(j>0 and startNote!=track[j].note): 
                timeSoFar += track[j].time
                j -= 1
            #we found matching note (or are at bottom)
            allTimes[track[j]] = timeSoFar
    if(len(allTimes)==0 and len(track)>0):
        #jython MIDI seem to be formatted different/lazier. Convert note_on with velocity 0 into note_off commands, retry
        numConverted = 0
        for i in reversed(xrange(0,len(track))):
            if(track[i].type=='note_on' and track[i].velocity==0):
                #track[i].type = 'note_off'
                numConverted+=1
        if(numConverted>0):
            return generateTimes(track,1)
    return allTimes
    

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
	elif track[i].type == 'note_on' or track[i].type == 'note_off':
            allNotes[track[i]] = [track[i].note]
    #set time for each note based on note_off signals
    """
    allTimes = {}
    for i in reversed(xrange(0,len(track))):
        if(track[i].type=='note_off'):
            startNote = track[i].note
            timeSoFar = track[i].time
            j = i-1
            while(j>0 and startNote!=track[j].note): 
                timeSoFar += track[j].time
                j -= 1
            #we found matching note (or are at bottom)
            allTimes[track[j]] = timeSoFar
    """
    allTimes = generateTimes(track)
    #go through, clean out note_offs
    for i in reversed(xrange(0,len(track))):
        if(track[i].type=='note_off'):
            track.pop(i)
    #combine chords
    for i in reversed(xrange(0,len(track))):
        if track[i].velocity == 0 and track[i].time == 0:
            curMsg = track.pop(i)
	    #part of a chord, combine into one
            if i>0 and hasattr(track[i-1],'note'):
                #track[i-1].notes = track[i-1].note + curMsg.notes
                #setattr(track[i-1],'notes',track[i-1].notes+curMsg.notes)
                allNotes[track[i-1]] += allNotes[curMsg]
    #add in silence - TODO: this isn't quite correct
        #and set time to duration of note
    for i in reversed(xrange(0,len(track))):
        curTime = track[i].time
        if track[i] in allTimes:
            track[i].time = allTimes[track[i]]
            if(curTime!=0):
                track.insert(i,mido.Message('aftertouch',time=curTime,channel=track[i].channel))
            

    #print "track len after",len(track)

    #Read in sound file
    if(len(track)>0):
		curChannel = track[0].channel
		print "Current Channel =",curChannel
		if(curChannel != 9):
			channelFile = "./channels/channel"+str(curChannel)+".wav"
		
			#sound = AudioSegment.from_wav(channelFile)
		
			frame_rate, sound = wavfile.read(channelFile)
		
			#analyze sound for pitch
			pitch = midi_from_file(channelFile)
		
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
		
			inTicks = midiMsg.time # midi note duration
                        #if(inTicks<10):
                        #print "inkTicks too small",inTicks,"msg type: ",midiMsg.type
		
			audioSize = midoTimes.ticksToSeconds(inTicks,midiSong)
			audioSize = int(round(1000.0*audioSize)) # Seconds to miliseconds

                        if midiMsg.type=='aftertouch':
                            #just insert silence
                            soundClip += AudioSegment.silent(audioSize)		
                        else:

			    inNote = midiMsg.note # midi note
			
                            #Adjust audio to correct pitch
			    if (basePitch == -1 and curChannel != 9):
			    	pitchCorrection = inNote - pitch
				pitchCorrection = int(math.fmod(pitchCorrection, 12))
				basePitch = inNote - pitchCorrection + 12
		
			    #handle chords
			    chordSound = AudioSegment.silent(audioSize)
			    newSound = AudioSegment.silent(audioSize)
                            for n in allNotes[midiMsg]:
				if (curChannel != 9):
					pitchCorrection = n-basePitch
					newSound = processNote(sound,pitchCorrection,audioSize,frame_rate)
				else:
					if n in drumS:
						newSound = processNote(drumS[n], 0, audioSize, drumF[n])
                                                newSound = newSound.apply_gain(-5)
					else:
						print 'Percussion Instrument ', n,' has no provided sound, will skip'
		
			        chordSound = newSound.overlay(chordSound)
			    soundClip = soundClip + chordSound
		
		#overlay that sound clip with all others
		#    segment that is overlayed is truncated, so pick longer one as base
		if len(outputClip)>len(soundClip):
			outputClip = outputClip.overlay(soundClip)
		else:
			outputClip = soundClip.overlay(outputClip)

#Write the sound to file
out_f = open("outP.wav",'wb')
outputClip.export(out_f,format='wav')

