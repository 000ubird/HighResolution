import wave
import numpy as np
from pylab import *
from libs.audio.read import read_wav_cd

#ファイル名を指定してFFTを表示する
def fft(fileName) : 
    data = read_wav_cd(fileName)
    wav_data = data["data"]
    fs = data["fs"]
    
    start = 0
    N = 5000
    
    #numpyを使用したFFT
    fft_data = np.fft.fft(wav_data[start:start+N])
    freq_data= np.fft.fftfreq(N, d=1/fs)
    
    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft_data]  # 振幅スペクトル
    phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in fft_data]    # 位相スペクトル
    
    #波形を描画
    subplot(311)
    plot(range(start, start+N), wav_data[start:start+N])
    axis([start,start+N, -1.0, 1.0])
    xlabel("time [sample]")
    ylabel("amplitude")
    
    #振幅スペクトルを描画
    subplot(312)
    plot(freq_data, amplitudeSpectrum,marker='o', linestyle='-')
    axis([0,fs,0,50 ])
    xlabel("freq [Hz]")
    ylabel("amp")

    # 位相スペクトルを描画
    subplot(313)
    plot(freq_data, phaseSpectrum, marker= 'o', linestyle='-')
    axis([0, fs/2, -np.pi, np.pi])
    xlabel("freq [Hz]")
    ylabel("phase spectrum")
    
    show()
    
    print("complete")
