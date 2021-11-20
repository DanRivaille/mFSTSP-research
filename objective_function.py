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
    t_salida = time
    t_etapas = get_t_etapas()
    for index, node in enumerate(tsp_route[:-1]):
        is_delivery_done = False

        # Se actualiza el tiempo de viaje, con el viaje entre los nodos
        if index != 0:
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
            print(f'{t_absolute} - UAV llega al nodo {node}')

            # Se calcula el tiempo en idle 
            t_etapas[ET_IDLE] = time - t_etapas[ET_DESCE_TRUCK] - t_absolute
            print(t_etapas[ET_IDLE])

            # Si el camion llego antes que el UAV y tiene tiempo de realizar la entrega
            if t_etapas[ET_IDLE] < 0 and -t_etapas[ET_IDLE] > t_service_truck:
                # Se realiza el delivery del camion y luego se recupera el uav
                print(f'{time} - El camion comienza a realizar su entrega')
                time += t_service_truck
                print(f'{time} - El camion termina de realizar su entrega')
                print(f'{time} - Se comienza a recuperar el UAV')
                time += sum(t_etapas[8:])
                print(f'{time} - Se recupera el UAV')
            else:
                # Se recupera el uav y luego se realiza el delivery del camion
                print(f'{time} - Se comienza a recuperar el UAV')
                time += sum(t_etapas[8:])
                print(f'{time} - Se recupera el UAV')
                print(f'{time} - El camion comienza a realizar su entrega')
                time += t_service_truck
                print(f'{time} - El camion termina de realizar su entrega')

            is_delivery_done = True

        
        # Se verifica si es que se lanza un UAV desde este nodo
        travel_tuple_uav_go_out = get_travel_tuple_from_uav_go_out(uav_sorties, node)
        if travel_tuple_uav_go_out is not None:
            t_salida = time
            print(f'{time} - Se comienza a lanzar un UAV desde el nodo {node}')
            time += t_etapas[ET_PREPARACION]
            print(f'{time} - El UAV deja el nodo { node }')

        # Si no se ha realizado todavia el delivery, se realiza
        if not is_delivery_done:
            print(f'{time} - El camion comienza a realizar su entrega')
            time += t_service_truck
            print(f'{time} - El camion termina de realizar su entrega')


        print(f'{time} - Dejando el nodo { node }\n')

    print(f'{time} - LLegando al deposito')
    print(f'Tiempo total: {time}')

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