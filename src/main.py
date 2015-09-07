from libs.fft.fft import fft
from libs.audio.create import createSineWave2
from libs.audio.wavio import writewav24

fileName = "../wav/sinwave.wav"

fft(fileName)

#sin波の書き出しと合成のテスト
createSineWave2(96000, 3, 440, "3.wav")
a = createSineWave2(44100, 2, 1000, "1000.wav")
b = createSineWave2(44100, 2, 440, "440.wav")
writewav24("test.wav",44100,a+b)
