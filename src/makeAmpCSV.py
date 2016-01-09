import numpy as np
import audioread as ar
import math
import sys, time

#ファイル名
wavName_hi = "../wav/02-Are You Real.wav"
wavName_cd = "../wav/02-Are You Real_CD.wav"
csvName_hi = "../result_hi.csv"
csvName_cd = "../result_cd.csv"

#取得する振幅値の数
N = 20

#抽出するフレーム数
beginFlame = 0  #固定
endFlame = 1000000 #10000000

#参考: http://wrist.hatenablog.com/entry/2013/08/06/015240
def pcm2float(short_ndary):
    float_ndary = np.array(short_ndary, dtype=np.float64)
    return np.where(float_ndary > 0.0, float_ndary / 32767.0, float_ndary / 32768.0)

#ファイル名を指定し、wavファイルのサンプリング周波数と振幅値を連想配列で返す
def read_wav_cd(wavName,begin,end) :
    wav_bary = bytearray()
    
    with ar.audio_open(wavName) as f:
        if f.duration*f.samplerate < end-begin:
            print("サンプル数が音声信号の長さを超えています。")
            exit()
            
        print("ファイル名 : ",wavName,"\nチャネル数: {0}[channel] \nサンプリング周波数 : {1}[Hz]\nフレーム数 : {2}"
              .format(f.channels, f.samplerate, f.duration*f.samplerate))
        # "block_samples"で指定されたチャンクサイズずつ処理する(デフォルト1024)
        for buf in f:
            wav_bary.extend(buf)
    
    wav_ary = np.frombuffer(wav_bary, dtype=np.int16)  # 常時16bitで読み込まれる
    wav_l = wav_ary[0::2]
    wav_r = wav_ary[1::2]
    
    #print(wav_l.shape)
    #print(wav_r.shape)
    
    # shortをfloat64に変換
    wav_float_l = pcm2float(wav_l[begin:end]) #配列が大きいとメモリエラー
    wav_float_r = pcm2float(wav_r[begin:end])
    
    #読み込んだ波形の一部を描画
    #import pylab as pl
    #pl.plot(wav_float_l[beginFlame:endFlame])
    #pl.show()
    
    return {"amp_l":wav_float_l, "amp_r":wav_float_r}

#指定したフレーム数分だけ振幅値をCSVで出力する
def makeAmpCSV(wavData,csvName,begin,end):
    amps = [[]] #2次元配列の動的確保
    result = ""
    
    #指定したフレーム部分内の振幅値を取得
    i = begin
    while i < end :
        #numAmp分だけ振幅値を抽出
        for j in range(i,i+N) : 
            amps.append(wavData[j])
            
            #最後の列にはカンマを付けない
            if j == i+N-1 : 
                result += repr(wavData[j])
            else : 
                result += repr(wavData[j])+','
                
        result += '\n'
        i += N
        
    #CSVファイルに格納
    try : 
        f = open(csvName,'w')
        f.write(result)
        f.close()
    except : 
        print("CSVファイルの出力中にエラーが発生しました。")
        exit()
    
    return amps

#指定したフレーム数分だけ振幅値をCSVで出力する - CD用
def makeAmpCSV2(wavData,csvName,begin,end):
    result = ""
    
    #指定したフレーム部分内の振幅値を取得
    i = begin
    while i < end :         
        #numAmp分だけ振幅値を抽出
        for j in range(i,i+N,2) : 
                result += repr(wavData[j])+','
                result += repr(wavData[j])
                #最後の列にはカンマを付けない
                if j != i+N-2 : 
                    result += ','
                
        result += '\n'
        i += N
        
    #CSVファイルに格納
    try : 
        f = open(csvName,'w')
        f.write(result)
        f.close()
    except : 
        print("CSVファイルの出力中にエラーが発生しました。")
        exit()

def makeAmpArrayHi(wavData,begin,end) :
    #numpyのinsert用ダミーデータ
    dummy_data = np.zeros(N)
    array = np.array([dummy_data],dtype=float)
    tmp_array = np.array([],dtype=float) 
    
    #指定したフレーム部分内の振幅値を取得
    i = 1   #処理する先頭のフレーム数
    n = 1   #結果を保持する配列のインデックス
    m = 0   #N個分の振幅値を保持する配列のインデックス
    current = 0
    
    while i < end - N :
        #N個分の配列データを抽出
        for j in range(i,i+N) : 
            tmp_array = np.insert(tmp_array, m, wavData[j])
            m += 1
            
        #抽出したデータを追加    
        array = np.insert(array,n,tmp_array,axis=0)
        
        #各変数の初期化
        tmp_array = np.array([],dtype=float)
        i += N
        n += 1
        m =  0
        
        #進行度合いの表示
        nextP = math.floor(i/end*100)
        if nextP > current : 
            sys.stdout.write("\r%s" % str(nextP)+"% ")
            sys.stdout.flush()
            time.sleep(0.01)
        current = nextP
    
    sys.stdout.write("\r%s" % str(100)+"% ")
    print("\n作成完了\n")
    
    return array

def makeAmpArrayCD(wavData,begin,end) :
    #numpyのinsert用ダミーデータ
    dummy_data = np.zeros(N)
    array = np.array([dummy_data],dtype=float)
    tmp_array = np.array([],dtype=float) 
    
    #指定したフレーム部分内の振幅値を取得
    i = 1   #処理する先頭のフレーム数
    n = 1   #結果を保持する配列のインデックス
    m = 0   #N個分の振幅値を保持する配列のインデックス
    current = 0
    
    while i < end - N :
        #N個分の配列データを抽出
        for j in range(i,i+int(N/2)) : 
            tmp_array = np.insert(tmp_array, m, wavData[j])
            m += 1
            tmp_array = np.insert(tmp_array, m, wavData[j])
            m += 1
        
        #抽出したデータを追加    
        array = np.insert(array,n,tmp_array,axis=0)
        
        #各変数の初期化
        tmp_array = np.array([],dtype=float)
        i += N
        n += 1
        m =  0
        
        #進行度合いの表示
        nextP = math.floor(i/end*100)
        if nextP > current : 
            sys.stdout.write("\r%s" % str(nextP)+"% ")
            sys.stdout.flush()
            time.sleep(0.01)
        current = nextP
        
    sys.stdout.write("\r%s" % str(100)+"% ")
    print("\n作成完了\n")
        
    return array

if __name__ == '__main__':
    #WAVデータの読み込み
    wav_data_hi = read_wav_cd(wavName_hi,beginFlame,endFlame)
    #wav_data_cd = read_wav_cd(wavName_cd)
    
    a = makeAmpArrayHi(wav_data_hi['amp_l'], beginFlame, endFlame)
    b = makeAmpArrayCD(wav_data_hi['amp_l'], beginFlame, endFlame)
    
    #CSVファイルの出力
    #makeAmpCSV(wav_data_hi['amp_l'], csvName_hi,beginFlame,endFlame)
    #現時点ではハイレゾ音源から擬似CD音源の特徴ベクトルを作成する
    #makeAmpCSV2(wav_data_hi['amp_l'], csvName_cd,beginFlame,endFlame)
    #print("CSVファイルを出力しました。")
