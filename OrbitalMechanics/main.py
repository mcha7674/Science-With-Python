import pygame
import numpy as np
def WorldToScrCoords(worldX, worldY, 
                     worldWidth, worldHeight, 
                     scrWidth, scrHeight):
    scrX = scrWidth/worldWidth * worldX
    scrY = scrHeight/worldHeight * worldY
    return (scrX, scrY)

def main():
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    WORLD_WIDTH = 100
    WORLD_HEIGHT = 100
    # initialize pygame
    pygame.init()
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
        # Logic updates
        x = 10 *np.cos(t * dt) + 50
        y = 10 *np.sin(t * dt) + 50
        # Graphics Rendering
        rectPosX, rectPosY = WorldToScrCoords(x,y,WORLD_WIDTH, WORLD_HEIGHT, 
                                              SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(displaySurface, (230,120,100),
                          pygame.Rect(rectPosX,rectPosY,50,50))

        pygame.display.flip() # buffer swapping
        # update the clock, argument is the frame rate.
        # computes how many milliseconds passed since previous call
        # provided argument will delay the loop to keep it within 60 frames per second
        clock.tick(60) # wait until next frame at 60 fps
        t += 1



if __name__ == "__main__":
    main()