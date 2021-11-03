import random
import math
from data_functions import get_distance_between_nodes, get_time_between_nodes
from drone_info_functions import *

def get_distance(nodes, index_origin, index_destiny):
    '''
    Obtiene la distancia entre dos puntos
    '''
    x_origin = nodes[index_origin].x
    x_destiny = nodes[index_destiny].x

    y_origin = nodes[index_origin].y
    y_destiny = nodes[index_destiny].y
    distance = math.hypot(x_origin - x_destiny, y_origin - y_destiny)
    return distance

def get_fitness(nodes, costs, tsp_route, uav_sorties):
    '''
    Obtiene el fitness de la solucion actual
    '''
    time = 0
    for index, node in enumerate(tsp_route):
        if index != 0:
            time += get_time_between_nodes(costs, tsp_route[index - 1], node)

        print("------------------------------------------\n")
        print(f"Nodo actual: {node} - tiempo actual {time}\n")
        print("Drones que se lanzan desde este punto: ")


        for dron_travel in uav_sorties:
            uav_id, travel_tuple = dron_travel
            launch_node, service_node, recovery_node = travel_tuple

            if node == launch_node:
                time_travel = get_time_dron_travel(nodes, costs, travel_tuple)
                print(f"UAV {uav_id} - travel: {travel_tuple} - tiempo {time_travel}")

        print()
        print("Drones que llegan en este punto: ")

        for dron_travel in uav_sorties:
            uav_id, travel_tuple = dron_travel
            launch_node, service_node, recovery_node = travel_tuple

            if node == recovery_node:
                print(f"UAV {uav_id} - travel: {travel_tuple}")
    return 0

def get_time_dron_travel(nodes, costs, travel_tuple):
    preparacion = getLaunchTime()
    elevacion_camion = getCruiseAlt() / getTakeoffSpeed()
    viaje_ida = get_distance_between_nodes(costs, travel_tuple[0], travel_tuple[1]) / getCruiseSpeed()
    descenso_cliente = getCruiseAlt() / getLandingSpeed()
    entrega = getServiceTimeDrone()
    elevacion_cliente = getCruiseAlt() / getTakeoffSpeed()
    viaje_vuelta = get_distance_between_nodes(costs, travel_tuple[1], travel_tuple[2]) / getCruiseSpeed()

    travel_time = preparacion + elevacion_camion + viaje_ida
    travel_time += descenso_cliente + entrega + elevacion_cliente + viaje_vuelta
    return travel_time


def get_tsp_points(nodes):
    '''
    Calcula la ruta tsp
    '''
    return [0, 17, 10, 3, 11, 16, 22, 24, 2, 5, 21, 8, 6, 25, 0]
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
            current_cost = get_distance(nodes, tsp_route[i], tsp_route[i + 1]) + get_distance(nodes, tsp_route[j], tsp_route[j + 1])
            new_cost = get_distance(nodes, tsp_route[i], tsp_route[j]) + get_distance(nodes, tsp_route[i + 1], tsp_route[j + 1])
            change = new_cost - current_cost

            if change < min_change:
                min_change = change
                min_i = i
                min_j = j

    if min_change < 0:
        tsp_route[min_i + 1: min_j + 1] = tsp_route[min_i + 1: min_j + 1][::-1]

    return tsp_route

def get_distance_dron_travel(nodes, travel_tuple):
    distance_dron_travel = get_distance(nodes, travel_tuple[0], travel_tuple[1])
    distance_dron_travel += get_distance(nodes, travel_tuple[1], travel_tuple[2])
    return distance_dron_travel

def get_drones_routes(nodes, tsp_route):
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
    length = len(tsp_route)
    max_dron_flight = 0.05
    drones_routes = []

    for i in range(0, length - 2):
        travel_tuple = (tsp_route[i], tsp_route[i + 1], tsp_route[i + 2])
        distance_dron_travel = get_distance_dron_travel(nodes, travel_tuple)

        if distance_dron_travel < max_dron_flight:
            drones_routes.append((2, travel_tuple))

    return drones_routes

def update_tsp_with_drone(tsp_route, dron_travel_tuple):
    
    if dron_travel_tuple[0] in tsp_route:
        start_index_drone_travel = tsp_route.index(dron_travel_tuple[0])
        new_tsp_route = tsp_route[0:start_index_drone_travel + 1] + tsp_route[start_index_drone_travel + 2:]
    else:
        new_tsp_route = tsp_route

    return new_tsp_route

