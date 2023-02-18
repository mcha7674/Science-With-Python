import numpy as np
from matplotlib import pyplot as plt
import Bifurcation as bf


def Generations(r, iters = 1000, x0 = 0.05, showTraj = True, startGen = 1):
    data = {"Xn":[], "Xn1":[],"trajX":[x0], "trajY":[0],"idX":[], "idY":[], "N":startGen, "r": r, "x0":x0 }
    GenerationRange = np.linspace(0, 1, iters)
    for x in GenerationRange:
        xn1 = x
        for gen in range(startGen):
            xn1 = bf.LogisticMap(xn1, r)
        data["Xn1"].append(xn1)
        data["Xn"].append(x)
        """
        Intersections with identity occur when x = xn1, however, since both values
        are floats, I can't compare them explicitly (doing x == xn1) since that will always be false.
        Instead I must subtract each xn1 and xn value and if their difference is very small (like a threshold of 0.001),
        then They are close enough to approximately be xn == xn1, so we append to our intersect array!
        """
        if (abs((x - xn1)) < 0.0001):
            data["idX"].append(x)
            data["idY"].append(xn1)   

    # Calculate Trajectories
    if (showTraj):   
        x = x0
        for i in range(800):
            # append generation Coordinate
            data["trajX"].append(x)
            data["trajY"].append(bf.LogisticMap(x, r))
            # Append Identity Line COordinate (pluging into itself)
            # new Generation now Gets old Generation
            data["trajX"].append(bf.LogisticMap(x, r))
            data["trajY"].append(bf.LogisticMap(x, r))
            # Append Next Generation Coordinate
            data["trajX"].append(bf.LogisticMap(x, r))
            # The new Generation is used to calculate Next Generation
            x = bf.LogisticMap(x, r)
            data["trajY"].append(x) # GrandParent Generation of the original x
        # Rinse and repeat
    return data

# print Intersect values
def printIntersectCoordsAndDerivatives(idIntersectX):
    print("Intersection Coordinates: ")
    for i, val in enumerate(idIntersectX):
        if (i % 2 != 0):
            print("({0:.4f},{0:.4f})".format(val, val), end=" ")
            print("Derivative at Point: {}".format(bf.LogisticMapDerivative(val, val)))



# Plots
def plotGensSideBySide(data1, data2, lw = 0.8, markerSize = 100, showPlot = True, 
                       savePlot = False, saveName = "Plots/GenerationPlot.png"):
    
    fig, ax = plt.subplots(nrows =1, ncols = 2,figsize = (23, 10), sharex=True)
    ax[0].plot(data1["Xn"], data1["Xn1"])
    ax[0].plot(data1["Xn1"], data1["Xn1"])
    ax[0].plot(data1["trajX"], data1["trajY"], linewidth = lw)
    ax[0].scatter(data1["idX"], data1["idY"], s = markerSize, c = "red")
    ax[0].set_title("Logistic Map Trajectory @ r = {} N = {} x0 = {}".format(data1["r"], data1["N"], data1["x0"]))

    ax[1].plot(data2["Xn"], data2["Xn1"])
    ax[1].plot(data2["Xn1"], data2["Xn1"])
    ax[1].plot(data2["trajX"], data2["trajY"], linewidth = lw)
    ax[1].scatter(data2["idX"], data2["idY"], s = markerSize, c = "red")
    ax[1].set_title("Logistic Map Trajectory @ r = {} N = {} x0 = {}".format(data2["r"], data2["N"], data2["x0"]))
    if showPlot:
        plt.show()
    elif savePlot:
        plt.savefig(saveName)  
    plt.close()