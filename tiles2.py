import os
import math
import requests
from pathlib import Path
import bz2
from poly import parse_poly
import shapely

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
        resp = requests.get(f'http://localhost:8764/tiles/16/{x}/{y}.json')
        if resp.status_code == 200:
            return resp.content


def writeFile(x,y, text):
    if not Path(f'{x}').exists():
        os.mkdir(f'{x}')
    with bz2.open(f'{x}/{y}.json.bz2','w') as file:
        file.write(text)



