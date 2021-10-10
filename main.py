import matplotlib.pyplot as plt
from graphics import *
from solver import *
from data_functions import load_data, create_nodes_list


def main():
    # Load data
    df = load_data('problems/example.csv')

    # Ploting the points
    plt.rcParams["figure.figsize"] = (20, 10)
    set_plot_limits(plt, df)
    draw_points(plt, df)

    # TSP Route
    tsp_route_points = get_tsp_points(df)
    fitness = get_fitness(df, tsp_route_points)

    drones_travels = get_drones_routes(df, tsp_route_points)

    print(drones_travels)
    print(tsp_route_points)
    print(int(fitness * 1000000))

    for dron_travel in drones_travels:
        new_tsp = update_tsp_with_drone(tsp_route_points, dron_travel)
        tsp_route_points = new_tsp

    draw_tsp_route(plt, df, tsp_route_points)
    draw_drones_routes(plt, df, drones_travels)


    plt.show()


if __name__ == '__main__':
    #main()
    df = load_data('problems/example.csv')
    nodes = create_nodes_list(df)

    for node in nodes:
        print(node)

