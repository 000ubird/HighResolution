#coding:utf-8
import struct
import wave
import numpy as np
import scipy.signal
from pylab import *

"""SciPyのFIRフィルタ関数を使うサンプル"""

def fft(b, y, fs):
    """フィルタ係数bとフィルタされた信号yのFFTを求める"""
    b = list(b)
    y = list(y)

    N = 512    # FFTのサンプル数

    # 最低でもN点ないとFFTできないので0.0を追加
    for i in range(N):
        b.append(0.0)
        y.append(0.0)

    # フィルタ係数のFFT
    B = np.fft.fft(b[0:N])
    freqList = np.fft.fftfreq(N, d=1.0/fs)
    spectrum = [int(np.sqrt(c.real ** 2 + c.imag ** 2)) for c in B]

    # フィルタ係数の波形領域
    subplot(221)
    plot(range(0, N), b[0:N])
    axis([0, N, -0.5, 0.5])
    xlabel("time [sample]")
    ylabel("amplitude")

    # フィルタ係数の周波数領域
    subplot(223)
    n = len(freqList) / 2
    plot(freqList[:n], spectrum[:n], linestyle='-')
    axis([0, fs/2, 0, 1.2])
    xlabel("frequency [Hz]")
    ylabel("spectrum")

    # フィルタされた波形のFFT
    Y = np.fft.fft(y[0:N])
    freqList = int(np.fft.fftfreq(N, d=1.0/fs))
    spectrum = [int(np.sqrt(c.real ** 2 + c.imag ** 2)) for c in Y]
    
    print(freqList)
    
    # 波形を描画
    subplot(222)
    plot(range(0, N), y[0:N])
    axis([0, N, -1.0, 1.0])
    xlabel("time [sample]")
    ylabel("amplitude")

    # 振幅スペクトルを描画
    subplot(224)
    n = len(freqList) / 2
    plot(freqList[:n], spectrum[:n], linestyle='-')
    axis([0, fs/2, 0, 10])
    xlabel("frequency [Hz]")
    ylabel("spectrum")

    show()

def save(data, fs, bit, filename):
    """波形データをWAVEファイルへ出力"""
    wf = wave.open(filename, "w")
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(41000)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
    wf = wave.open("sample.wav", "r")
    fs = wf.getframerate()

    x = wf.readframes(wf.getnframes())
    x = frombuffer(x, dtype="int16") / 32768.0

    nyq = fs / 2.0  # ナイキスト周波数

    # フィルタの設計
    # ナイキスト周波数が1になるように正規化
    fe1 = 50.0 / nyq      # カットオフ周波数1
    fe2 = 3000.0 / nyq      # カットオフ周波数2
    numtaps = 255           # フィルタ係数（タップ）の数（要奇数）

    b = scipy.signal.firwin(numtaps, fe1)                         # Low-pass
    #b = scipy.signal.firwin(numtaps, fe2, pass_zero=False)        # High-pass
#    b = scipy.signal.firwin(numtaps, [fe1, fe2], pass_zero=False) # Band-pass
#    b = scipy.signal.firwin(numtaps, [fe1, fe2])                  # Band-stop

    # FIRフィルタをかける
    y = scipy.signal.lfilter(b, 1, x)

    # フィルタ係数とフィルタされた信号のFFTを見る
    fft(b, y, fs)

    # 音声バイナリに戻して保存
    y = [int(v * 32767.0) for v in y]
    y = struct.pack("h" * len(y), *y)
    save(y, fs, 16, "sine2.wav")