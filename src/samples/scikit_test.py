from sklearn.datasets import load_digits
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn import mixture
from sklearn.metrics.classification import accuracy_score, classification_report

digits = load_digits()
print(digits.data.shape)
data_train, data_test, label_train, label_test = train_test_split(digits.data, digits.target)

#学習1 - 線形SVC
lin_svc = svm.LinearSVC()
lin_svc.fit(data_train, label_train)

#予測
predict = lin_svc.predict(data_test)

#正答率
print (accuracy_score(label_test,predict))

#正答率レポート
print (classification_report(label_test,predict))

#学習2 - GMM
gmm = mixture.GMM()
gmm.fit(data_train,label_train)
