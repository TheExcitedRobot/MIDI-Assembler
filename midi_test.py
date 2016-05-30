import midi
pattern = midi.read_midifile("inMidi.mid")
#print pattern

for i in xrange(0,len(pattern)):
    print "midi",i,":",pattern[i]
    for j in xrange(0,len(pattern[i])):
        print "inner",j,":",pattern[i][j]
        print "tick",j,":",pattern[i][j].tick
        print "notes",j,":",pattern[i][j].data

