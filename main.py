import random
import pandas as pd
import matplotlib.pyplot as plt

def get_deliveriable_points_by_drones(data):
    filtered_data = df[(df['nodeType'] != 0) & (df['altMeters'] == 0) & (df['parcelWtLbs'] <= 5)]
    return filtered_data

def get_not_deliveriable_points_by_drones(data):
    filtered_data = df[(df['nodeType'] != 0) & ((df['altMeters'] != 0) | (df['parcelWtLbs'] > 5))]
    return filtered_data

def get_tsp_points(data):
    quants_points_deliveriable = data.shape[0] - 1
    tsp_route = random.sample(range(1, quants_points_deliveriable + 1), quants_points_deliveriable)
    #tsp_route = list(range(1, quants_points_deliveriable + 1))
    tsp_route = [0] + tsp_route + [0]
    return tsp_route

def get_tsp_coords(data, tsp_route_points):
    lat_tsp = []
    lon_tsp = []

    for point in tsp_route_points:
        lat_tsp.append(data.iloc[point]['latDeg'])
        lon_tsp.append(data.iloc[point]['lonDeg'])

    return lat_tsp, lon_tsp

def draw_tsp_route(data, tsp_route_points):
    x, y = get_tsp_coords(data, tsp_route_points)
    plt.plot(x, y, linewidth=1)
    plt.arrow(x[0], y[0], (x[1] - x[0]) / 2, (y[1] - y[0]) / 2, width=0.0005)


def set_plot_limits(data, delta=0.01):
    max_lat = data['latDeg'].max()
    min_lat = data['latDeg'].min()

    max_lon = data['lonDeg'].max()
    min_lon = data['lonDeg'].min()

    plt.ylim(min_lon - delta, max_lon + delta)
    plt.xlim(min_lat - delta, max_lat + delta)


def load_data(filename):
    names = ['nodeType', 'latDeg', 'lonDeg', 'altMeters', 'parcelWtLbs']
    data = pd.read_csv(filename, names=names, skiprows=1, index_col=0)
    return data

def draw_points(data):
    deliveriable_points_by_drones = get_deliveriable_points_by_drones(data)
    not_deliveriable_points_by_drones = get_not_deliveriable_points_by_drones(data)

    # Plot the deposit
    plt.scatter(data.iloc[0]['latDeg'], data.iloc[0]['lonDeg'], marker='^', s=150, color='black')

    # Plot the deliveriable point by drones
    plt.scatter(deliveriable_points_by_drones['latDeg'], deliveriable_points_by_drones['lonDeg'], color='green')

    # Plot the not deliveriable point by drones (only trucks)
    plt.scatter(not_deliveriable_points_by_drones['latDeg'], not_deliveriable_points_by_drones['lonDeg'], marker='s', color='red')


# Settings of pyplot
plt.rcParams["figure.figsize"] = (20, 10)

# Load data
df = load_data('problems/example.csv')

# Plot limits
set_plot_limits(df)

# Plot 
draw_points(df)

# TSP Route
tsp_route_points = get_tsp_points(df)
print(tsp_route_points)

draw_tsp_route(df, tsp_route_points)

plt.show()


