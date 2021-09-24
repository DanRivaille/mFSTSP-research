import pandas as pd

def scale_data(data, scale_factor=1000000):
    data['latDeg'] = data['latDeg'] * scale_factor
    data['lonDeg'] = data['lonDeg'] * scale_factor
    return data

def load_data(filename):
    '''
    Carga los datos
    '''
    names = ['nodeType', 'latDeg', 'lonDeg', 'altMeters', 'parcelWtLbs']
    data = pd.read_csv(filename, names=names, skiprows=1, index_col=0)

    return data


