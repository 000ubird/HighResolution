'''
@author: BP12084
'''
import numpy as np
import wave
import pylab as pl
import audioread as ar

#ファイル名
wavName = "../wav/sample_44100_16bit_000.wav"
csvName = "../result_hi.csv"

#サンプル数と開始フレーム
sampleNum = 4000
beginFlame = 0
endFlame = beginFlame + sampleNum

#取得する振幅値の数
N = 20

#参考: http://wrist.hatenablog.com/entry/2013/08/06/015240
def pcm2float(short_ndary):
    float_ndary = np.array(short_ndary, dtype=np.float64)
    return np.where(float_ndary > 0.0, float_ndary / 32767.0, float_ndary / 32768.0)

#ファイル名を指定し、wavファイルのサンプリング周波数と振幅値を連想配列で返す
def read_wav_cd(wavName) :
    wav_bary = bytearray()
    
    with ar.audio_open(wavName) as f:
        print("ch: {0}, fs: {1}, duration [s]: {2}".format(f.channels, f.samplerate, f.duration))
        # "block_samples"で指定されたチャンクサイズずつ処理する(デフォルト1024)
        for buf in f:
            wav_bary.extend(buf)
    
    wav_ary = np.frombuffer(wav_bary, dtype=np.int16)  # 常時16bitで読み込まれる
    wav_l = wav_ary[0::2]
    wav_r = wav_ary[1::2]
    
    print(wav_l.shape)
    print(wav_r.shape)
    
    # shortをfloat64に変換
    wav_float_l = pcm2float(wav_l)
    wav_float_r = pcm2float(wav_r)
    
    #読み込んだ波形の一部を描画
    pl.plot(wav_float_l[beginFlame:1000])
    pl.show()
    
    return {"amp_l":wav_float_l, "amp_r":wav_float_r}

#指定したフレーム数分だけ振幅値をCSVで出力する
def makeAmpCSV(wavData,csvName):
    amps = [[]] #2次元配列の動的確保
    result = ""
    
    #指定したフレーム部分内の振幅値を取得
    for i in range(beginFlame,endFlame) : 
        #numAmp分だけ振幅値を抽出
        for j in range(i,i+N) : 
            amps.append(wavData[j])
            result += repr(wavData[j])+','
        result += '\n'
    
    #CSVファイルに格納
    try : 
        f = open(csvName,'w')
        f.write(result)
        f.close()
        print("CSVファイルを出力しました。")
    except : 
        print("CSVファイルの出力中にエラーが発生しました。")
        exit()
    
    return amps

if __name__ == '__main__':
    #WAVデータの読み込み
    wav_data = read_wav_cd(wavName)
    
    #CSVファイルの出力
    makeAmpCSV(wav_data['amp_l'], csvName)
