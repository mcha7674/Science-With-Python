import numpy as np
from matplotlib import pyplot as plt
import orbit
import render
import pygame
import os.path
from pathlib import Path

def VelYforCircOrbit(distFromSun):
    return 2 * np.pi * np.sqrt(orbit.Orbit.M / distFromSun)
def VelYGeneral(e, distFromSun, planetMass):
    return np.sqrt(orbit.Orbit.G*orbit.Orbit.M) * np.sqrt((1-e)/(distFromSun*(1+e))*(1+planetMass/orbit.Orbit.M))
def plotOrbit():
    # Initiating Variables
    duration = 20.0 # years
    dt = 0.0001
    e = 0.206
    x0 = 0.39*(1+e)
    # Initiate Orbiting planet
    earth = orbit.Body(0.001, 3.00273e-6)
    startPos = (x0, 0) # In AU
    v0y_Circ = VelYforCircOrbit(np.sqrt(startPos[0]**2 + startPos[1]**2))
    v0y = VelYGeneral(e, x0, earth.mass)
    startVel = (0, v0y_Circ) # AU/yr
    B = 2.5
    # Initiate Orbit
    myOrbit1 = orbit.Orbit(earth, startPos, startVel, dt, B)
    # Initiate Data Collection Variables
    x = []
    y = []
    # Calculate Orbit Data
    for tick in range(int(duration/dt)):
        x.append(myOrbit1.x)
        y.append(myOrbit1.y)
        myOrbit1.StepOrbit()

    plt.figure(figsize=(9,9))
    plt.scatter(x, y, s = 0.1)
    plt.scatter(0,0,color = "gold", s = 500)
    # Plot will resize such that the orbit will always seem circular if my figure width and height are equal
    # To prevent this, simply anchor the plot size to a set value
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.show()

plotOrbit()









# ANIMATION

def Render():
    pygame.init()
    # font stuff
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 30)
    text_surface = my_font.render('Some Text', False, (100, 100, 100))
    # init window for display - THIS IS OUR SURFACE
    displaySurface = pygame.display.set_mode((render.SCREEN_WIDTH, render.SCREEN_HEIGHT))
    
    # Clock object to track time
    clock = pygame.time.Clock()
    # Orbit
    t = 0
    # Initiating Variables
    dt = 0.0001
    e = 0.206
    x0 = 0.39*(1+e)
    # Initiate Orbiting planet
    earth = orbit.Body(0.001, 3.00273e-6)
    startPos = (x0, 0) # In AU
    v0y_Circ = VelYforCircOrbit(np.sqrt(startPos[0]**2 + startPos[1]**2))
    v0y = VelYGeneral(e, x0, earth.mass)
    startVel = (0, v0y_Circ) # AU/yr
    B = 2.5
    # Initiate Orbit
    myOrbit1 = orbit.Orbit(earth, startPos, startVel, dt, B)

    # REndering properties
    sunDims = (100, 100)
    planetDims = (50, 50)
    posCache = [render.WorldToScrCoordsNeg(startPos[0], startPos[1])]
    sunFile = Path(__file__).parent / Path("planetSprites/Sun.png")
    SUN_IMAGE = pygame.image.load(sunFile.resolve()).convert_alpha()
    SUN_IMAGE = pygame.transform.scale(SUN_IMAGE, sunDims)
    planetFile = Path(__file__).parent / Path("planetSprites/Earth.png")
    PLANET_IMAGE = pygame.image.load(planetFile.resolve()).convert_alpha()
    PLANET_IMAGE = pygame.transform.scale(PLANET_IMAGE, planetDims)
    # run Loop
    iters = 0
    while True:
        displaySurface.fill("black")
        text_surface = my_font.render('t = {0:.3f} years'.format(t), False, (100, 100, 100))
        displaySurface.blit(text_surface, (50,0))
        # player input processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            # Sun
        x, y = render.WorldToScrCoordsNeg(0,0)
        displaySurface.blit(SUN_IMAGE,(x- sunDims[0]/2, y- sunDims[1]/2))
        # planet
        myOrbit1.StepOrbit()
        x, y = render.WorldToScrCoordsNeg(myOrbit1.x, myOrbit1.y)
        posCache.append((x, y))
        displaySurface.blit(PLANET_IMAGE,(x - planetDims[0]/2, y - planetDims[1]/2))
        # draw trail
        pygame.draw.lines(displaySurface, (255,255,255), False, posCache)
        # if (iters > 1/dt): 
        #     posCache = [(x, y)]
        #     iters = 0
        t+=dt
        iters+=1

        pygame.display.flip() # buffer swapping

Render()