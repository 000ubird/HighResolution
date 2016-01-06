import numpy as np
from sklearn import mixture
from sklearn.externals import joblib
import matplotlib.pyplot as plt

#ファイル名
wavName = "../wav/sample_96000_24bit_000.wav"
csvName = "../result_hi.csv"

#取得する振幅値の数(次元数)
N = 20

#CSVファイルから振幅値の2次元配列取得
def getAmpArray(fileName):
    #CSVファイルをfloatとして読み込み
    data = np.recfromcsv(csvName)
    
    #学習用の配列を作成する
    array = []
    n=0
    m=0
    for i in data : 
        array.append([])
        for row in i :
            if row != False : 
                array[n].append(row)
                #print(n,m,row)    #デバッグ
                m+=1
        m=0    
        n+=1
    
    return array

def debug_gmm(gmm) :
    # 結果を表示
    print ("*** weights")   #混合係数
    print (gmm.weights_)
    
    print ("*** means")     #平均ベクトル    
    print (gmm.means_)
    
    print ("*** covars")    #共分散行列
    print (gmm.covars_)
    
    predict = gmm.predict(array[3])
    print ( gmm.score(array[3]) )
    print ( gmm.score(array[4]) )
    print ( gmm.score(array[5]) )
    print(predict)
    
    # コンポーネントの平均ベクトルを描画
    for k in range(5):
        plt.plot(gmm.means_[k, :])
    plt.xlim((0, (N+1)*2))
    plt.show()

    # 0番目のコンポーネントの共分散行列を描画
    plt.imshow(gmm.covars_[0])
    plt.show()
    
if __name__ == '__main__':
    #CSVファイルから振幅値を取得
    print("振幅値を読み込みます。")
    array = getAmpArray(csvName)
    print("振幅値を読み込みました。")
    
    print("GMMの学習を開始します。")
    # GMMを学習
    n_components = 5    #混合数
    gmm = mixture.GMM(n_components, covariance_type='full')
    gmm.fit(array)
    print("GMMの学習が終わりました。")
    
    #GMMを保存
    joblib.dump(gmm, "gmm.txt")
    
    debug_gmm(gmm)
