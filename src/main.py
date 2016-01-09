from makeAmpCSV import makeAmpArrayHi
from makeAmpCSV import makeAmpArrayCD
from makeAmpCSV import read_wav_cd
from makeGMM import makeGMM,debug_gmm
from convert import convert
from sklearn.externals import joblib

import math
import sys, time
import numpy as np
import matplotlib.pyplot as plt
import wavio

#学習に使う音声ファイル名
WAV_NAME_GMM = "../wav/sample_96000_24bit_001.wav"

#抽出するフレーム数
BEGIN_FLAME = 0  #固定
END_FLAME = 380000
#GMMの混合数
components = 30

'''
#学習処理
print("学習に使用する音声ファイルを読み込んでいます。")
wav_data_hi = read_wav_cd(WAV_NAME_GMM,BEGIN_FLAME,END_FLAME)
print("音声ファイルを読み込みました。\n")

print("1つ目の学習用データを作成しています。")
cd = makeAmpArrayCD(wav_data_hi['amp_l'], BEGIN_FLAME, END_FLAME)    #変換元
print("2つ目の学習用データを作成しています。")
hi = makeAmpArrayHi(wav_data_hi['amp_l'], BEGIN_FLAME, END_FLAME)    #変換先

print("2つの学習用データを結合しています。")
sample = np.hstack((cd,hi))
print("学習データが生成されました。サンプル数は",int(END_FLAME/20),"個です。\n")

print("学習を実行します。")
gmm = makeGMM(components,sample)
#debug_gmm(gmm)
print("学習が完了しました。\n")
'''

#高階調化処理
wav = read_wav_cd("../wav/sample_96000_24bit_000.wav",BEGIN_FLAME,END_FLAME)
print("変換する振幅データを読み込んでいます。")
cdAmp = makeAmpArrayCD(wav['amp_l'], BEGIN_FLAME, END_FLAME)
print("正解振幅データを作成しています。")   #正解を見たい時のオプション
#originAmp = makeAmpArrayHi(wav['amp_l'], BEGIN_FLAME, END_FLAME)

#変換のみ実行する場合はコメントを外す
gmm = joblib.load("gmm")    #GMMファイルの読み込み

print("変換を実行します。")
result = []
currentP = 0
for i in range(0,len(cdAmp)) : 
    convFlame = convert([cdAmp[i]], gmm, components)
    result.extend(convFlame * 16777216.0)   #24bitに変換
    
    #進行度合いの表示
    nextP = math.floor(i/len(cdAmp)*100)
    if nextP > currentP : 
        sys.stdout.write("\r%s" % str(nextP)+"% ")
        sys.stdout.flush()
        time.sleep(0.01)
    currentP = nextP
sys.stdout.write("\r%s" % str(100)+"% ")

b = []
for j in cdAmp : 
    b.extend(j)
    
c = []
#for j in originAmp : 
#    c.extend(j)
print("\n変換が終わりました。\n")

wavio.writewav24("sample.wav", 96000, result)

#波形の表示
fl1 = 0
fl2 = len(cdAmp)
plt.plot(b[fl1:fl2], label = "CD")
plt.plot(result[fl1:fl2], label = "Result")
#plt.plot(c[fl1:fl2], label = "Correct")
plt.legend()
plt.title("Result")
plt.xlabel("Time [t]")
plt.ylabel("Amplitude")
plt.show()
