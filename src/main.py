from makeAmpCSV import makeAmpArrayHi
from makeAmpCSV import makeAmpArrayCD
from makeAmpCSV import read_wav_cd
from makeGMM import makeGMM,debug_gmm
from convert import convertAmp
from sklearn.externals import joblib
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
wav = read_wav_cd("../wav/sample_96000_24bit_001.wav",BEGIN_FLAME,END_FLAME)
print("変換する振幅データを読み込みます。")
cdAmp_l = makeAmpArrayCD(wav['amp_l'], BEGIN_FLAME, END_FLAME)  #Lチャネル
#cdAmp_r = makeAmpArrayCD(wav['amp_r'], BEGIN_FLAME, END_FLAME)  #Rチャネル

#print("正解振幅データを作成しています。")   #正解を見たい時のオプション
#originAmp = makeAmpArrayHi(wav['amp_l'], BEGIN_FLAME, END_FLAME)

#変換のみ実行する場合はコメントを外す
gmm = joblib.load("gmm")    #GMMファイルの読み込み

print("Lチャネルを変換しています。")
result_l = convertAmp(gmm, cdAmp_l, components)
'''
print("Rチャネルを変換しています。")
result_r = convertAmp(gmm, cdAmp_r, components)
#変換元
#b = []
#for j in cdAmp : b.extend(j * 5000000.0)

#c = []
#for j in originAmp : c.extend(j)


result = [0] * (len(cdAmp_l)*2)
j = 0
for i in range(0,len(result)-1,2) : 
    result[i] = result_l[j]
    result[i+1] = result_r[j]
    j+=1
#print(result)
'''

print("\n変換が終了しました。\n")

#波形の表示
fl1 = 0
fl2 = len(cdAmp_l)
#plt.plot(b[fl1:fl2], label = "CD")
plt.plot(result_l[fl1:fl2], label = "Result")
#plt.plot(c[fl1:fl2], label = "Correct")
plt.legend()
plt.title("Result")
plt.xlabel("Time [t]")
plt.ylabel("Amplitude")
plt.show()

#結果をwavファイルに書き込み
wavio.writewav24("out.wav", 96000, result_l)
