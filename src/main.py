from libs.fft.fft import fft
from libs.audio.create import createSineWave2
from libs.audio.wavio import writewav24
from libs.audio.read import read_wav_cd

fileName = "../wav/sample.wav"

def getTest(wavData):
    array = []
    
    for i in range(1,len(wavData)) : 
        data1 = wavData[i-1]
        data2 = wavData[i]
        div = data2 - data1
        
        array.append(div)
        
    return array

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
writeText(wav_data['data'][0::2], '../amp.csv') #Lチャネルだけを抽出
writeText(getTest(wav_data['data'][0::2]), '../div.csv')
