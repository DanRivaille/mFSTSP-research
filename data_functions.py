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

def load_costs_nodes(filename):
    '''
    Carga los costos (distancia y tiempo) de los viejes entre los nodos
    '''
    names = ['origin', 'destiny', 'time', 'distance']
    data = pd.read_csv(filename, names=names, skiprows=1)

    return data

def get_distance_between_nodes(costs, origin_node, destiny_node):
    '''
    Obtiene la distancia entre los nodos "origin_node" y "destiny_node"
    '''
    distance_serie = costs[(costs['origin'] == origin_node)  & (costs['destiny'] == destiny_node)]
    distance = distance_serie.distance.values[0]
    return distance

def get_time_between_nodes(costs, origin_node, destiny_node):
    '''
    Obtiene el tiempo entre los nodos "origin_node" y "destiny_node"
    '''
    time_serie = costs[(costs['origin'] == origin_node)  & (costs['destiny'] == destiny_node)]
    time = time_serie.time.values[0]
    return time

def create_nodes_list(dataframe):
    nodes = []

    for i in range(len(dataframe)):
        new_node = Node(dataframe.iloc[i], i)
        nodes.append(new_node)

    return nodes

