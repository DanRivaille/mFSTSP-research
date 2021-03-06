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
    launch_times = [-1] * n_uavs
    available_times = [-1] * n_uavs
    idle_times = [-1] * n_uavs
    t_service_truck = getServiceTimeTruck()

    for i, node, in enumerate(tsp_route):
        if i != 0:
            time += get_time_between_nodes(costs, tsp_route[i - 1], node)
            print(f'{time} - Llegando al nodo {node}')

        uavs_reaches = get_uavs_reaches(uav_sorties, node)
        uavs_go_out = get_uavs_go_out(uav_sorties, node)

        if len(uavs_reaches) != 0:
            available_times = get_available_times(costs, n_uavs, uavs_reaches, launch_times)
            idle_times = get_idle_times(n_uavs, uavs_reaches, available_times, time)

        # Mientras hayan nodos esperando
        while (len(uavs_reaches) != 0) or (len(uavs_go_out) != 0):

            # Obtengo un uav con bateria critica FALTA IMPLEMENTAR LA BATERIA!!!
            index_uav = get_low_battery(nodes, costs, uavs_reaches, idle_times)
            if index_uav >= 0:
                time = recover_uav(uavs_reaches, launch_times, idle_times, available_times, index_uav, time)
                update_idle_times(uavs_reaches, idle_times, is_going=False)
                continue

            # Obtengo una tupla de un uav que llega y sale en este mismo nodo
            indexes_uavs = get_reaches_go(uavs_reaches, uavs_go_out)
            if indexes_uavs != None:
                time = recover_uav(uavs_reaches, launch_times, idle_times, available_times, indexes_uavs[0], time)
                update_idle_times(uavs_reaches, idle_times, is_going=False)

                time = launch_uav(uavs_go_out, launch_times, indexes_uavs[1], time)
                update_idle_times(uavs_reaches, idle_times, is_going=True)
                continue

            # Obtengo un uav que sale del nodo
            index_uav = get_go(uavs_go_out)
            if index_uav >= 0:
                time = launch_uav(uavs_go_out, launch_times, index_uav, time)
                update_idle_times(uavs_reaches, idle_times, is_going=True)
                continue

            # Obtengo un uav que llega a este nodo
            index_uav = get_reach(uavs_reaches, available_times)
            if index_uav >= 0:
                time = recover_uav(uavs_reaches, launch_times, idle_times, available_times, index_uav, time)
                update_idle_times(uavs_reaches, idle_times, is_going=False)
                continue

        # Realizo el delivery
        if i != len(tsp_route) - 1:
            print(f'{time} - Realizando delivery')
            time += t_service_truck

    print(f'Tiempo total: {time}')
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

def get_intersection(uavs_reaches, uavs_go_out):
    '''
    Obtiene los nodos que llegan y salen
    '''
    intersection = []

    # Se obtiene la interseccion entre las dos listas
    for index_r, uav_reache in enumerate(uavs_reaches):
        id_uav_reache, travel_tuple_reache = uav_reache

        for index_g, uav_go_out in enumerate(uavs_go_out):
            id_uav_go_out, travel_tuple_go_out = uav_go_out

            if id_uav_go_out == id_uav_reache and travel_tuple_reache[TRAV_DESTINY] == travel_tuple_go_out[TRAV_ORIGIN]:
                intersection.append((index_r, index_g))
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

def get_available_times(costs, n_uavs, uavs_reaches, launch_times):
    '''
    Obtiene los tiempos en donde los uavs llegan al nodo actual
    '''
    available_times = [-1] * n_uavs
    t_etapas = get_t_etapas()

    for uav in uavs_reaches:
        id_uav, travel = uav

        # Se suman los tiempos del viaje hasta antes del viaje de vuelta
        time_dron_travel = sum(t_etapas[:6])

        time_dron_travel += get_time_dron_travel(costs, travel[TRAV_ORIGIN], travel[TRAV_CLIENT])
        time_dron_travel += get_time_dron_travel(costs, travel[TRAV_CLIENT], travel[TRAV_DESTINY])
        available_times[id_uav - 2] = launch_times[id_uav - 2] + time_dron_travel

    return available_times

