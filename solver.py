import random
import math

def get_distance(data, index_origin, index_destiny):
    x_origin = data['latDeg'][index_origin]
    x_destiny = data['latDeg'][index_destiny]

    y_origin = data['lonDeg'][index_origin]
    y_destiny = data['lonDeg'][index_destiny]
    distance = math.hypot(x_origin - x_destiny, y_origin - y_destiny)
    return distance

def get_fitness(data, tsp_route):
    sum_distances = 0
    for i in range(1, len(tsp_route)):
        sum_distances += get_distance(data, tsp_route[i - 1], tsp_route[i])

    return sum_distances

def get_tsp_points(data):
    quants_points_deliveriable = data.shape[0] - 1
    tsp_route = random.sample(range(1, quants_points_deliveriable + 1), quants_points_deliveriable)
    #tsp_route = list(range(1, quants_points_deliveriable + 1))
    tsp_route = [0] + tsp_route + [0]
    #tsp_route = [0, 4, 8, 6, 20, 25, 17, 18, 12, 7, 10, 3, 19, 14, 23, 11, 9, 16, 22, 24, 21, 2, 5, 15, 13, 1, 0]

    is_improve = True
    while is_improve:
        previous_fitness = get_fitness(data, tsp_route)
        tsp_route = run_2opt(data, tsp_route)
        new_fitness = get_fitness(data, tsp_route)

        is_improve = previous_fitness != new_fitness

    return tsp_route

def run_2opt(data, tsp_route):
    min_change = 0
    min_i = 0
    min_j = 0

    quants_points = len(tsp_route)

    for i in range(quants_points - 2):
        for j in range(i + 2, quants_points - 1):
            current_cost = get_distance(data, tsp_route[i], tsp_route[i + 1]) + get_distance(data, tsp_route[j], tsp_route[j + 1])
            new_cost = get_distance(data, tsp_route[i], tsp_route[j]) + get_distance(data, tsp_route[i + 1], tsp_route[j + 1])
            change = new_cost - current_cost

            if change < min_change:
                min_change = change
                min_i = i
                min_j = j

    if min_change < 0:
        tsp_route[min_i + 1: min_j + 1] = tsp_route[min_i + 1: min_j + 1][::-1]

    return tsp_route




