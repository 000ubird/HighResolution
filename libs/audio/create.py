import wave
import struct
from pylab import *

"""
振幅amp、基本周波数frq、サンプリング周波数 fs、
ビット深度bit_depthbit、長さlength秒の正弦波を作成して返す
"""
def createSineWave(amp, frq, fs, bit_depth, length) : 
    data = []
    clip_hi = 1.0
    clip_lo = -1.0
    
    #正規化した波を整数値に変換する時の倍率
    mult_bit = 0
    if bit_depth == 16 : mult_bit = 32767.0
    elif bit_depth == 24 : mult_bit = 16777216.0
    else : exit() #16,24bit深度の時以外は終了
    
    for n in arange(length * fs) :
        s = amp * np.sin(2*np.pi * frq * n / fs)
       
        #クリッピング処理
        if s > clip_hi : s = clip_hi
        if s < clip_lo : s = clip_lo
        
        #書き込み
        data.append(s)
    
    #nBit深度の音源に変換
    data = [int(x * mult_bit) for x in data]
    #バイナリに変換
    data = struct.pack("h" * len(data), *data)
    
    return data

def save(data, fs, bit, filename):
    """波形データをWAVEファイルへ出力"""
    wf = wave.open(filename, "w")
    wf.setnchannels(2)
    wf.setsampwidth(bit)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()

if __name__ == "__main__" :
    #freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    freqList = [440]
    for f in freqList:
        data = createSineWave(1.0, f, 44100, 16, 5.0)
    #print(data)
    save(data,44100,2,"test.wav")
