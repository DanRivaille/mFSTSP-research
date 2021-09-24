import random
import pandas as pd

def get_deliveriable_points_by_drones(data):
    '''
    Obtiene los puntos que son entregables por drones
    '''
    filtered_data = data[(data['nodeType'] != 0) & (data['altMeters'] == 0) & (data['parcelWtLbs'] <= 5)]
    return filtered_data

def get_not_deliveriable_points_by_drones(data):
    '''
    Obtiene los puntos que no son entregables por drones (solo por camiones)
    '''
    filtered_data = data[(data['nodeType'] != 0) & ((data['altMeters'] != 0) | (data['parcelWtLbs'] > 5))]
    return filtered_data

def get_coords_from_points(data, route_points):
    '''
    Dada una lista con el orden que deben ser visitadas las ciudades (ruta TSP)
    entrega las coordenadas de cada ciudad de la ruta
    '''
    lat_tsp = []
    lon_tsp = []

    for point in route_points:
        lat_tsp.append(data.iloc[point]['latDeg'])
        lon_tsp.append(data.iloc[point]['lonDeg'])

    return lat_tsp, lon_tsp

def draw_tsp_route(plt, data, tsp_route_points):
    '''
    Dibuja la ruta del tsp ingresada
    '''
    x, y = get_coords_from_points(data, tsp_route_points)
    plt.plot(x, y, linewidth=1)
    plt.arrow(x[0], y[0], (x[1] - x[0]) / 2, (y[1] - y[0]) / 2, width=0.0005)

def draw_drones_routes(plt, data, drones_routes):
    for travel_tuple in drones_routes:
        x, y = get_coords_from_points(data, travel_tuple)
        plt.plot(x, y, "g--")

def set_plot_limits(plt, data, delta=0.01):
    '''
    Establece los limites de los ejes del grafico
    '''
    max_lat = data['latDeg'].max()
    min_lat = data['latDeg'].min()

    max_lon = data['lonDeg'].max()
    min_lon = data['lonDeg'].min()

    plt.ylim(min_lon - delta, max_lon + delta)
    plt.xlim(min_lat - delta, max_lat + delta)

def draw_points(plt, data):
    '''
    Dibuja los puntos en el grafico
    '''
    deliveriable_points_by_drones = get_deliveriable_points_by_drones(data)
    not_deliveriable_points_by_drones = get_not_deliveriable_points_by_drones(data)

    # Plot the deposit
    plt.scatter(data.iloc[0]['latDeg'], data.iloc[0]['lonDeg'], marker='^', s=150, color='black')

    # Plot the deliveriable point by drones
    plt.scatter(deliveriable_points_by_drones['latDeg'], deliveriable_points_by_drones['lonDeg'], color='green')

    # Plot the not deliveriable point by drones (only trucks)
    plt.scatter(not_deliveriable_points_by_drones['latDeg'], not_deliveriable_points_by_drones['lonDeg'], marker='s', color='red')

