import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile

"""
speedx, stretch, pitchshift 
From: http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
"""

def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( len(sound_array) /f + window_size)

    for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += np.asarray(hanning_window*a2_rephased,dtype=np.float64)

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

#from http://stackoverflow.com/questions/35735497/how-to-create-a-pydub-audiosegment-using-an-numpy-array
def convertSciToPyDub(channel,fps):
    audioSeg = AudioSegment(
        channel.tostring(),
        frame_rate = fps,
        sample_width=channel.dtype.itemsize,
        channels=1
    )
    return audioSeg

fps, bowl_sound = wavfile.read("whip_def.wav")
tones = range(-25,25)
#transposed = [pitchshift(bowl_sound, n) for n in tones]
newSound = bowl_sound#pitchshift(bowl_sound,20)

#wavfile.write('whip20.wav',fps,newSound)#transposed[20])

print "shape sound ",newSound.shape





soundClip = convertSciToPyDub(newSound,fps)
for tone in tones:
    #print "shifting by tone ",tone
    shiftedClip = pitchshift(bowl_sound,tone)
    soundClip = soundClip.append(convertSciToPyDub(shiftedClip,fps))

out_f = open("whippd.wav",'wb')
soundClip.export(out_f,format='wav')



