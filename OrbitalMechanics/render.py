import pygame
import numpy as np

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
WORLD_WIDTH = 2
WORLD_HEIGHT = 2

def WorldToScrCoords(worldX, worldY):
    scrX = SCREEN_WIDTH/WORLD_WIDTH * worldX
    scrY = SCREEN_HEIGHT/WORLD_HEIGHT * worldY
    return (scrX, scrY)
# span -worldx/2 to +worldx/2
def WorldToScrCoordsNeg(worldX, worldY):
    # convert world coordinates to one where origin is center
    transWorldX = worldX + WORLD_WIDTH/2
    transWorldY = -1*worldY + WORLD_HEIGHT/2
    scrX, scrY = WorldToScrCoords(transWorldX, transWorldY)
    return (scrX, scrY)


def Init():
    # initialize pygame
    pygame.init()
    

def run(Execute):
    # init window for display - THIS IS OUR SURFACE
    displaySurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Clock object to track time
    clock = pygame.time.Clock()
    # run Loop
    dt = 1/60
    t = 0
    while True:
        displaySurface.fill("black")
        # player input processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        
        Execute()

        pygame.display.flip() # buffer swapping
        # update the clock, argument is the frame rate.
        # computes how many milliseconds passed since previous call
        # provided argument will delay the loop to keep it within 60 frames per second
        clock.tick(60) # wait until next frame at 60 fps
        t += 1
