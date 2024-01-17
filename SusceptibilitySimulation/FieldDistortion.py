"""
Implementation based on:
PhD thesis Sunil Patil,
"Passive Tracking and System Interfaces for Interventional MRI"

This only simulates the magnetic field, without any intravoxel dephasing (MRI effects).
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Constants
B0 = 1.5  # Tesla
delta_chi = 0.05  # The susceptibility difference, this is an arbitrary value for visualization
V = 10  # The volume of the marker material, also arbitrary for visualization
x0 = y0 = z0 = 0  # The location of the marker material, assuming it's at the origin

# Define the grid for simulation
artifact_size = 1
artifact_resolution = 200
x = np.linspace(-artifact_size, artifact_size, artifact_resolution)
y = np.linspace(-artifact_size, artifact_size, artifact_resolution)
z = np.linspace(-artifact_size, artifact_size, artifact_resolution)
X, Y, Z = np.meshgrid(x, y, z)

# Calculate the field perturbation (Delta Bz)
# Using the equation provided in the screenshot
Delta_Bz = (B0 * delta_chi * V / (4 * np.pi)) * (X ** 2 + Y ** 2 - 2.2 * Z ** 2) / ((X ** 2 + Y ** 2 + Z ** 2) ** ( 2.5 ))

# Visualize the field perturbation in a 2D slice at z=0 (assuming symmetry along z-axis)
plt.figure(figsize=(8, 8))
graph_size = 10000

colors = [(0, (0.3, 0.3, 0.3)), (0.01, (0.25, 0.25, 0.25)), (0.11, (0.1, 0.1, 0.1)), (0.15, (0.3, 0.3, 0.3)), (0.17, (.3, .3, .3)), (0.3, (0.4, 0.4, 0.4)), (0.35, (0.1, 0.1, 0.1)), (1, (0.15, 0.15, 0.15))]
cmap_name = 'custom_colormap'
n_bins = 1000
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

noise_level = 1
noise = np.random.normal(0, noise_level, Delta_Bz.shape)
# Delta_Bz = Delta_Bz + noise

plt.imshow(np.rot90(Delta_Bz[:, 90, :]), extent=(-graph_size, graph_size, -graph_size, graph_size), cmap=custom_cmap, interpolation='none')
plt.colorbar(label='Field')
plt.title('Susceptibility Artifact')
plt.xlabel('x')
plt.ylabel('y')
plt.show()