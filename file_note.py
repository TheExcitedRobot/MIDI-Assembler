from __future__ import division
from scikits.audiolab import wavread
from numpy.fft import rfft, irfft
from numpy import argmax, sqrt, mean, diff, log
from matplotlib.mlab import find
from scipy.signal import blackmanharris, fftconvolve
from time import time
import sys
import math

from parabolic import parabolic

def freq_from_fft(sig, fs):
    """Estimate frequency from peak of FFT

    """
    # Compute Fourier transform of windowed signal
    windowed = sig * blackmanharris(len(sig))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f)) # Just use this for less-accurate, naive version
    true_i = parabolic(log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)


def midi_from_freq(freq):

    shift = 12*math.log((freq/440),2)
    shift = shift+69
    return shift


def midi_from_file(fileName):
    signal, fs, enc = wavread(fileName)

    # Compute Fourier transform of windowed signal
    windowed = signal * blackmanharris(len(signal))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f)) # Just use this for less-accurate, naive version
    true_i = parabolic(log(abs(f)), i)[0]

    # Convert to equivalent frequency
    freq = fs * true_i / len(windowed)

    shift = 12*math.log((freq/440),2)
    midiNum = shift+69

    return midiNum


#signal, fs, enc = wavread("meow1_shaggy.wav")
#frequency = freq_from_fft(signal, fs)
#midiNum =  midi_from_freq(frequency)
#print int(round(midiNum))
