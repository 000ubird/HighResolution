from libs.audio.read import read_wav_cd

import pylab
import numpy as np

fileName = "../wav/sample_96000_24bit_000.wav"
csvFileName = "../result_hi.csv"

sampleNum = 100
minFlame = 1000
maxFlame = minFlame + sampleNum

def getDivAndAmps(wavData):
    divs = []
    amps = []
    
    #for i in range(1,len(wavData)-1) : 
    for i in range(minFlame,maxFlame) : 
        data1 = wavData[i-1]
        data2 = wavData[i+1]
        div = data2 - data1 #変化量の計算
        
        divs.append(div)    #現在の振幅値の前後の変化量
        amps.append(wavData[i])      #現在の振幅値
        
    return {"divs" : divs, "amps" : amps}

#10次元分の学習データを取得する
def getAmpGMM(wavData, numAmp,csvName):
    #振幅値を格納する二次元配列 → [フレーム数][11振幅]
    #amps = [ [0 for i in range(sampleNum)] for j in range (11)]
    amps = [[]] #動的確保
    x = []
    y = []
    
    #CSVファイルに格納
    f = open(csvName,'w')
    result = ""
    
    for i in range(minFlame,maxFlame) : 
        x.append(i)
        y.append(wavData[i])
        
        #11個分の振幅値を抽出
        for j in range(i,i+numAmp) : 
            amps.append(wavData[j])
            result += repr(wavData[j])+','
        result += '\n'
    
    f.write(result)
    f.close()
    
    
    pylab.plot(x,y)
    pylab.show()
    
    #5番目が補完する振幅値
    return amps

#CSVファイルに配列の要素を書き込み
def writeText(wavData,csvName):
    f = open(csvName,'w')
    result = ""
    
    for i in wavData : 
        result += repr(i)+',\n'
        
    f.write(result)
    f.close()


#WAVデータの読み込み

wav_data = read_wav_cd(fileName)
getAmpGMM(wav_data['data'][0::2], 21, csvFileName)

###
'''
#GMMの作成
results = getAmpGMM(wav_data['data'][0::2]) #Lチャンルの信号を抽出
f = open(csvFileName,'w')
str = ""
#for i in range(0,len(results['amps'])): 
for i in range(0,maxFlame-minFlame): 
    str += repr(results['amps'][i])+','+repr(results['divs'][i])+',\n'
    
f.write(str)
f.close()
'''
###