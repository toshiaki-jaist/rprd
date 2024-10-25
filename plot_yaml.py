import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the YAML file
file_path = "sample.yaml"
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)

# Extract x, y, and z coordinates from the 'groundtruth_ego' position
timestamps = []
x_vals = []
y_vals = []
z_vals = []
x_vals_npc = []
y_vals_npc = []
z_vals_npc = []

for state in data['states']:
    timestamps.append(state['timeStamp'])
    position = state['groundtruth_ego']['pose']['position']
    x_vals.append(position['x'])
    y_vals.append(position['y'])
#    z_vals.append(position['z'])
    position_npc = state['groundtruth_NPCs'][0]['pose']['position']
    x_vals_npc.append(position_npc['x'])
    y_vals_npc.append(position_npc['y'])
#    z_vals_npc.append(position_npc['z'])
   
# Create a 3D plot for x, y, and z positions
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

ax.plot(x_vals, y_vals, marker='o')
ax.plot(x_vals_npc, y_vals_npc, marker='o')

ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Plot of groundtruth_ego Positions')

plt.show()
