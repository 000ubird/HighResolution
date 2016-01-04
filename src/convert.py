import numpy as np
from scipy.stats import multivariate_normal
from sklearn.externals import joblib

#参考 : http://aidiary.hatenablog.com/entry/20150418/1429357892

#ファイル名
gmmFile = "gmm"

#取得する振幅値の数
N = 20

# GMMの混合数
K = 5

def convert_mcep(sourceAmp, result, gmm):
    source_mcep = sourceAmp

    # 式9の多次元正規分布のオブジェクトを作成しておく
    gauss = []
    for k in range(K):
        gauss.append(multivariate_normal(gmm.means_[k, 0:N], gmm.covars_[k, 0:N, 0:N]))

    # 式11のフレームtに依存しない項を計算しておく
    ss = []
    for k in range(K):
        #ss.append(np.dot(gmm.covars_[k, N:, 0:N], np.linalg.inv(gmm.covars_[k, 0:N, 0:N])))
        ss.append(np.dot(gmm.covars_[k, 0:N, 0:N], np.linalg.inv(gmm.covars_[k, 0:N, 0:N])))
        
    # 各フレームをGMMで変形する
    for t in range(len(source_mcep)):
        x_t = source_mcep[t]
        y_t = convert_frame(x_t, gmm, gauss, ss)
        print(y_t)
    
    return y_t

# 式(13)の計算
def convert_frame(x, gmm, gauss, ss):
    # 式(9)の分母だけ先に計算
    denom = np.zeros(K)
    for n in range(K):
        denom[n] = gmm.weights_[n] * gauss[n].pdf(x)
        
    y = np.zeros_like(x)
    
    for k in range(K):
        y += P(k, x, gmm, gauss, denom) * E(k, x, gmm, ss)
    return y

# 式(9)の計算
def P(k, x, gmm, gauss, denom):
    return denom[k] / np.sum(denom)

# 式(11)の計算
def E(k, x, gmm, ss):
    tmp = np.dot(ss[k], x - gmm.means_[k, 0:N]) #内積を取る
    
    #return gmm.means_[k, N:] + tmp
    return gmm.means_[k, 0:] + tmp

if __name__ == '__main__':
    print("GMMの読み込みを開始します。")
    gmm = joblib.load(gmmFile)
    #print(gmm.covars_)
    print("GMMの読み込みが終わりました。")
    
    sampleAmp = [[0.24906155583361309,0.2772301400799585,
                  0.23670155949583421,0.20682393871883298,
                  0.22400585955381938,0.249977111117893, 
                  0.24286629840998566,0.21613208410901211,
                  0.20715964232306894,0.21845149082918791,
                  0.22156437879573962,0.20630512405774101,
                  0.19275490585039826,0.19483016449476609,
                  0.19956053346354563,0.19180883205664234,
                  0.17877742851039155,0.17523728141117587,
                  0.17871639149143956,0.17569505905331584,]]
    
    result_amp = convert_mcep(sampleAmp, "out.txt", gmm)
    
    print("最終結果 : \n")
    result = ""
    for i in result_amp : 
        result += str(i)+","
        
    print(result)
    
