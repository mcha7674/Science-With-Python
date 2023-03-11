import numpy as np
from matplotlib import pyplot as plt
import orbit
import render

############### Sub Routines ##################
def VelYGeneral(e, distFromSun, planetMass):
    return np.sqrt(orbit.Orbit.G*orbit.Orbit.M) * np.sqrt((1-e)/(distFromSun*(1+e))*(1+planetMass/orbit.Orbit.M))

def CalcPrecessAngle(x, r):
    return np.arccos(x / r) * (180/np.pi)  # Convert angle from radians to degrees with 180/pi

def plotOrbit(data:dict, xlim = (-1, 1), ylim = (-1, 1), showPlot = True, savePlot = False, saveName = "orbitPlot.png", showAphelionPoints = True):
    fig, ax = plt.subplots(1,1, figsize = (9, 9))
    ax.scatter(data["x"], data["y"], s = 0.2, lw=0, marker='.')
    # Aphelion points
    if showAphelionPoints:
        ax.scatter(data["xAphelion"], data["yAphelion"], s = 50, marker = '.', label = "Aphelion Point(s)")
        ax.legend()
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

def plotPrecessionAngleVsTime(data:dict, showPlot = True, savePlot = False, saveName = "AngleVsTime.png"):
    fig, ax = plt.subplots(1,1, figsize = (12, 9))
    ax.scatter(data["periodPoints"], data["precessAngle"], s = 100, lw=0, marker='.', color = "red")
    ax.set_title("Precession angle Over time ( Just the first 180 degrees )")
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Precession Angle (Degrees From Start Position)")
    # Line Fit
    dTheta, b = np.polyfit(data["periodPoints"], data["precessAngle"], deg=1)
    data["precessAngleRate"] = dTheta
    ax.plot(data["periodPoints"], dTheta*np.array(data["periodPoints"]) + b, c="green", linestyle="--", label ="({0:.3f})x + {0:.3f}".format(dTheta, b))
    ax.legend()
    if showPlot:
        plt.show()
    if savePlot:
        plt.savefig(saveName)

def OrbitCalculations(orbit:orbit.Orbit, data:dict, t):
    # Get Data for Aphelion Points. 
    if orbit.isAtAphelion(): 
        if not orbit.finishedPeriod:
            data["xAphelion"].append(orbit.x)
            data["yAphelion"].append(orbit.y)
            precessionAngle = CalcPrecessAngle(orbit.x, orbit.r)
            # only store precession angles for the first 180 degrees
            if (precessionAngle - data["precessAngle"][len(data["precessAngle"]) - 1] >= 0):
                data["precessAngle"].append( CalcPrecessAngle(orbit.x, orbit.r) )
                data["periodPoints"].append( t )
            orbit.finishedPeriod = True
    if orbit.isAtPerihelion():
        orbit.finishedPeriod = False
    orbit.StepOrbit()
############################################################

# Initiating time variables
duration = 5.0 # years
dt = 0.0001

# Physics Modifiers
B = 2.0 # Beta exponent in the Force equation
#a = 0.00001 # relativistic alpha term
# Starting parameters
# earth starting parameters
earth = orbit.Body(0.001, 3.00273e-6)
e = 0
x0 = 1

v0y_Circ = VelYGeneral(e, x0, earth.mass)
startVel = (0, v0y_Circ) # AU/yr
startPos = (x0, 0) # In AU
# Orbit Instance for Earth
myOrbit2 = orbit.Orbit(earth, startPos, startVel, dt, B)
# mercury starting parameters
mercury = orbit.Body(0.0001, 1.65913e-7)
e = 0.206
x0 = 0.39*(1+e)
v0y = VelYGeneral(e, x0, earth.mass)
startVel = (0, v0y) # AU/yr
startPos = (x0, 0) # In AU


# Create Orbit instance for Mercury
myOrbit1 = orbit.Orbit(mercury, startPos, startVel, dt, B)


##### Orbit data calculations #####
data = {"x":[], "y":[], "xAphelion":[], "yAphelion":[], "precessAngle":[0], "periodPoints":[0], "t":[], "precessAngleRate":0}
# Calculate and store Orbit Data into "data" dictionary
t = 0
for tick in range(int(duration/dt)):
    data["t"].append(t)
    data["x"].append(myOrbit1.x)
    data["y"].append(myOrbit1.y)
    OrbitCalculations(myOrbit1, data, t)
    t+=dt
plotOrbit(data, showPlot=False, savePlot = False, showAphelionPoints = True)
plotPrecessionAngleVsTime(data, showPlot=False)
print("Rate of angle precession is: ", data["precessAngleRate"], "degrees per year" )
render.Animate(myOrbit1, dt = dt, skips = 30)

##### calculate precession rate over several relativistic alpha factors #####
# duration = 2
# dt = 0.0001
# alpha = np.linspace(0.0001, 0.002, 5)
# startVel = (0, v0y) # AU/yr
# startPos = (x0, 0) # In AU
# dThetaArr = []
# for a in alpha:
#     data = {"x":[], "y":[], "xAphelion":[], "yAphelion":[], "precessAngle":[0], "periodPoints":[0], "t":[], "precessAngleRate":0}
#     t = 0
#     myOrbit1 = orbit.Orbit(mercury, startPos, startVel, dt, 2, a)
#     for tick in range(int(duration/dt)):
#         data["t"].append(t)
#         data["x"].append(myOrbit1.x)
#         data["y"].append(myOrbit1.y)
#         OrbitCalculations(myOrbit1, data, t)
#         t+=dt
#     dTheta, b = np.polyfit(data["periodPoints"], data["precessAngle"], deg=1)
#     dThetaArr.append(dTheta)


# plt.scatter(alpha, dThetaArr)
# dThetaDot, b = np.polyfit(alpha, dThetaArr, deg=1)
# print(dThetaDot)
# plt.plot(alpha, dThetaDot*alpha + b, linestyle = "--", color = "red")
# plt.show()

