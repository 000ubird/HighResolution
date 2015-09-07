import wave
import struct
from pylab import *
from libs.audio.wavio import writewav24

"""
振幅amp、基本周波数frq、サンプリング周波数 fs、
ビット深度depth(単位:byte)、長さlength秒の正弦波を作成して返す
"""
def createSineWave(amp, frq, fs, depth, length) : 
    data = []
    clip_hi = 1.0
    clip_lo = -1.0
    
    #正規化した波を整数値に変換する時の倍率
    mult_bit = 0
    if depth == 2 : mult_bit = 32767.0
    elif depth == 3 : mult_bit = 16777216.0
    else : exit() #16,24bit深度の時以外は終了
    
    for n in arange(length * fs) :
        s = amp * np.sin(2*np.pi * frq * n / fs)
       
        #クリッピング処理
        if s > clip_hi : s = clip_hi
        if s < clip_lo : s = clip_lo
        
        #書き込み
        data.append(s)
    
    #nBit深度の音源に変換
    data = [long(x * mult_bit) for x in data]
    #plot(data[0:1000]); show()
    
    #バイナリに変換
    data = struct.pack("l" * len(data), *data)
    
    return data

"""
"""
def createSineWave2(fs, depth, freq,filename) :
    bit = 0
    if depth == 2 :
        bit = 23
    elif depth == 3 :
        bit = 23
    else : exit()
    
    t = np.linspace(0, depth, depth*fs, endpoint=False)
    sig = np.sin(2 * np.pi * freq * t)
    data = (2**bit - 1)*sig
    writewav24(filename, fs, data)
    
    return data

"""
波形データをWAVEファイルへ出力
24ビット深度の時は正しく出力できない
"""
def save(data, fs, depth, filename):
    wf = wave.open(filename, "w")
    wf.setnchannels(2)  #2チャンネル
    wf.setsampwidth(depth)  #3にすると正しく出力できない
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()

#テスト
if __name__ == "__main__" :
    """
    #freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    freqList = [440]
    fs = 44100 
    depth = 2
    for f in freqList:
        data = createSineWave(1.0, f, fs, depth, 5.0)
    save(data,fs,depth,"test.wav")
    """
