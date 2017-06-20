#!/usr/bin/env python3

__copyright__ = "Copyright 2017"
__version__ = "1.0.1"
__maintainer__ = "Christian Norfleet"
__email__ = "http://contact@deadlycheerio.com"
__repo__ = "https://github.com/cynorfleet/REPONAME"

""" Program 2 """

import pygame
import random
from dbscan import *
import sys
import os
import pprint as pp
import re
import csv
from itertools import cycle

# GLOBALS
DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
FILEPATHS = ['Nypd_Crime_01.csv']
TAGS = \
    'CMPLNT_NUM,CMPLNT_FR_DT,CMPLNT_FR_TM,CMPLNT_TO_DT,CMPLNT_TO_TM, RPT_DT,KY_CD,OFNS_DESC,PD_CD,PD_DESC,CRM_ATPT_CPTD_CD,LAW_CAT_CD,JURIS_DESC,BORO_NM,ADDR_PCT_CD,LOC_OF_OCCUR_DESC,PREM_TYP_DESC,PARKS_NM,HADEVELOPT,X_COORD_CD,Y_COORD_CD,Latitude,Longitude,Lat_Lon'.split(
        ',')
WINSIZE = {'x': 1000, 'y': 1000}


class CrimeDatabase:
    """
    Contains groupings of Crimes, their COLORS, and LOCATION
    """

    def __init__(self):
        self.db = {}

    def insertIntoDataBase(self, crime, crime_to_color, id):
        # for i in crime_to_color:
        acolor = crime_to_color[crime['OFNS_DESC']]

        if crime['OFNS_DESC'] not in self.db:
            self.db[crime['OFNS_DESC']] = [{
                'info': crime, 'color': acolor, 'id': id}]
        else:
            self.db[crime['OFNS_DESC']].append(
                {'info': crime, 'color': acolor, 'id': id})


class Report:
    """
    Contains LIST of incidents in DICTIONARY form
    """

    def __init__(self, paths):
        self.count = 0
        self.CDB = CrimeDatabase()
        self.min = {'x': 99999999999999.0, 'y': 99999999999999.0}
        self.max = {'x': -99999999999999.0, 'y': -99999999999999.0}
        self.records = []
        self.coords = []
        self.ERRORS = []
        self.DESC_To_COLOR_set = [()]
        self.DESC_set = []
        self.COLOR_set = []
        for path in paths:
            self.readData(path)
        while len(self.COLOR_set) < len(self.DESC_set):
            color = self.randColor()
            self.COLOR_set.append(color)
        self.DESC_To_COLOR_set = dict(
            zip(set(self.DESC_set), set(self.COLOR_set)))
        print('len of desc {}, len of color {}, len of desc-color {}'.format(
            len(self.DESC_set), len(self.COLOR_set), len(self.DESC_To_COLOR_set)))
        for id, entry in enumerate(self.records):
            self.CDB.insertIntoDataBase(entry, self.DESC_To_COLOR_set, id)

    def generateValues(self, offense, meta):
        for field in self.CDB.db[offense]:
            print('\ngenerating: {}\n'.format(field[meta]))
            return field[meta]

    def convertToNumeric(self, value):
        """
        Its order of conversion is INT, FLOAT, TUPLE in that order.
        The TUPLE returns a FLOAT pair.
        """
        rstring = '^.*\((\d+\.\d+,[ -]*\d+.\d+).*$'
        try:
            return int(value)
        except:
            try:
                return float(value)
            except:
                try:
                    match = re.match(rstring, value)
                    lon_lat_split = match.group(1).split(',')
                    value = (
                        float(lon_lat_split[0]), float(lon_lat_split[1]))
                    oldvalue = value
                    ischanged = self.ismin_max(value)
                    # if ischanged['chanied']:
                    # print('\nFound new min/max\n{}'.format(ischanged))
                    return value
                except:
                    return value

    def ismin_max(self, pair):
        change = {'changed': False}
        if pair[0] < self.min['x']:
            change['xmin'] = {'old': self.min['x'], 'new': pair[0]}
            change['changed'] = True
            self.min['x'] = pair[0]
        if pair[0] > self.max['x']:
            change['xmin'] = {'old': self.max['x'], 'new': pair[0]}
            change['changed'] = True
            self.max['x'] = pair[0]
        if pair[1] < self.min['y']:
            change['ymin'] = {'old': self.max['y'], 'new': pair[1]}
            change['changed'] = True
            self.min['y'] = pair[1]
        if pair[1] > self.max['y']:
            change['ymax'] = {'old': self.max['y'], 'new': pair[1]}
            change['changed'] = True
            self.max['y'] = pair[1]
        return change

    def scalePoints(self, incident):
        # if len(incident['Lat_Lon']) is not 2:
        #     print('incident ', incident['Lat_Lon'])
        x, y = incident['Lat_Lon']
        xpt = ypt = 'ERROR'
        try:
            xpt = ((x - self.min['x']) /
                   (self.max['x'] - self.min['x']) * WINSIZE['x'])
            ypt = (
                (1 - (y - self.min['y']) / (self.max['y'] - self.min['y'])) * WINSIZE['y'])
            return (xpt, ypt)
        except Exception as e:
            # print('**** SCALE ERROR\nx(in): {}\ny(in): {}\nx(out): {}\ny(out): {}\nINCIDENT: \n{}\n ****'.format(
                # x, y, xpt, ypt, incident))
            self.ERRORS.append(incident)
            return None

    def randColor(self):
        color = ['red', 'blue', 'green']
        for i, rgb in enumerate(color):
            color[i] = random.randint(0, 255)
        return tuple(color)

    def readData(self, path):
        """
        Reads files containg data and stores them as incident records
        """
        # read the data
        with open(DIRPATH + path) as csvfile:
            report = csv.DictReader(csvfile)

            for incident in report:
                for tag in incident:
                    incident[tag] = self.convertToNumeric(incident[tag])
                self.records.append(incident)

                if self.records[-1]['Lat_Lon'] is '' or \
                        self.records[-1]['OFNS_DESC'] is '':
                    del self.records[-1]
                else:
                    # print('sending ', self.records[-1])
                    scaled_pair = self.scalePoints(self.records[-1])
                    if scaled_pair is not None:
                        self.records[-1]['Lat_Lon'] = scaled_pair
                        self.DESC_set.append(self.records[-1]['OFNS_DESC'])


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters = dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs)
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    for id in range(len(clusters) - 1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs)
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x, min_y), (max_x, min_y),
                     (max_x, max_y), (min_x, max_y), (min_x, min_y)])
    return mbrs


