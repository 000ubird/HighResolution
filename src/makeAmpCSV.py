'''
@author: BP12084
'''
import numpy as np
import wave

#ファイル名
wavName = "../wav/sample_96000_24bit_000.wav"
csvName = "../result_hi.csv"

#サンプル数と開始フレーム
sampleNum = 1000
beginFlame = 1000
endFlame = beginFlame + sampleNum

#取得する振幅値の数
N = 20

#ファイル名を指定し、wavファイルのサンプリング周波数と振幅値を連想配列で返す
def read_wav_cd(wavName) :
    print("Reading "+wavName)
    
    #指定したファイルが見つからなかった時の処理
    try :
        wf = wave.open(wavName, "r")
    except FileNotFoundError :
        print ("ファイル "+wavName+" が見つかりません")
        exit()
        
    fs = wf.getframerate()  #サンプリング周波数
    nflame = wf.getnframes() #フレーム数
    data = wf.readframes(wf.getnframes())
    
    #int型に変換
    data = np.frombuffer(data, dtype="int16") / 32768.0
    wf.close()
    
    return {"data":data, "fs":fs, "nflame":nflame}

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
    makeAmpCSV(wav_data['data'][0::2], csvName)

