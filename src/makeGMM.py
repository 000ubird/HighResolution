import numpy as np
from sklearn import mixture
from sklearn.externals import joblib
import matplotlib.pyplot as plt

#ファイル名
csvName_hi = "../result_hi.csv"
csvName_cd = "../result_cd.csv"

#取得する振幅値の数(次元数)
N = 20

#CSVファイルから振幅値の2次元配列取得
def getAmpArray(fileName):
    #CSVファイルをfloatとして読み込み
    data = np.recfromcsv(fileName)
    
    #numpyのinsert用ダミーデータ
    dummy_data = [0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0]
    
    array = np.array([dummy_data],dtype=float)
    tmp_array = np.array([],dtype=float)
    n = 1
    m = 0
    #学習用の配列を作成する
    for i in data : 
        for j in i: 
            tmp_array = np.insert(tmp_array, m, j)
            m += 1
                
        array = np.insert(array,n,tmp_array,axis=0)
        tmp_array = np.array([],dtype=float)    #tmp_arrayを初期化
        #print(array[n])    #デバッグ
        n+=1
        m=0

    return array

def debug_gmm(gmm) :
    # 結果を表示
    print ("*** weights")   #混合係数
    print (gmm.weights_)
    
    #print ("*** means")     #平均ベクトル    
    #print (gmm.means_)
    
    #print ("*** covars")    #共分散行列
    #print (gmm.covars_)
    
    # 0番目のコンポーネントの共分散行列を描画
    plt.imshow(gmm.covars_[0])
    plt.show()
    
if __name__ == '__main__':
    #CSVファイルから振幅値を取得
    print("振幅値を読み込んでいます。")
    array = getAmpArray(csvName_cd) #変換元
    array2= getAmpArray(csvName_hi) #変換先
    print("振幅値を読み込みました。")
    
    print("ベクトルを結合しています。\n")
    Z = np.hstack((array,array2))
    
    print("GMMの学習を開始します。")
    # GMMを学習
    n_components = 30    #混合数
    gmm = mixture.GMM(n_components, covariance_type='full')
    gmm.fit(Z)
    print("GMMの学習が終わりました。")
    
    #GMMを保存
    joblib.dump(gmm, "gmm")
    
    debug_gmm(gmm)
