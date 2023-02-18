import matplotlib.pyplot as plt 
import math as m


####################Initialization of variables#######################
global consts 
consts = {"m":43, "rad":0.0775, "C":0.25, "rho":1.29, "g":9.81, "dt":0.01, "v0":830, "a": 6.5*(10**(-3)), "alpha": 2.5}
########################Interpolate Defining##############################

def interpolate(Xn,Xn1, Yn, Yn1):
    # using interpolation formula
    r = -1 * (Yn / Yn1)
    xl = (Xn + r * Xn1) / (r + 1)
    return xl

def oneTrajectory(theta, T,  drag = True, adiabatic = False):
    data = {"x":[], "y": [], "v": [], "t": [], "range":0, "angle":theta, "flightTime":0, "maxH":0}
    # run the while loop and fill up the trajData!
    vx = consts["v0"] * m.cos(m.radians(theta))
    vy = consts["v0"] * m.sin(m.radians(theta))
    v = consts["v0"]
    x = 0
    y = 0
    t = 0
    while y >= 0:
        # adding initial data to arrays
        data["x"].append(x)
        data["y"].append(y)
        data["v"].append(v)
        data["t"].append(t)
        # calculating new data
        if drag:
            rho = consts["rho"] # a copy of rho0
            # if adiabatic, then change rho to its dynamic version
            if adiabatic: rho = consts["rho"]*((1-((consts["a"]*y)/T))**(consts["alpha"]))  #changes rho if we choose adiabatic
            B = (.5)*consts["C"]*rho*(m.pi*(consts["rad"]**2)) #drag constant
            x = x + vx*consts["dt"]     #This section deals with position
            y = y + vy*consts["dt"] 
            vx = vx - (B/consts["m"])*v*vx*consts["dt"] 
            vy = vy - (B/consts["m"])*v*vy*consts["dt"]  - consts["g"]*consts["dt"]    #This section deals with velocity
            v = m.sqrt((vx)**2 + (vy)**2)    
        else: # no drag code:
            x = x + vx*consts["dt"]    #This section deals with no drag
            y = y + vy*consts["dt"]
            vx = vx
            vy = vy - consts["g"]*consts["dt"]   #This section deals with velocity
            v = m.sqrt((vx)**2 + (vy)**2) 
        #find max height and range
        if y > data["maxH"]:
            data["maxH"] = y
        t += consts["dt"]    # move to the next point in time   
    #Out of loop, now determine maxR after interpolation
    R = interpolate(data["x"][len(data["x"]) - 2], data["x"][len(data["x"]) - 1], data["y"][len(data["y"]) - 2], data["y"][len(data["y"]) - 1] )
    data["x"][len(data["x"]) - 1] = R
    data["y"][len(data["y"]) - 1] = 0
    # set the range
    data["range"] = R
    # set the flight time
    data["t"] = t
    return data
    

def plot(x, y, name = "Trajectories", xLabel = "x", yLabel = "y", color = "black"):
    plt.plot(x,y, c = color, linestyle = "-")
    plt.title(name)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    

######### PART A #########
maxTraj = None
currMaxRange = 0
T = 280
for theta in range(40,50):
    data = oneTrajectory(theta, T, drag = False) # data is the dictionary returned by oneTrajectory
    # Okay we got our data for one of the trajectories, now do stuff with it!
    if data["range"] > currMaxRange: # find max Traj
        maxTraj = data  
    if theta % 5 == 0:
        # plot
        plot(data["x"], data["y"])
# plot max Traj
plot(maxTraj["x"], maxTraj["y"], color = "red")
#plot max traj no drag
plt.show()

######### PART B #########
plot(maxTraj["t"], maxTraj["v"], color = "red")
plt.show()
######### PART C #########
######### PART D #########



