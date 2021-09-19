import pandas as pd
import matplotlib.pyplot as plt

def get_deliveriable_points_by_drones(data):
    filtered_data = df[(df['nodeType'] != 0) & (df['altMeters'] == 0) & (df['parcelWtLbs'] <= 5)]
    return filtered_data

def get_not_deliveriable_points_by_drones(data):
    filtered_data = df[(df['nodeType'] != 0) & ((df['altMeters'] != 0) | (df['parcelWtLbs'] > 5))]
    return filtered_data

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
plt.ylim(min_lon + delta, max_lon + delta)
plt.xlim(min_lat + delta, max_lat + delta)

deliveriable_points_by_drones = get_deliveriable_points_by_drones(df)
not_deliveriable_points_by_drones = get_not_deliveriable_points_by_drones(df)

# Plot the deposit
plt.scatter(df.iloc[0]['latDeg'], df.iloc[0]['lonDeg'], marker='^', s=150)

# Plot the deliveriable point by drones
plt.scatter(deliveriable_points_by_drones['latDeg'], deliveriable_points_by_drones['lonDeg'])

# Plot the not deliveriable point by drones (only trucks)
plt.scatter(not_deliveriable_points_by_drones['latDeg'], not_deliveriable_points_by_drones['lonDeg'], marker='s')

plt.show()


