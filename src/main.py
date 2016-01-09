from makeAmpCSV import makeAmpArrayHi
from makeAmpCSV import makeAmpArrayCD
from makeAmpCSV import read_wav_cd
from makeGMM import makeGMM,debug_gmm
from convert import convert

import numpy as np
import pylab as pl

#学習に使うwavファイル名
WAV_NAME_GMM = "../wav/sample_96000_24bit_001.wav"

#抽出するフレーム数
BEGIN_FLAME = 0  #固定
END_FLAME = 300000 #10000000

#GMMの混合数
components = 30

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
debug_gmm(gmm)
print("学習が完了しました。\n")

#変換に使うサンプル
convertSample = cd[1000]    #ここで別のwavファイルなどを読み込む

print("変換を実行します。")
result_amp = convert([convertSample], gmm)
print("変換が終わりました。\n")

print("変換元 の振幅値: ",convertSample)
pl.plot(convertSample)
pl.show()
print("変換結果の振幅値 : ",result_amp)
pl.plot(result_amp)
pl.show()
print("正解の振幅値 : ",hi[1000])
pl.plot(hi[1000])
pl.show()
