from drone_info_functions import *
from data_functions import get_distance_between_nodes, get_time_between_nodes

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

def get_fitness(nodes, costs, tsp_route, uav_sorties, n_uavs):
    '''
    Obtiene el fitness de la solucion actual
    '''
    time = 0
    launch_times = [0] * n_uavs

    t_service_truck = getServiceTimeTruck()
    for index, node in enumerate(tsp_route[:-1]):
        # Se actualiza el tiempo de viaje, con el viaje entre los nodos
        if index != 0:
            time += get_time_between_nodes(costs, tsp_route[index - 1], node)
            print(f'Delivery {node}')

        uavs_reaches = get_uavs_reaches(uav_sorties, node)
        uavs_go_out = get_uavs_go_out(uav_sorties, node)
        intersection = get_uavs_reaches_and_go_out(uavs_reaches, uavs_go_out)
        print(f'Uavs que llegan y salen del nodo {node}: {intersection}')
        print(f'Uavs que llegan en nodo {node}: {uavs_reaches}')
        print(f'Uavs que salen del nodo {node}: {uavs_go_out}')
        print()

    print(time)
    return time


def get_uavs_reaches(uav_sorties, node):
    '''
    Obtiene el travel tuple del uav si es que llega al nodo ingresado, si no hay ningun
    viaje en donde el dron llegue a ese nodo, entonces retorna None
    '''
    uavs_reaches = []
    for dron_travel in uav_sorties:
        travel_tuple = dron_travel[1]

        destiny_node_travel = travel_tuple[TRAV_DESTINY]
        if node == destiny_node_travel:
            uavs_reaches.append(dron_travel)

    return uavs_reaches


def get_uavs_go_out(uav_sorties, node):
    '''
    Obtiene el travel tuple del uav si es que se lanza desde el nodo ingresado, si no hay ningun
    viaje en donde el dron se lance deste ese nodo, entonces retorna None
    '''
    uavs_go_out = []
    for dron_travel in uav_sorties:
        travel_tuple = dron_travel[1]

        origin_node_travel = travel_tuple[TRAV_ORIGIN]
        if node == origin_node_travel:
            uavs_go_out.append(dron_travel)
    return uavs_go_out

def get_uavs_reaches_and_go_out(uavs_reaches, uavs_go_out):
    intersection = []
    index_reaches = []
    index_go_out = []

    # Se obtiene la interseccion entre las dos listas
    for index_r, uav_reache in enumerate(uavs_reaches):
        id_uav_reache, travel_tuple_reache = uav_reache

        for index_g, uav_go_out in enumerate(uavs_go_out):
            id_uav_go_out, travel_tuple_go_out = uav_go_out

            if id_uav_go_out == id_uav_reache and travel_tuple_reache[TRAV_DESTINY] == travel_tuple_go_out[TRAV_ORIGIN]:
                intersection.append((uav_reache, uav_go_out))
                index_reaches.append(index_r)
                index_go_out.append(index_g)
                break

    return intersection

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

def get_time_dron_travel(costs, origin_travel, destiny_travel):
    '''
    Obtiene el tiempo de viaje de un UAV entre dos nodos
    '''
    travel_time = get_distance_between_nodes(costs, origin_travel, destiny_travel) / getCruiseSpeed()
    return travel_time

