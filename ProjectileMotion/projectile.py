from matplotlib import pyplot as plt
import math

# Subroutines (Functions)
def degreeToRads(angleDegrees):
    return math.radians(angleDegrees)
def interpolate(Xn,Xn1, Yn, Yn1):
    # using interpolation formula
    r = -1 * (Yn / Yn1)
    xl = (Xn + r * Xn1) / (r + 1)
    return xl

# declare constants
g = 9.81
theta0 = 10
dt = 0.01
x0 = 0
y0 = 0
v0 = 100
# Max Height and Range
maxH = 0
maxR = 0
maxTraj = {"x":[], "y":[], "a":0}
trajList = []
durationList = []
rangeList = []
heightList = []
vList = []
# Trajectory Loops
for theta in range(theta0, 120):
    # Dynamic Variables - reset after every angle step
    t = 0
    x = 0
    y = 0
    vx0 = v0 * math.cos(degreeToRads(theta))
    vy0 = v0 * math.sin(degreeToRads(theta))
    vy = vy0
    vx = vx0
    v = v0
    # Trajectory data arrays (will hold all my data)
    data = {"x":[], "y":[], "a":0, "flightTime":0, "range":0, "height":0, "v":0}
    # Create Trajectory
    while y >= 0: # while y is positive (projectile above ground)
        # Append this trajectory's data only if not negative
        data["x"].append(x)
        data["y"].append(y)
        # analytical  calculations of parameters ( valid for vaccum calculations)
        x = x + (vx * t)
        y = y + (vy * t) - (0.5 * g * t**2)
        vy = vy - (g * t)
        #vx = vx0
        v = math.sqrt(vx**2 + vy**2)
        # find max H and R
        if y > maxH:
            maxH = y
        # Increment t for next run
        t += dt
    data["a"] = theta
    data["v"] = v
    # Out of the trajectory loop, use interpolation function to final the new final x that corresponds to a y of 0.
    xFinal = interpolate(data["x"][len(data["x"])-2], data["x"][len(data["x"])-1], data["y"][len(data["y"])-2], data["y"][len(data["y"])-1])
    data["range"] = xFinal
    data["x"][len(data["x"])-1] = xFinal
    data["y"][len(data["y"])-1] = 0
    if xFinal > maxR: 
            maxR = xFinal
            maxTraj = data # IMPORTANT - if  the final x is the largest x so far, the data calculated is assigned to the 'maxRData' dictionary
    # once trajectory for that angle ends...
    # plot the acquired data ONLY if angle is increment of 5
    if theta % 5 == 0:
        plt.plot(data["x"], data["y"], label = "{} degrees".format(theta), alpha=0.45) # alpha parameter makes these more transparent
    trajList.append(data)
    durationList.append(t)

# Plotting #
plt.plot(maxTraj["x"], maxTraj["y"], c = "blue", label = "max Traj @ {} degrees".format(maxTraj["a"])) # plot the maximum trajectory in blue
# the plot functions below are to draw vertical and horizontal lines on the maximum Height and Range values.       
plt.hlines(maxH, 0, maxR/2, colors="red", label="max Height = "+"{0:.2f}".format(maxH), linestyles="dashed")
plt.vlines(maxR, 0, maxH/2, colors="orange", label="max Range = "+"{0:.2f}".format(maxR), linestyles="dashed")

plt.legend(loc = 1, prop = {'size':5}) # make a legend (makes a legend for all plots that have a LABEL)

plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")

plt.show()


plt.plot(range(10,120), durationList)
plt.show()