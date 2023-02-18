from matplotlib import pyplot as plt
import numpy as np
import math
# My Files - ## MAJOR SUBROUTINES ##
import Bifurcation as bf
import Generations as gen
import Lyapunov as lp

# Starting Constants
x0 = 0.5
rMin = 2.8
rMax = 3.9
rStep = 0.001
iters = 200
######## PART A ########
""" Theory
The X-Axis of the bifurcation diagram is the 'r' value which
represents the rate of growth for the system. We assume the sytem to 
be a population of some animal for ease of explanation.

When a population of animal first is instantiated, the population of the
next generations will vary wildly at first until finally stabalizing to
1 or more population sizes each successive generation IF the rate of growth
r is at a reasonable level.

HOWEVER, at a certain rate, the population siezes to oscillate/stabalize to
a series of values and instead begins permutating widly with no pattern. It
has entered Chaos, occuring around r = 3.57

The Bifurcation Diagram allows to witness the oscillation of generations
after stabalizing, which double in their oscillations as we increase r. 

If we dont let the populations stabalize before plotting the points however,
we will plot what are known as 'Transients' which are the intermediate values
present in the first few generations (The wild phase). 
"""
# Creating And Plotting the Bifurcation diagram
# No Transients
def PartA(disableCalculations = False, showPlots = False, savePlots = False):
    if (not disableCalculations):
        print("Executing Part A Plots and Calculations")
        Xn, r = bf.Bifurcation(x0, rMin, rMax, rStep, iters, includeTransients= False)
        # With Transients
        XnTrans, rTrans = bf.Bifurcation(x0, rMin, rMax, rStep, iters, includeTransients= True)
        # Plotting
        bf.plotBifurcation(r, Xn, markerSize=0.1, xLimLeft=r[0], showPlot = showPlots,  savePlot=savePlots, title="Bifurcation Diagram - Transients Removed") 
        bf.plotBifurcation(rTrans, XnTrans, markerSize=0.1, xLimLeft=r[0],  showPlot = showPlots, savePlot=savePlots, 
                        saveName = "Plots/Bifurcation.png", title="Bifurcation Diagram - Transients Kept")
        # Calculate FeigenBaum Constant - Constants Found Analythically
        periodPoints = {"r32":3.568, "r16":3.564, "r8":3.544, "r4":3.449, "r2":3.001}
        def calcFiegenBaum(periodPoints):
            return  (periodPoints["r16"] - periodPoints["r8"])/(periodPoints["r32"] - periodPoints["r16"]) 
        feigenbaum = calcFiegenBaum(periodPoints)
        print("Approximation of Feigenbaum Constant: ", feigenbaum) # gets about 5 which is close enough

PartA(disableCalculations = True, showPlots=False, savePlots=False)
######### Part B #############
""" Theory
The Xn1 vs Xn Diagrams don't tell you much until
you introduce CobWebbing (The trajectories).
By Introducing trajectories, one is able to visualize successive
generations. 

If The main function is starting at a higher N (a later generation),
the trajectories show Nth successive generations everytime The Cobweb draw a line
from the identity to a point on the function. 

Essentially, Each step of the trajectory from the Identity line to the main function
is going from previous generation to the (previous generation + Nth Generation).

So the trajectories allow us to visualize successive generations (Xn+N), with a Higher order
starting function allowing each trajectory step to jump further generations.
"""
###### PART C ######
""" Theory
The Intersections with the lines demonstrate points where 
the last generation equals the next generation!

For whichever generation we plot, the stable points of the trajectories
for a given r value and initial condition will be the same.

The Stable Points are always along intersections with the Identity line at higher
Generations. This makes sense because after a million generations, the population will stabalize
so that the last generation equals the next generation, it does not vary!
"""
def PartBAndC(disableCalculations = False, showPlots = False, savePlots = False, x0 = 0.5):
    iterations = 10000
    if not disableCalculations:
        print("Executing Part B and C Plots and Calculations")
        r = 2.9
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 4)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 10)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 100)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 100)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1000)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        
        print("-"*10)
        print("Stable Intersection Coordinates for r = {}".format(r))
        gen.printIntersectCoordsAndDerivatives(genData2["idX"])
        
        print("-"*10)

        r = 3.3
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 4)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 10)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 100)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 100)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1000)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        r = 3.5
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 4)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}x0{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"]), str(x0)))
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 10)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 100)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"])))
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 100)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1000)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"])))
        
        print("-"*10)
        print("Stable Intersection Coordinates for r = {}".format(r))
        gen.printIntersectCoordsAndDerivatives(genData2["idX"])
        print("-"*10)

        r = 3.6
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 4)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"])))
        r = 3.8
        genData1 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 1)
        genData2 = gen.Generations(r, iters=iterations, x0=x0, showTraj = True, startGen = 4)
        gen.plotGensSideBySide(genData1, genData2, showPlot = showPlots, savePlot= savePlots, 
            saveName = "Plots/GenerationPlots{}N{}.png".format(int(r*10), str(genData1["N"])+str(genData2["N"])))
        
        print("-"*10)
        print("Stable Intersection Coordinates for r = {}".format(r))
        gen.printIntersectCoordsAndDerivatives(genData2["idX"])
        print("-"*10)

PartBAndC(disableCalculations = True, showPlots=False, savePlots=False)

###### PART D - LYPANOV ######
""" Theory
The Lyapunov Exponent is a quantity that characterizes the RATE OF SEPERATION
of INFINITESIMALLY CLOSE TRAJECTORIES.

lambda = (1/n)*ln|dn/d0| 

where n is the generation, dn is the infinitesimal
change in the nthe generation and d0 is an infinitesimal change in the
initial generation.

Another way to express the equation is as follows:

|dn| = |d0|e^(lambda*n) = f^n(x0 + d0) - f^n(x0)  for Large n.

which states that the magnitude of a 
tiny change in the nth generation value is exponentially
proportional to the generation number n at large n (regime of chaos). 
Where we can see if lambda is positive, dn explodes (Chaos).
If lambda is negative However, ( f^n(x0 + d0) - f^n(x0) ) converges to 0 
(i.e, tiny change in initial conditions has little to no effect on the outcome,
f^n(x0 +d0) = f^n(x0) -> The Identity Line!-> Where all the stable points fall into!)

So a negative or positive lambda corresponds to stability and chaos respectively.

To find lambda, It will just be the SLOPE of the following equation:

ln|dn/d0| = lambda * n
-> ln|dn| - ln|d0| = lambda *n
-> ln|dn| = lambda * n - ln|d0|

So we just have to plot ln|dn| vs n, do a best fit line, and the slope of that
line is the lyapunov constant!!!

"""
def PartD(disableCalculations = False, showPlots = False, savePlots = False):

    if not disableCalculations:
        iters = 40
        x0 = 0.2
        dx0 = 0.00001
        r = 3.3
        (n, deltaArray1) = lp.Lyapunov(r, iters, x0, dx0)
        r = 3.8
        (n, deltaArray2) = lp.Lyapunov(r, iters, x0, dx0)
        lp.plotLyapunov(n, deltaArray1, deltaArray2, showPlot = showPlots, savePlot = savePlots, saveName="Plots/Lyapunov.png")

PartD(disableCalculations = False, showPlots = True, savePlots = False)

