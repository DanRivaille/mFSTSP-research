import pandas as pd

names = ['nodeType', 'latDeg', 'lonDeg', 'altMeters', 'parcelWtLbs']
df = pd.read_csv('problems/example.csv', names=names, skiprows=1, index_col=0)

print(df)


