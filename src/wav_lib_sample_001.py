#http://docs.python.jp/2/library/wave.html

import wave
import math
import numpy
import pylab
from scipy import fromstring, int16

#使用するwavファイル
wavFile = "../wav/sample.wav"

#WaveReadオブジェクトを取得
wr = wave.open(wavFile, "rb")

#読み込んだwavファイル名
print("ファイル ->",wavFile,"\n")
#オーディオチャンネル数の取得
print("オーディオチャンネル数 -> ",wr.getnchannels())
#サンプル幅を取得 バイト数で返す
print("サンプル幅 -> ",wr.getsampwidth()," (8倍するとbit深度になる)")
#サンプリングレートの取得
print("サンプリングレート -> ",wr.getframerate())
#オーディオフレーム数の取得
print("オーディオフレーム数 -> ",wr.getnframes(),"(サンプリングレート×秒数)")
#再生時間は総フレーム数÷サンプリングレートで求まる。
print("再生時間 -> ",wr.getnframes() / wr.getframerate(),"[s]")
#圧縮形式の取得
print("圧縮形式 -> ",wr.getcomptype())
#圧縮形式の判読可能な文字列の取得
print("圧縮形式名 -> ",wr.getcompname())
#チャンネル数・サンプル幅・サンプリングレート・フレーム数・圧縮形式・圧縮形式名のタプルを取得
print("上記の情報をまとめたタプル -> ",wr.getparams(),"\n")

#ポインタを指定した位置に設定
wr.setpos(20)
#ポインタを先頭に戻す
wr.rewind()
#現在のファイルポインタの位置を返す
currentFrame = wr.tell()
#読み取りたい位置までのポインタ数
endFrame = 30000
#オーディオフレームの値を読み込んで、バイトごとに文字に変換した文字列を取得
#print(currentFrame,"から",endFrame,"までのフレーム\n",wr.readframes(endFrame))

#ポインタ数まで読み込み
data = wr.readframes(wr.getnframes())
#文字列から数値への変換
num_data = fromstring(data,dtype = int16)

#チャネル数が2→ステレオ
#数値列は左右左右・・・で入っている
if (wr.getnchannels() == 2):
    # 左チャンネルの抽出
    left = num_data[::2]
    left_abs = abs(num_data[::2])	#絶対値を取ったもの
    # 右チャンネル
    right = num_data[1::2]
    right_abs = abs(num_data[1::2])	#絶対値を取ったもの

#デバッグ
print("左チャネル : ",left)
print("右チャネル : ",right)


#WaveReadインスタンスを使用不可にする
wr.close()
