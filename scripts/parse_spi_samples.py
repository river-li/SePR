import os
import pandas as pd

def parseCSV(csv_path):
    csv_path = os.path.abs(csv_path)

    df = pd.read_csv(csv_path)
    del(df['Unnamed: 0'])

    nsep = df.loc[df['vulnerability']==0]
    sep = df.loc[df['vulnerability']==1]
