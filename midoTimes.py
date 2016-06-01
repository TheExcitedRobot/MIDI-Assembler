from mido import MidiFile

#Goal: convert from ticks to seconds
from mido import MetaMessage
import mido

#find tempo of song and encode into that song
#   tempo is in microseconds per beat
#   Side effect: cache that tempo for later
def findTempo(midiSong):
    if hasattr(midiSong,'tempo'):
        return midiSong.tempo
    for i,track in enumerate(midiSong.tracks):
        for message in track:
            if message.type == 'set_tempo':
                midiSong.tempo = message.tempo
                return message.tempo
    defaultTempo = 500000
    midiSong.tempo = defaultTempo
    return defaultTempo #apparently the default


#converts some number of ticks to some fraction of a second
def ticksToSeconds(ticks,song):
    #math - first ratio is % of beat the number of given ticks is
    #       second ratio is % of second each beat is (given 1 million microseconds in one second)
    tempo = findTempo(song)
    mil = 1000000.0
    return float(ticks)/float(song.ticks_per_beat) * float(tempo) / mil


def testFindTempo():
    tempo = findTempo(mid)
    print "how long 240 ticks",ticksToSeconds(240,mid)
    print "tempo (microseconds per beat?)",tempo
    print "bpm ",mido.tempo2bpm(tempo)
    print "ticks per beat", mid.ticks_per_beat
    print "total seconds",mid.length


def printAllSongMessages():
    for i,track in enumerate(mid.tracks):
        print 'track',i,':',track.name
        for message in track:
            print message



