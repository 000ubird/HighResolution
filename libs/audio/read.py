import wave
import numpy

#ファイル名を指定し、wavファイルのサンプリング周波数とint型のデータを連想配列で返す
def read_wav_cd(fileName) :
    print("Reading "+fileName)
    
    #指定したファイルが見つからなかった時の処理
    try :
        wf = wave.open(fileName, "r")
    except FileNotFoundError :
        print ("ファイル "+fileName+" が見つかりません")
        exit()
        
    fs = wf.getframerate()  #サンプリング周波数
    N = wf.getnframes() #フレーム数
    data = wf.readframes(wf.getnframes())
    
    #int型に変換
    data = numpy.frombuffer(data, dtype="int16") / 32768.0
    wf.close()
    
    return {"data":data, "fs":fs, "N":N}
