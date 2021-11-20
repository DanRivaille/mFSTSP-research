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

def get_fitness(nodes, costs, tsp_route, uav_sorties):
    '''
    Obtiene el fitness de la solucion actual
    '''
    time = 0

    t_service_truck = getServiceTimeTruck()
    for index, node in enumerate(tsp_route[:-1]):
        # Se actualiza el tiempo de viaje, con el viaje entre los nodos
        if index != 0:
            time += get_time_between_nodes(costs, tsp_route[index - 1], node)
            time += t_service_truck
            print(f'Delivery {node}')

    print(time)
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


def get_distance_dron_travel(nodes, travel_tuple):
    '''
    Obtiene la distancia del viaje de un UAV, desde que sale del camion, luego se dirije
    hacia el cliente, y por ultimo cuando se junta con el camion
    '''
    distance_dron_travel = get_distance(nodes, travel_tuple[TRAV_ORIGIN], travel_tuple[TRAV_CLIENT])
    distance_dron_travel += get_distance(nodes, travel_tuple[TRAV_CLIENT], travel_tuple[TRAV_DESTINY])
    return distance_dron_travel