import pandas as pd

def load_data(filename):
    '''
    Carga los datos
    '''
    names = ['nodeType', 'latDeg', 'lonDeg', 'altMeters', 'parcelWtLbs']
    data = pd.read_csv(filename, names=names, skiprows=1, index_col=0)
    return data

