import numpy as np
from matplotlib import pyplot as plt
import orbit
import render

############### Sub Routines ##################
def VelYforCircOrbit(distFromSun):
    return 2 * np.pi * np.sqrt(orbit.Orbit.M / distFromSun)
def VelYGeneral(e, distFromSun, planetMass):
    return np.sqrt(orbit.Orbit.G*orbit.Orbit.M) * np.sqrt((1-e)/(distFromSun*(1+e))*(1+planetMass/orbit.Orbit.M))

def plotOrbit(xlim = (-1, 1), ylim = (-1, 1), showPlot = True, savePlot = False, saveName = "orbitPlot.png"):
    fig, ax = plt.subplots(1,1, figsize = (9, 9))
    ax.scatter(x, y, s = 0.2, lw=0, marker='.')
    # Draw Sun
    ax.scatter(0,0, color = "gold", s = 500, marker='.')
    # Plot will resize such that the orbit will always seem circular if my figure width and height are equal
    # To prevent this, simply anchor the plot size to a set value
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(ylim[0], ylim[1])
    if showPlot:
        plt.show()
    if savePlot:
        plt.savefig(saveName)

############################################################

# Initiating Variables
duration = 20.0 # years
dt = 0.0001
e = 0.206
x0 = 0.39*(1+e)
# Initiate Orbiting planet
earth = orbit.Body(0.001, 3.00273e-6)
mercury = orbit.Body(0.0001, 1.65913e-7)
startPos = (x0, 0) # In AU
v0y_Circ = VelYforCircOrbit(np.sqrt(startPos[0]**2 + startPos[1]**2))
v0y = VelYGeneral(e, x0, earth.mass)
startVel = (0, v0y) # AU/yr
B = 2.1
# Create my Orbit
myOrbit1 = orbit.Orbit(mercury, startPos, startVel, dt, B)
# Initiate Data Collection Variables
x = []
y = []
# Calculate Orbit Data
for tick in range(int(duration/dt)):
    x.append(myOrbit1.x)
    y.append(myOrbit1.y)
    myOrbit1.StepOrbit()

plotOrbit(showPlot=True)
myOrbit2 = orbit.Orbit(mercury, startPos, startVel, dt, B)
render.Animate(myOrbit2, dt = dt, skips = 30)