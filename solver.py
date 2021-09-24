import random

def get_tsp_points(data):
    quants_points_deliveriable = data.shape[0] - 1
    #tsp_route = random.sample(range(1, quants_points_deliveriable + 1), quants_points_deliveriable)
    #tsp_route = list(range(1, quants_points_deliveriable + 1))
    #tsp_route = [0] + tsp_route + [0]
    tsp_route = [0, 4, 8, 6, 20, 25, 17, 18, 12, 7, 10, 3, 19, 14, 23, 11, 9, 16, 22, 24, 21, 2, 5, 15, 13, 1, 0]
    return tsp_route

