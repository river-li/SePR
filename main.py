import pandas as pd
import numpy as np
from scripts.parse_spi_samples import parse_csv
from sklearn import svm

def main():
    sep,nsep = parse_csv('./data/spi/qemu.csv')
    security = np.array(sep)
    non_security = np.array(nsep)

    train = pd.read_csv('./data/linux/security.csv')
    del(train['Unnamed: 0'])
    train = np.array(train)[:,:31]

    clf = svm.OneClassSVM(nu=0.2, kernel='rbf',gamma=0.2)

if __name__ == '__main__':
    main()