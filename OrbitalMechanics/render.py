import pygame
import numpy as np
from pathlib import Path
import orbit
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

def WorldToScrCoords(worldX, worldY, worldWidth, worldHeight):
    scrX = SCREEN_WIDTH/worldWidth * worldX
    scrY = SCREEN_HEIGHT/worldHeight * worldY
    return (scrX, scrY)
# span -worldx/2 to +worldx/2
def WorldToScrCoordsNeg(worldX, worldY, worldWidth, worldHeight):
    # convert world coordinates to one where origin is center
    transWorldX = worldX + worldWidth/2
    transWorldY = -1*worldY + worldHeight/2
    scrX, scrY = WorldToScrCoords(transWorldX, transWorldY, worldWidth, worldHeight)
    return (scrX, scrY)
    
def loadImage(relPath:str, scale = (1, 1)):
    file = Path(__file__).parent / Path(relPath)
    image = pygame.image.load(file.resolve()).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

# ANIMATION
# pass in the Orbit Object to Render which will animate the Object Created for the plots!
def Animate(orbitObj:orbit.Orbit, dt = 0.0001, skips = 1, worldWidth = 2, worldHeight = 2):
    pygame.init()
    clock = pygame.time.Clock()
    # font stuff
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 30)
    # init window for display - THIS IS OUR SURFACE
    displaySurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
    # REndering properties
    sunDims = ((SCREEN_WIDTH/worldWidth)/7, (SCREEN_WIDTH/worldWidth)/7)
    planetDims = (sunDims[0]/4, sunDims[1]/4)
    posCache = [WorldToScrCoordsNeg(orbitObj.x, orbitObj.y,worldWidth, worldHeight)]
    # Image Loading
    SUN_IMAGE = loadImage("planetSprites/Sun.png", sunDims)
    PLANET_IMAGE = loadImage("planetSprites/Earth.png", planetDims)
    # run Loop
    t = 0
    ogSkip = skips
    while True:
        displaySurface.fill("black")
        # Update Text Surface and display it
        stats_text = 'FPS = {0:.3f}'.format(clock.get_fps())
        worldDim_text = "World Scaling = {} AU".format(worldWidth)
        time_surface = my_font.render('t = {0:.3f} years'.format(t), False, (100, 100, 100))
        speed_surface = my_font.render('speed = {}'.format(skips), False, (100, 100, 100))
        worldDim_surface = my_font.render(worldDim_text, False, (100, 100, 100))
        stats_surface = my_font.render(stats_text, False, (100, 100, 100))
        displaySurface.blits([(time_surface, (20,0)), (stats_surface, (SCREEN_WIDTH - 200,0))])
        displaySurface.blit(speed_surface, (300, 0))
        displaySurface.blit(worldDim_surface, (SCREEN_WIDTH/2 - 110, SCREEN_HEIGHT - 50))
        # User input processing - all events go here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()  
                if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    if keys[pygame.K_UP]:
                        worldHeight +=1
                        worldWidth += 1
                    if keys[pygame.K_DOWN]:
                        worldHeight -= 1
                        worldWidth -= 1
                        if (worldWidth == 0):
                            worldHeight = 1
                            worldWidth  = 1
                    # Update planet and sun sizes as well as clear trail position cache 
                    # since world dimensions have been changed
                    sunDims = ((SCREEN_WIDTH/worldWidth)/7, (SCREEN_WIDTH/worldWidth)/7)
                    planetDims = (sunDims[0]/4, sunDims[1]/4)
                    SUN_IMAGE = loadImage("planetSprites/Sun.png", sunDims)
                    PLANET_IMAGE = loadImage("planetSprites/Earth.png", planetDims)
                    posCache.clear()
                if event.key == pygame.K_SPACE:
                    if skips == 0: skips = ogSkip
                    else:skips = 0 # Pause
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            skips += 1
            ogSkip = skips
        if keys[pygame.K_LEFT]:
            skips -= 1
            if skips < 1: skips = 1
            ogSkip = skips 
        # Step The Orbit
        for i in range(skips):
            orbitObj.StepOrbit()
            t+=dt
        ### RENDERING ###
        # Sun
        x, y = WorldToScrCoordsNeg(0,0, worldWidth, worldHeight)
        displaySurface.blit(SUN_IMAGE,(x- sunDims[0]/2, y- sunDims[1]/2))
        # Planet
        x, y = WorldToScrCoordsNeg(orbitObj.x, orbitObj.y, worldWidth, worldHeight)
        if (len(posCache) == 0):
            posCache.append((x, y)) # add another of the same point so no error occurs
        posCache.append((x, y))
        displaySurface.blit(PLANET_IMAGE,(x - planetDims[0]/2, y - planetDims[1]/2))
        # Planet Trail
        pygame.draw.lines(displaySurface, (100,100,100), False, posCache, 1)
        pygame.display.flip() # buffer swapping
        # delay 
        clock.tick(60)