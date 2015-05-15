#http://docs.python.jp/2/library/wave.html

import wave

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
endFrame = 30
#オーディオフレームの値を読み込んで、バイトごとに文字に変換した文字列を取得
print(currentFrame,"から",endFrame,"までのフレーム\n",wr.readframes(endFrame))

#WaveReadインスタンスを使用不可にする
wr.close()
