import random
import math
from data_functions import get_distance_between_nodes, get_time_between_nodes
from drone_info_functions import *

ET_PREPARACION = 0
ET_ELEVA_TRUCK = 1
ET_VIAJE_IDA = 2
ET_DESCE_CLI = 3
ET_ENTREGA_CLI = 4
ET_ELEVA_CLI = 5
ET_VIAJE_VUELTA = 6
ET_IDLE = 7
ET_DESCE_TRUCK = 8
ET_RECUPERACION = 9

TRAV_ORIGIN = 0
TRAV_CLIENT = 1
TRAV_DESTINY = 2

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

    t_service_truck = getServiceTimeTruck()
    t_salida = time
    t_etapas = get_t_etapas()
    for index, node in enumerate(tsp_route):
        is_delivery_done = False

        # Se actualiza el tiempo de viaje, con el viaje entre los nodos
        if index != 0:
            print(f'{time} - Viajando del nodo { tsp_route[index - 1] } al nodo { node }')
            time += get_time_between_nodes(costs, tsp_route[index - 1], node)
            print(f'{time} - LLegando al nodo { node }')

        # Se verifica si es que llegó un UAV en este nodo
        travel_tuple_uav_reaches = get_travel_tuple_from_uav_reaches(uav_sorties, node)
        if travel_tuple_uav_reaches is not None:
            # Se calcula el tiempo relativo de viaje
            origin_node = travel_tuple_uav_reaches[TRAV_ORIGIN]
            destiny_node = travel_tuple_uav_reaches[TRAV_DESTINY]
            t_etapas[ET_VIAJE_VUELTA] = get_time_dron_travel(costs, origin_node, destiny_node)
            t_relative = sum(t_etapas[:ET_VIAJE_VUELTA + 1])

            # Se calcula el tiempo absoluto
            t_absolute = t_relative + t_salida

            # Se calcula el tiempo en idle 
            t_etapas[ET_IDLE] = time - t_etapas[ET_DESCE_TRUCK] - t_absolute

            # Si el UAV llego antes que el camion
            if t_etapas[ET_IDLE] < 0:
                if -t_etapas[ET_IDLE] > t_service_truck:
                    # Se realiza el delivery del camion y luego se recupera el uav
                    time += t_service_truck
                    time += sum(t_etapas[8:])
                else:
                    # Se recupera el uav y luego se realiza el delivery del camion
                    time += sum(t_etapas[8:])
                    time += t_service_truck

                is_delivery_done = True

        
        # Se verifica si es que se lanza un UAV desde este nodo
        travel_tuple_uav_go_out = get_travel_tuple_from_uav_go_out(uav_sorties, node)
        if travel_tuple_uav_go_out is not None:
            t_salida = time
            time += t_etapas[ET_PREPARACION]

        # Si no se ha realizado todavia el delivery, se realiza
        if not is_delivery_done:
            time += t_service_truck


    return time

def get_travel_tuple_from_uav_reaches(uav_sorties, node):
    '''
    Obtiene el travel tuple del uav si es que llega al nodo ingresado, si no hay ningun
    viaje en donde el dron llegue a ese nodo, entonces retorna None
    '''
    for dron_travel in uav_sorties:
        id_uav, travel_tuple = dron_travel

        destiny_node_travel = travel_tuple[TRAV_DESTINY]
        if node == destiny_node_travel:
            return travel_tuple
        
    return None

def get_travel_tuple_from_uav_go_out(uav_sorties, node):
    '''
    Obtiene el travel tuple del uav si es que se lanza desde el nodo ingresado, si no hay ningun
    viaje en donde el dron se lance deste ese nodo, entonces retorna None
    '''
    for dron_travel in uav_sorties:
        id_uav, travel_tuple = dron_travel

        origin_node_travel = travel_tuple[TRAV_ORIGIN]
        if node == origin_node_travel:
            return travel_tuple
        
    return None

def get_time_dron_travel(costs, origin_travel, destiny_travel):
    '''
    Obtiene el tiempo de viaje de un UAV entre dos nodos
    '''
    travel_time = get_distance_between_nodes(costs, origin_travel, destiny_travel) / getCruiseSpeed()
    return travel_time

def get_t_etapas():
    '''
    Obtiene una lista de 10 elementos con los tiempos en todas las etapas del viaje de un UAV,
    en algunas etapas, los tiempos van dependiendo de donde parta, hacia donde se dirija o 
    del camion, esas etapas se calcularan despues y aqui se establecen en 0
    '''
    preparacion = getLaunchTime()
    elevacion_camion = getCruiseAlt() / getTakeoffSpeed()
    viaje_ida = 0
    descenso_cliente = getCruiseAlt() / getLandingSpeed()
    entrega = getServiceTimeDrone()
    elevacion_cliente = getCruiseAlt() / getTakeoffSpeed()
    viaje_vuelta = 0
    idle = 0
    descenso_camion = getCruiseAlt() / getLandingSpeed()
    recuperacion = getRecoveryTime()
    t_etapas = [preparacion, elevacion_camion, viaje_ida, descenso_cliente, entrega, elevacion_cliente, viaje_vuelta, idle, descenso_camion, recuperacion]

    return t_etapas


def get_tsp_points(nodes):
    '''
    Calcula la ruta tsp
    '''
    #return [0, 17, 10, 3, 11, 16, 22, 24, 2, 5, 21, 8, 6, 25, 0]
    return [0, 18, 12, 7, 10, 19, 3, 11, 16, 22, 24, 2, 5, 21, 8, 6, 25, 0]
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
    '''
    Obtiene la distancia del viaje de un UAV, desde que sale del camion, luego se dirije
    hacia el cliente, y por ultimo cuando se junta con el camion
    '''
    distance_dron_travel = get_distance(nodes, travel_tuple[TRAV_ORIGIN], travel_tuple[TRAV_CLIENT])
    distance_dron_travel += get_distance(nodes, travel_tuple[TRAV_CLIENT], travel_tuple[TRAV_DESTINY])
    return distance_dron_travel

def get_drones_routes(nodes, tsp_route):
    '''
    Ejecuta el algoritmo que calcula las rutas de los UAV para la instancia del problema
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
        distance_dron_travel = get_distance_dron_travel(nodes, travel_tuple)

        if distance_dron_travel < max_dron_flight:
            drones_routes.append((2, travel_tuple))

    return drones_routes

def update_tsp_with_drone(tsp_route, dron_travel_tuple):
    '''
    Actualiza el tsp del camion, eliminando de este los nodos que son visitados por un UAV, 
    de forma que el camion pase solo por los nodos de launch y recovery del UAV
    '''
    
    if dron_travel_tuple[TRAV_ORIGIN] in tsp_route:
        start_index_drone_travel = tsp_route.index(dron_travel_tuple[TRAV_ORIGIN])
        new_tsp_route = tsp_route[0:start_index_drone_travel + 1] + tsp_route[start_index_drone_travel + 2:]
    else:
        new_tsp_route = tsp_route

    return new_tsp_route

