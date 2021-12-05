import matplotlib.pyplot as plt
from graphics import *
from solver import *
from data_functions import *
from drone_info_functions import load_dron_info
from objective_function import get_fitness

PLOT_ROUTES = False

def main():
    # Load data
    load_dron_info('drones_types_info/drone101.csv')
    costs = load_costs_nodes('problems/example_truck_travel_data.csv')
    df = load_data('problems/example.csv')
    nodes = create_nodes_list(df)

    n_uavs = 3

    # Ploting the points
    plt.rcParams["figure.figsize"] = (20, 10)
    set_plot_limits(plt, df)
    draw_points(plt, df)

    # TSP Route
    tsp_route_points = get_tsp_points(nodes)
    drones_travels = get_drones_routes(nodes, tsp_route_points)
    fitness = get_fitness(nodes, costs, tsp_route_points, drones_travels, n_uavs)


    print("UAV's sorties: ")
    for dron_travel in drones_travels:
        print(dron_travel)

    print(f"TSP Tour: {tsp_route_points}")

    if PLOT_ROUTES:
        draw_tsp_route(plt, nodes, tsp_route_points)
        draw_drones_routes(plt, nodes, drones_travels)



if __name__ == '__main__':
    main()

