import numpy as np
import matplotlib.pyplot as plt

"""
This function allows us to map a value
in the -L/2 -> L/2 range to a 0 -> N matrix value 
for grid placement
"""
def map(value:int, N:int, L:int):
    dx = L/N
    if np.abs(value) == L//2:
        if value > 0:
            return int((value + L//2)/dx) +1
    return int((value + L//2)/dx)
    

# Define constants
N = 150 # number of grid points in each dimension - RESOLUTION
L = 10 # size of the square area
q = 2 # charge of the point source
# Set Charge Positions in the (within -L/2 to L/2 Range)
x1 = -1
x2 = 1
y1 = -1
y2 = 1
# Calculate charge density
rho = np.zeros((N, N)) # generate a 2d NxN matrix of zeroes
# Note the double slash operator is division that rounds to an integer
# set the middle element to the charge density, where L/N is dx
rho[N//2, map(x1, N, L)] = q / (L/N)**2 
rho[N//2, map(x2, N, L)] = q / (L/N)**2 
rho[map(y1, N, L), N//2] = q / (L/N)**2 
rho[map(y2, N, L), N//2] = q / (L/N)**2 

# Define initial guess for electric potential ( all zeros )
V = np.zeros((N, N))
# Iterate until convergence
maxiter = 10000
tolerance = 1e-8
for iteration in range(maxiter):
    Vold = V.copy()
    # Only update the slice of V that is not the edges ( V on edges has boundary condition of 0)
    # each value in the slice represents the start row or column, negatives meaning the nth row/col from the right hand side.
    # Here since V is a 2d matrix,
    V[1:-1, 1:-1] = (V[1:-1, 0:-2] + V[1:-1, 2:] + V[0:-2, 1:-1] + V[2:, 1:-1] + rho[1:-1, 1:-1] * (L/N)**2) / 4
    # below, a dV grid is created in which we take the maximum dv in that grid.
    # if the max dv value is smaller than tolerance, we have relaxed the Potential grid!
    if np.max(np.abs(V - Vold)) < tolerance:
        break
# Plot electric potential using imshow
plt.imshow(V, cmap='inferno', extent=[-L/2, L/2, -L/2, L/2], alpha=1.0)
ax = plt.gca() # get current axes
# set Ticks
ax.set_xticks(np.arange(-L//2, L//2 +1, 1));
ax.set_yticks(np.arange(-L//2, L//2 + 1, 1));
plt.colorbar()
plt.title('Electric Potential of Point Charges')
plt.xlabel('x')
plt.ylabel('y')
plt.show()