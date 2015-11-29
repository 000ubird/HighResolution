from libs.fft.fft import fft
from libs.audio.create import createSineWave2
from libs.audio.wavio import writewav24
from libs.audio.read import read_wav_cd

fileName = "../wav/sample_96000_24bit_001.wav"

def getTest(wavData):
    array = []
    
    for i in wavData : 
        array.append(i)
    
    return array

#CSVファイルに配列の要素を書き込み
def writeText(wavData):
    f = open('../hi.csv','w')
    result = ""
    
    for i in wavData : 
        result += repr(i)+',\n'
        
    f.write(result)
    f.close()

#WAVデータの読み込み
wav_data = read_wav_cd(fileName)
writeText( wav_data['data'] )
