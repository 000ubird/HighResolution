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
WAV_NAME_GMM = "../wav/Moanin.wav"

#抽出するフレーム数
BEGIN_FLAME = 0  #固定
END_FLAME = 380000

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

print("学習を実行します。混合数=50")
gmm1 = makeGMM(50,sample,"gmm_jazz_50")
print("学習を実行します。混合数=100")
gmm2 = makeGMM(100,sample,"gmm_jazz_100")   #100以降はメモリエラーが発生する場合あり
'''

#高階調化処理
wav = read_wav_cd("../wav/Moanin.wav",BEGIN_FLAME,END_FLAME)

print("変換する振幅データを読み込みます。")
cdAmp_l = makeAmpArrayCD(wav['amp_l'], BEGIN_FLAME, END_FLAME)  #Lチャネル
#cdAmp_r = makeAmpArrayCD(wav['amp_r'], BEGIN_FLAME, END_FLAME)  #Rチャネル

#変換前
inputArray = []
for j in cdAmp_l : inputArray.extend(j * 5000000.0)

#print("正解振幅データを作成しています。")   #正解を見たい時のオプション
originAmp = makeAmpArrayHi(wav['amp_l'], BEGIN_FLAME, END_FLAME)
origin = []
for j in originAmp : origin.extend(j * 5000000.0)

gmm = joblib.load("gmm_jazz_50")    #GMMファイルの読み込み
debug_gmm(gmm)

print("Lチャネルを変換しています。")
result_l = convertAmp(gmm, cdAmp_l, 50)
#print("Rチャネルを変換しています。")
#result_r = convertAmp(gmm, cdAmp_r, components)
print("\n変換が終了しました。\n")

#波形の表示
fl1 = 100000
fl2 = 150000
plt.plot(inputArray[fl1:fl2], label = "CD")     #入力波形
plt.plot(result_l[fl1:fl2], label = "Result")   #出力波形
plt.plot(origin[fl1:fl2], label = "Origin")     #正解波形
plt.legend()
plt.title("Result")
plt.xlabel("Time [t]")
plt.ylabel("Amplitude")
plt.show()

#結果をwavファイルに書き込み
wavio.writewav24("result.wav", 96000, result_l)