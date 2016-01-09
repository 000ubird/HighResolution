import numpy as np
import pylab as pl
from scipy.stats import multivariate_normal
from sklearn.externals import joblib
from makeGMM import getAmpArray

#参考 : http://aidiary.hatenablog.com/entry/20150418/1429357892

#ファイル名
gmmFile = "gmm"

#取得する振幅値の数
N = 20

def convert(sourceAmp, gmm,component):
    # 式9の多次元正規分布のオブジェクトを作成しておく
    gauss = []
    for k in range(component):
        gauss.append(multivariate_normal(gmm.means_[k, 0:N], gmm.covars_[k, 0:N, 0:N]))

    # 式11のフレームtに依存しない項を計算しておく
    ss = []
    for k in range(component):
        ss.append(np.dot(gmm.covars_[k, N:, 0:N], np.linalg.inv(gmm.covars_[k, 0:N, 0:N])))
        
    # 各フレームをGMMで変形する
    for t in range(len(sourceAmp)):
        x_t = sourceAmp[t]
        y_t = convert_frame(x_t, gmm, gauss, ss, component)
    
    return y_t

# 式(13)の計算
def convert_frame(x, gmm, gauss, ss,component):
    # 式(9)の分母だけ先に計算
    denom = np.zeros(component)
    for n in range(component):
        denom[n] = gmm.weights_[n] * gauss[n].pdf(x)
        
    y = np.zeros_like(x)
    
    for k in range(component):
        y += P(k, x, gmm, gauss, denom) * E(k, x, gmm, ss)
    return y

# 式(9)の計算
def P(k, x, gmm, gauss, denom):
    return denom[k] / np.sum(denom)

# 式(11)の計算
def E(k, x, gmm, ss):
    tmp = np.dot(ss[k], x - gmm.means_[k, 0:N]) #内積を取る
    
    return gmm.means_[k, N:] + tmp

if __name__ == '__main__':
    print("GMMの読み込みを開始します。")
    gmm = joblib.load(gmmFile)
    print("GMMの読み込みが終わりました。\n")
    
    print("変換元のファイルを読み込んでいます。")
    sampleAmp = getAmpArray("../result_cd.csv")
    sampleFlame = sampleAmp[2500]
    print("変換元 : ",sampleFlame)
    pl.plot(sampleFlame)
    pl.show()
    
    print("変換を実行します。")
    result_amp = convert([sampleFlame], gmm,30)
    print("変換が終わりました。\n")
    
    print("最終結果 : ",result_amp)
    pl.plot(result_amp)
    pl.show()
    
    print("正解ファイルを読み込んでいます。")
    correct = getAmpArray("../result_hi.csv")
    pl.plot(correct[2500])
    pl.show()
    
