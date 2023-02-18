import numpy as np
from matplotlib import pyplot as plt


def LogisticMap(x0, r):
    return (r*x0)*(1-x0)

def LogisticMapDerivative(x0, r):
    return r-2*r*x0


def Bifurcation(x0, rMin, rMax, dr, iters = 150, includeTransients = False):
    Xn = []
    R = []
    rArr = np.linspace(rMin, rMax, int(1/dr))
    for r in rArr:
        xn = x0
        # Calculate Several generations first before adding data
        for i in range(iters):
            xn = LogisticMap(xn, r)
            # only start adding once a certain number of iterations occur (Let Points Stabalize)
            if includeTransients:
                Xn.append(xn)
                R.append(r)
            elif i > (int(iters/2)) and not includeTransients:
                Xn.append(xn)
                R.append(r)

    return (Xn, R)


def getStablePoints(r, Xn):
    stablePoints = {"r":[], "Xn":[]}
    pass


# Plots
def plotBifurcation(r, Xn, showPlot = True, savePlot = False, saveName = "Plots/Bifurcation.png", 
                    xLimLeft = 2.0, xLimRight = 4.0, yLimBottom = 0.0, yLimTop = 1.0,
                    title = "Bifurcation Diagram", xLabel = "r", yLabel = "X*", markerSize = 0.5, closePlot = True, color = "black"):
    #Plot Bifurcation - use subplots because marker sizes go smaller as well
    plt.subplots(figsize = (23, 13))
    plt.scatter(r, Xn, s = markerSize, marker = '.', linewidth = 0, c = color)
    plt.ylim(bottom = yLimBottom, top= yLimTop)
    plt.xlim(left = xLimLeft, right = xLimRight)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    if showPlot:
        plt.show()
    elif savePlot:
        plt.savefig(saveName)
    if closePlot:
        plt.close()
