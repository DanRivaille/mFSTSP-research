import matplotlib.pyplot as plt
from graphics import *
from data_functions import load_data
from solver import get_tsp_points

# Load data
df = load_data('problems/example.csv')

# Ploting the points
plt.rcParams["figure.figsize"] = (20, 10)
set_plot_limits(plt, df)
draw_points(plt, df)

# TSP Route
tsp_route_points = get_tsp_points(df)
draw_tsp_route(plt, df, tsp_route_points)

print(tsp_route_points)

plt.show()

