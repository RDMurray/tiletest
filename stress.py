import os
import math
import requests
from pathlib import Path
import bz2
from poly import parse_poly
import shapely
import random

def osm_deg2num(lat_deg, lon_deg, zoom):                                        
    lat_rad = math.radians(lat_deg)                                             
    n = 2.0 ** zoom                                                             
    xtile = int((lon_deg + 180.0) / 360.0 * n)                                  
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)                                                              
    return (xtile, ytile)                                                       
                                                                                
# This returns the NW-corner of the square. Use the function with xtile+1 and/or ytile+1 to get the other corners. With xtile+0.5 & ytile+0.5 it will return the center of the tile.                                                            
def num2deg(xtile, ytile, zoom):                                                
    n = 2.0 ** zoom                                                             
    lon_deg = xtile / n * 360.0 - 180.0                                         
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))               
    lat_deg = math.degrees(lat_rad)                                             
    return (lon_deg, lat_deg)                                                   
 

def downloadTile(x,y):
    while(True):
        resp = requests.get(f'http://localhost:8080/tiles/16/{x}/{y}.json')
        if resp.status_code == 200:
            return resp.content
        raise(Exception("request failed)"))


def writeFile(x,y, text):
    if not Path(f'{x}').exists():
        os.mkdir(f'{x}')
    with bz2.open(f'{x}/{y}.json.bz2','w') as file:
        file.write(text)



poly = parse_poly(open('great-britain.poly','r').readlines())
poly=poly.buffer(0.003)
bounds=poly.bounds
tileTL = osm_deg2num(bounds[3],bounds[0], 16)
tileBR=osm_deg2num(bounds[1],bounds[2],16)
count=0
for i in range(1000000):
    if i%100 == 0:
        print(i)
    x = random.randrange(tileTL[0], tileBR[0])
    y = random.randrange(tileTL[1], tileBR[1])
    p=shapely.Point(num2deg(x+0.5,y+0.5,16))
    if not (poly.contains(p)):
        continue
    text=downloadTile(x,y)
    count += 1
print(count)



