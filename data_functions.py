import pandas as pd
from node import Node

def scale_data(data, scale_factor=1000000):
    data['latDeg'] = data['latDeg'] * scale_factor
    data['lonDeg'] = data['lonDeg'] * scale_factor
    return data

def load_data(filename):
    '''
    Carga los datos y devuelve un dataframe de pandas
    '''
    names = ['nodeType', 'latDeg', 'lonDeg', 'altMeters', 'parcelWtLbs']
    data = pd.read_csv(filename, names=names, skiprows=1, index_col=0)

    return data

def create_nodes_list(dataframe):
    nodes = []

    for i in range(len(dataframe)):
        new_node = Node(dataframe.iloc[i], i)
        nodes.append(new_node)

    return nodes
