import numpy as np
from sklearn import svm

clf = svm.OneClassSVM(nu=0.1,kernel='rbf',gamma=0.1)
