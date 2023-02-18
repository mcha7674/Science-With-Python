import numpy as np
from matplotlib import pyplot as plt
import Bifurcation as bf
import math



def Lyapunov(r, iters = 40, x0 = 0.2, dx0 = 0.00001):
    y = [] # array of Delta Arrays (ln|dn| vs n), each array added to y is for a slightlydifferent initial condition
    dxSpace = np.linspace(dx0, dx0*10, iters)
    for dx in dxSpace:
        lnFor1dx = [] # array of deltas for n generations
        x01 = x0
        x02 = x01 + dx
        for n in range(iters):
            lnFor1dx.append(math.log(np.abs(x02 - x01)))
            x01 = bf.LogisticMap(x01, r)
            x02 = bf.LogisticMap(x02, r)
        # Append the ln{dXn} for n generations into the y array.
        y.append(lnFor1dx)
    # Averaging Step
    finalDeltaArray = []
    for i, deltaArray in enumerate(y): # size of dxSpace
        sum = 0
        for j, delta in enumerate(y[0]):
            sum += y[j][i] # sum up the ith element of each row j (each row is a differnt dx array)
        # add the average to the final delta array
        finalDeltaArray.append(sum/len(y[0])) 
    return range(iters), finalDeltaArray

# Plot Lyapunov
# Plots
def plotLyapunov(n, deltaArray1, deltaArray2, showPlot = True, savePlot = False, saveName = "Plots/Lyapunov.png", 
                    title = "Lyapunov Graph", xLabel = "n (Generations)", yLabel = "ln(dn/d0)", closePlot = True):
    
    plt.figure(figsize=(15,11))
    plt.plot(n, deltaArray1, c = "blue", label = "r = 3.3")
    a, b = np.polyfit(n, deltaArray1, 1) # a is the Lyapunov Constant!!
    plt.plot(n, a*n + b, c = "blue", linestyle = "--", label = "y = {}x + b".format(a))

    plt.plot(n, deltaArray2, c = "red", label = "r = 3.8")
    a, b = np.polyfit(n[0:int(len(n)/2)], deltaArray2[0:int(len(n)/2)], 1)
    plt.plot(n, a*n + b, c = "red", linestyle = "--", label = "y = {}x + b".format(a))

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()
    if showPlot:
        plt.show()
    elif savePlot:
        plt.savefig(saveName)
    if closePlot:
        plt.close()
