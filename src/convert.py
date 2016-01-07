import numpy as np
from scipy.stats import multivariate_normal
from sklearn.externals import joblib

#参考 : http://aidiary.hatenablog.com/entry/20150418/1429357892

#ファイル名
gmmFile = "gmm"

#取得する振幅値の数
N = 20

# GMMの混合数
K = 30

def convert_mcep(sourceAmp, result, gmm):
    source_mcep = sourceAmp

    # 式9の多次元正規分布のオブジェクトを作成しておく
    gauss = []
    for k in range(K):
        gauss.append(multivariate_normal(gmm.means_[k, 0:N], gmm.covars_[k, 0:N, 0:N]))

    # 式11のフレームtに依存しない項を計算しておく
    ss = []
    for k in range(K):
        ss.append(np.dot(gmm.covars_[k, N:, 0:N], np.linalg.inv(gmm.covars_[k, 0:N, 0:N])))
        #ss.append(np.dot(gmm.covars_[k, 0:N, 0:N], np.linalg.inv(gmm.covars_[k, 0:N, 0:N])))
        
    # 各フレームをGMMで変形する
    for t in range(len(source_mcep)):
        x_t = source_mcep[t]
        y_t = convert_frame(x_t, gmm, gauss, ss)
    
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
    
    return gmm.means_[k, N:] + tmp
    #return gmm.means_[k, 0:] + tmp

if __name__ == '__main__':
    print("GMMの読み込みを開始します。")
    gmm = joblib.load(gmmFile)
    #print(gmm.covars_)
    print("GMMの読み込みが終わりました。")
    
    sampleAmp = [[-0.16595458984375,-0.16595458984375,
                  -0.1448974609375,-0.1448974609375,
                  0.055299539170506916,0.055299539170506916,
                  0.33420819727164525,0.33420819727164525,
                  0.21985534226508377,0.21985534226508377,
                  0.1945249794000061,0.1945249794000061,
                  0.28949858088930935,0.28949858088930935,
                  0.17230750450148014,0.17230750450148014,
                  0.24451429792168949,0.24451429792168949,
                  0.19888912625507371,0.19888912625507371]]
    
    result_amp = convert_mcep(sampleAmp, "out.txt", gmm)
    
    print("最終結果 : ",result_amp)
