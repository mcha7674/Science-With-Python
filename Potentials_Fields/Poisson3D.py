import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def map(value:int, N:int, L:int):
    dx = L/N
    if np.abs(value) == L//2:
        if value > 0:
            return int((value + L//2)/dx) +1
    return int((value + L//2)/dx)

# Define the grid size and number of points
L = 3
N = 50
q = 2

x = np.linspace(-L/2, L/2, N)
y = np.linspace(-L/2, L/2, N)
z = np.linspace(-L/2, L/2, N)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Define the charge distribution
x1 = -1
x2 = 1
y1 = -1
y2 = 1
z1 = -1
z2 = 1
# Calculate charge density
rho = np.zeros_like(X) # generate a 2d NxN matrix of zeroes
# Note the double slash operator is division that rounds to an integer
# set the middle element to the charge density, where L/N is dx
rho[N//2, map(x1, N, L), N//2] = q / (L/N)**3 
rho[N//2, map(x2, N, L), N//2] = q / (L/N)**3 
rho[map(y1, N, L), N//2, N//2] = q / (L/N)**3 
rho[map(y2, N, L), N//2, N//2] = q / (L/N)**3


# Define the electric potential
V = np.zeros_like(X)
tolerance = 1e-4
max_iterations = 10000
for i in range(max_iterations):
    V_new = np.zeros_like(V)
    V_new[1:-1, 1:-1, 1:-1] = (V[:-2, 1:-1, 1:-1] + V[2:, 1:-1, 1:-1]
                                + V[1:-1, :-2, 1:-1] + V[1:-1, 2:, 1:-1]
                                + V[1:-1, 1:-1, :-2] + V[1:-1, 1:-1, 2:]
                                + (L/N)**2 * rho[1:-1, 1:-1, 1:-1]) / 6
    if np.max(np.abs(V - V_new)) < tolerance:
        V = V_new
        break
    V = V_new

# Plot the electric potential
fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-L/2, L/2)
ax.set_ylim(-L/2, L/2)
ax.set_zlim(-L/2, L/2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('V')
# X and Y are sliced at z = N//2, Z axis
surf = ax.plot_surface(X[:,:,N//2], Y[:,:,N//2], V[:,:,N//2], rstride=1, cstride=1, cmap='inferno', alpha=0.8)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
