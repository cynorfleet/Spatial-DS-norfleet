
__copyright__ = "Copyright 2017"
__version__ = "1.0.1"
__maintainer__ = "Christian Norfleet"
__credit__= "Dr. Terry Griffin"
__email__ = "http://contact@deadlycheerio.com"
__repo__ = "https://github.com/cynorfleet/REPONAME"

""" Program 2 """


import get_quake_points
import adjust_quake_points
import pygame
import sys
import os
import json

DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
SAVEPATH = DIRPATH + 'quakedata.json'
ADJUSTPATH = DIRPATH + "quake-adjusted.json"
MAPPATH = DIRPATH + 'earthquake_map.png'
LOADINGbkg = DIRPATH + 'LOADING.jpg'


def clean_area(screen, origin, width, height, color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox, oy = origin
    points = [(ox, oy), (ox + width, oy), (ox + width,
                                           oy + height), (ox, oy + height), (ox, oy)]
    pygame.draw.polygon(screen, color, points, 0)


def convert_points(listofFloat):
    x, y, z = listofFloat
    return [int(x), int(y), int(z)][:2]


if __name__ == '__main__':
    """
    added loading img (48)
    called quake modules (53)
    changed open path (57)
    """
    pygame.font.init()
    font = pygame.font.SysFont("comicsansms", 72)

    background_colour = (255, 255, 255)
    black = (0, 0, 0)
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    screen.fill(background_colour)

    # Show Load Screen
    loadingbg = pygame.image.load(LOADINGbkg)
    screen.blit(loadingbg, (0, 0))
    pygame.display.flip()

    if not os.path.isfile(SAVEPATH):
        status ='Grabbing Data'
        pygame.time.wait(45)
        get_quake_points.execute(SAVEPATH, 1960, 7, endYr=2016)
        status = 'Data Grab Complete'
        status = 'Adjusting coordinates'
        adjust_quake_points.execute(SAVEPATH)
        status = 'Adjustment Complete'
    else:
        status = "Using previous data"

    f = open(ADJUSTPATH, 'r')
    points = json.loads(f.read())

    bg = pygame.image.load(MAPPATH)
    pygame.display.flip()

    running = True
    while running:
        screen.blit(bg, (0, 0))
        for p in points:
                # p = convert_points(p['geometry']['coordinates'])
                # print("Points are %s" % p)
            pygame.time.wait(10)
            pygame.draw.circle(
                screen, (255, 102, 0), p, 1, 0)
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.image.save(
                    screen, '.\\Assignments\\Program_3\\Quake.png')
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen, (0, 0), width,
                            height, (255, 255, 255))