def get_idle_times(n_uavs, uavs_reaches, available_times, time):
    '''
    Obtiene los tiempos que han estado esperando los uavs que llegan al nodo
    '''
    idle_times = [-1] * n_uavs

    for uav in uavs_reaches:
        id_uav = uav[0]
        idle_times[id_uav - 2] = time - available_times[id_uav - 2]

    return idle_times

def get_low_battery(nodes, costs, uavs_reaches, idle_times):
    '''
    Obtiene el indice de un uav con bateria critica
    '''
    rec_time = getRecoveryTime()

    for index, uav in enumerate(uavs_reaches):
        id_uav, travel = uav

        # Si el idle es negativo no tiene sentido esperar por este uav (puedo hacer otro)
        if idle_times[id_uav - 2] > 0:
            distance_ij = get_distance_between_nodes(costs, travel[TRAV_ORIGIN], travel[TRAV_CLIENT])
            distance_jk = get_distance_between_nodes(costs, travel[TRAV_CLIENT], travel[TRAV_DESTINY])
            parcel_weight = nodes[travel[TRAV_CLIENT]].weight

            # Se calcula la duracion que puede seguir en el aire esperado
            #endurance_seconds = get_endurance(distance_ij, distance_jk, parcel_weight)
            endurance_seconds = rec_time * 3    # For debug

            if endurance_seconds < (rec_time * 2):
                return index

    return -1

def recover_uav(uavs_reaches, launch_times, idle_times, available_times, index_uav, time):
    '''
    Realiza la recuperacion de un uav, actualizando el tiempo actual, y algunas
    variables de los uavs
    '''
    print(f'{time} - Recogiendo uav {uavs_reaches[index_uav]}')
    # Actualizo el tiempo actual
    time += getRecoveryTime()
    time += getCruiseAlt() / getLandingSpeed() 

    # Obtengo el uav
    uav = uavs_reaches[index_uav]
    id_uav = uav[0]

    # Actualizo los demas tiempos
    launch_times[id_uav - 2] = -1
    available_times[id_uav - 2] = -1
    idle_times[id_uav - 2] = -1

    # Elimino el sortie que ya se proceso de los uavs que llegan
    uavs_reaches.pop(index_uav)

    return time

def update_idle_times(uavs_reaches, idle_times, is_going):
    '''
    Actualiza los tiempos idle de los nodos que llegan
    '''
    if is_going:
        new_time = getLaunchTime()
    else:
        new_time = getRecoveryTime()

    # Actualizo el tiempo de espera de todos los uavs que estan esperando
    for uav in uavs_reaches:
        id_uav = uav[0]
        idle_times[id_uav - 2] += new_time

def get_reaches_go(uavs_reaches, uavs_go_out):
    '''
    Obtiene un uav que llega y sale en este mismo nodo
    '''
    intersection = get_intersection(uavs_reaches, uavs_go_out)

    if len(intersection) != 0:
        return intersection[0]
    else:
        return None

def launch_uav(uavs_go_out, launch_times, index_uav, time):
    '''
    Realiza el lanzamiento de un uav, actualizando el tiempo actual, y algunas
    variables de los uavs
    '''
    print(f'{time} - Lanzando uav {uavs_go_out[index_uav]}')
    uav = uavs_go_out[index_uav]
    id_uav = uav[0]

    # Se guarda el tiempo t de lanzamiento del uav
    launch_times[id_uav - 2] = time

    time += getLaunchTime()

    # Se saca el uav que ya se proceso
    uavs_go_out.pop(index_uav)

    return time

def get_go(uavs_go_out):
    '''
    Obtiene un uav que se va en este nodo
    '''
    if len(uavs_go_out) != 0:
        return 0
    else:
        return -1

def get_min_index(available_times):
    '''
    Obtiene el indice del uav que llego primero al nodo
    '''
    i = 0
    min_t = available_times[0]

    for j, t in enumerate(available_times):
        if t < min_t and t > 0:
            i = j
            min_t = t

    return i

def get_reach(uavs_reaches, available_times):
    '''
    Obtiene el indice del uav que llego primero al nodo actual
    '''
    if len(uavs_reaches) != 0:
        # Se obtiene el que llego primero al nodo
        index = get_min_index(available_times)
        return index
    else:
        return -1

