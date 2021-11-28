import random
import math
from data_functions import get_distance_between_nodes, get_time_between_nodes
from drone_info_functions import *

def get_tsp_points(nodes):
    '''
    Calcula la ruta tsp
    '''
    return [0, 17, 10, 3, 11, 16, 22, 24, 2, 5, 21, 8, 6, 25, 26]
    #return [0, 18, 12, 7, 10, 19, 3, 11, 16, 22, 24, 2, 5, 21, 8, 6, 25, 0]
    quants_points_deliveriable = len(nodes) - 1
    tsp_route = random.sample(range(1, quants_points_deliveriable + 1), quants_points_deliveriable)
    tsp_route = [0] + tsp_route + [0]
    #tsp_route = [0, 4, 8, 6, 20, 25, 17, 18, 12, 7, 10, 3, 19, 14, 23, 11, 9, 16, 22, 24, 21, 2, 5, 15, 13, 1, 0]

    is_improve = True
    while is_improve:
        previous_fitness = get_fitness(nodes, tsp_route)
        tsp_route = run_2opt(nodes, tsp_route)
        new_fitness = get_fitness(nodes, tsp_route)

        is_improve = previous_fitness != new_fitness

    return tsp_route

def run_2opt(nodes, tsp_route):
    '''
    Aplica el algoritmo 2opt sobre la solucion ingresada
    '''
    min_change = 0
    min_i = 0
    min_j = 0

    quants_points = len(tsp_route)

    for i in range(quants_points - 2):
        for j in range(i + 2, quants_points - 1):
            current_cost = get_distance_between_nodes(nodes, tsp_route[i], tsp_route[i + 1]) + get_distance_between_nodes(nodes, tsp_route[j], tsp_route[j + 1])
            new_cost = get_distance_between_nodes(nodes, tsp_route[i], tsp_route[j]) + get_distance_between_nodes(nodes, tsp_route[i + 1], tsp_route[j + 1])
            change = new_cost - current_cost

            if change < min_change:
                min_change = change
                min_i = i
                min_j = j

    if min_change < 0:
        tsp_route[min_i + 1: min_j + 1] = tsp_route[min_i + 1: min_j + 1][::-1]

    return tsp_route

def get_drones_routes(nodes, tsp_route):
    '''
    Ejecuta el algoritmo que calcula las rutas de los UAV para la instancia del problema
    '''
    '''
    return [(2, (0, 4, 18)),
        (2, (18, 17, 12)),
        (2, (19, 14, 3)),
        (2, (3, 23, 11)),
        (2, (16, 9, 22)),
        (2, (22, 1, 24)),
        (2, (24, 15, 2)),
        (2, (5, 13, 21)),
        (2, (6, 20, 25))]
    '''
    return [(2, (0, 4, 17)),
 (2, (17, 7, 10)),
 (2, (10, 19, 3)),
 (2, (3, 14, 11)),
 (2, (16, 9, 24)),
 (2, (5, 15, 21)),
 (3, (17, 12, 10)),
 (3, (3, 23, 11)),
 (3, (22, 1, 24)),
 (3, (5, 13, 21)),
 (3, (6, 20, 25)),
 (4, (17, 18, 10))]
'''
    length = len(tsp_route)
    max_dron_flight = 0.05
    drones_routes = []

    for i in range(0, length - 2):
        travel_tuple = (tsp_route[i], tsp_route[i + 1], tsp_route[i + 2])
        #distance_dron_travel = get_distance_dron_travel(nodes, travel_tuple)

        if distance_dron_travel < max_dron_flight:
            drones_routes.append((2, travel_tuple))

    return drones_routes
'''
