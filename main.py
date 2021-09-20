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
    tsp_route = [0] + tsp_route + [0]
    return tsp_route

def get_tsp_coords(data, tsp_route_points):
    lat_tsp = []
    lon_tsp = []

    for point in tsp_route_points:
        lat_tsp.append(data.iloc[point]['latDeg'])
        lon_tsp.append(data.iloc[point]['lonDeg'])

    return lat_tsp, lon_tsp


# Settings of pyplot
plt.rcParams["figure.figsize"] = (20, 10)

# Load data
names = ['nodeType', 'latDeg', 'lonDeg', 'altMeters', 'parcelWtLbs']
df = pd.read_csv('problems/example.csv', names=names, skiprows=1, index_col=0)

# Plot things
max_lat = df['latDeg'].max()
min_lat = df['latDeg'].min()

max_lon = df['lonDeg'].max()
min_lon = df['lonDeg'].min()

delta = 0.01
plt.ylim(min_lon - delta, max_lon + delta)
plt.xlim(min_lat - delta, max_lat + delta)



deliveriable_points_by_drones = get_deliveriable_points_by_drones(df)
not_deliveriable_points_by_drones = get_not_deliveriable_points_by_drones(df)

# Plot the deposit
plt.scatter(df.iloc[0]['latDeg'], df.iloc[0]['lonDeg'], marker='^', s=150, color='black')

# Plot the deliveriable point by drones
plt.scatter(deliveriable_points_by_drones['latDeg'], deliveriable_points_by_drones['lonDeg'], color='green')

# Plot the not deliveriable point by drones (only trucks)
plt.scatter(not_deliveriable_points_by_drones['latDeg'], not_deliveriable_points_by_drones['lonDeg'], marker='s', color='red')

# TSP Route
tsp_route_points = get_tsp_points(df)
print(tsp_route_points)

x, y = get_tsp_coords(df, tsp_route_points)
plt.plot(x, y, linewidth=1)

plt.show()


