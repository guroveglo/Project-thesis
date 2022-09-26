from audioop import tostereo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from math import sqrt

# OBS: had to comment out 'dic[keymap.all_axes]' line in events.py to get the code to run 

if __name__ == '__main__':

    import seacharts
    
    size = 9000, 5062
    center = 44300, 6956450
    enc = seacharts.ENC(border=True)
    	
    # (id, easting, northing, heading, color)
    ships = [
        (1, 46100, 6957000, 132, 'orange'),
        (2, 45000, 6956000, 57, 'yellow'),
        (3, 44100, 6957500, 178, 'red'),
        (4, 42000, 6955200, 86, 'green'),
        (5, 44000, 6955500, 68, 'pink'),
    ]

    enc.add_vessels(*ships)

    import shapely.geometry as geo

    x, y = center
    width, height = 1900, 1900
    box = geo.Polygon((
        (x - width, y - height), 
        (x + width, y - height),
        (x + width, y + height),
        (x - width, y + height),
    ))
    areas = list(box.difference(enc.seabed[10].geometry))
    enc.draw_polygon(enc.seabed[100].geometry[-3], 'cyan')    # depth of 100
    enc.draw_polygon(enc.shore.geometry[56], 'highlight')
    for area in areas[3:8] + [areas[14], areas[17]] + areas[18:21]:
        enc.draw_polygon(area, 'red')
    enc.draw_rectangle(center, (width, height), 'pink', fill=False,
                       edge_style=(0, (10, 10)), thickness=1.5)

    enc.save_image('example1', extension='svg')

    enc.show_display()
    
    