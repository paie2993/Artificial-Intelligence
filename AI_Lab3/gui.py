# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame
import time
from utils import *
from domain import *


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()


def movingDrone(currentMap, path, speed=SPEED, markSeen=MARK_SEEN):
    # animation of a drone on a path
    screen = initPyGame((currentMap.n * U, currentMap.m * U))

    drona = pygame.image.load("drona.png")

    # 'i' will denote the current position of the drone on the path
    for i in range(len(path)):
        screen.blit(image(currentMap), (0, 0))

        if markSeen:
            seenSquare = pygame.Surface((U, U))
            seenSquare.fill(GREEN)
            # at every outer loop iteration, the map, with the seen bricks, is repainted
            for j in range(i + 1):
                # move in the every direction and changing direction when brick encountered
                for var in v:
                    x = path[j][0]
                    y = path[j][1]
                    while (0 <= x < currentMap.n and                   # x coordinate inside map limits
                            0 <= y < currentMap.m and                  # y coordinate inside map limits
                            currentMap.surface[x][y] != 1):   # guard against moving on a brick
                        screen.blit(seenSquare, (y * U, x * U))
                        x = x + var[0]
                        y = y + var[1]

        screen.blit(drona, (path[i][1] * U, path[i][0] * U))
        pygame.display.flip()
        time.sleep(0.5 * speed)

    closePyGame()


def image(currentMap, brickColor=BLUE, backgroundColor=WHITE):
    # creates the image of a map
    imagine = pygame.Surface((currentMap.n * U, currentMap.m * U))
    brick = pygame.Surface((U, U))
    brick.fill(brickColor)
    imagine.fill(backgroundColor)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:           # if the algorithm iterates over a brick, paint it
                imagine.blit(brick, (j * 20, i * 20))

    return imagine