def clean_area(screen, origin, width, height, color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox, oy = origin
    points = [(ox, oy), (ox + width, oy), (ox + width,
                                           oy + height), (ox, oy + height), (ox, oy)]
    pygame.draw.polygon(screen, color, points, 0)


if __name__ == "__main__":
    borough = {"MANHATTAN": (194, 35, 38),
               "QUEENS": (243, 115, 56),
               "STATEN ISLAND": (253, 182, 50),
               "BRONX": (2, 120, 120),
               "BROOKLYN": (128, 22, 56)}

    background_colour = (255, 255, 255)
    black = (0, 0, 0)
    (width, height) = (WINSIZE['x'], WINSIZE['y'])

    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption('Simple Line')
    screen.fill(background_colour)

    pygame.display.flip()

    epsilon = 20
    min_pts = 5.0

    points = []

    num_points = 500

    report = Report(FILEPATHS)
    # mbrs = calculate_mbrs(coords[:num_points], epsilon, min_pts)
    running = True
    print('xmin {}, xmax {}\nymin {} ymax {}'.format(
        report.min['x'], report.max['x'], report.min['y'], report.max['y']))
    while running:
        for offense in report.CDB.db:
            # print(offense)
            for record in report.CDB.db[offense]:
                # print(record)
                x, y = record['info']['Lat_Lon']
                # print('x: {} y: {}'.format(x,y))
                x = int(x)
                y = int(y)
                p = (x, y)
                color = borough[record['info']['BORO_NM']]
                pygame.draw.circle(screen, color, p, 3, 0)
        # for mbr in mbrs:
            # pygame.draw.polygon(screen, black, mbr, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(
                    screen, '.\\Assignments\\Program_2\\all_buroughs_screen_shot.png')
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen, (0, 0), width, height, (255, 255, 255))
                points.append(event.pos)
                mbrs = calculate_mbrs(points, epsilon, min_pts)
        pygame.display.flip()
