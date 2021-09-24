import matplotlib.pyplot as plt
from graphics import *
from solver import get_tsp_points

# Settings of pyplot
plt.rcParams["figure.figsize"] = (20, 10)

df = load_data('problems/example.csv')

set_plot_limits(plt, df)

draw_points(plt, df)

# TSP Route
tsp_route_points = get_tsp_points(df)
print(tsp_route_points)

draw_tsp_route(plt, df, tsp_route_points)

plt.show()

