from bregman.suite import Chromagram

audio_file = "whip_def.wav"
F = Chromagram(audio_file, nfft=16384, wfft=8192, nhop=2205)
print F.X
F.X[:,0]
