import pandas as pd
import numpy as np
from sklearn import svm


class OCSVM:
    def __init__(self, csv):
        self.data = np.array(pd.read_csv(csv)).T[1:].T
        # when we save as csv, the
        self.model = svm.OneClassSVM(nu=0.1,kernel='sigmoid',gamma=0.1)
        self.model.fit(self.data)

    def train(self,data):
        self.model.fit(data)

    def predict(self,data):
        predict = self.model.predict(data)
        return predict