import os
import math
import random
import numpy as np
import time
import Vector

def bearingMeasurement(dx, dy):
    a = math.atan2(dx,dy)
    a = a*(a>=0) + (a+2*math.pi)*(a<0)
    return round(a*(180/math.pi),1)

def makedir(DIR):
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def chunker(seq, size):
    return [seq[pos:pos + size] for pos in xrange(0, len(seq), size)]

def readFile2List(textFile):
    with open(textFile, "r") as file:
        data = []
        for line in file.readlines():
            data.append([float(i) for i in line.split()])
    return data

def writeList2File(textFile, DATA):
    with open(textFile, "w") as file:
        DATA = '\n'.join('\t'.join(map(str,j)) for j in DATA)
        file.write(DATA)

def linspace(start, end, step=1, sigfigs=1, type="+"):
    array = []
    temp = start
    if type == "+":
        while round(temp,sigfigs) <= round(end,sigfigs):
            array.append(round(temp,sigfigs))
            temp += step
    if type == "-":
        while round(temp,sigfigs) >= round(end,sigfigs):
            array.append(round(temp,sigfigs))
            temp -= step
    return array

def size(x):
    return int(round((0.0333*x) + 3.3333, 0))

def lowerLimit(value, minimum):
    return max(minimum, value)

def upperLimit(value, maximum):
    return min(maximum, value)

def limit(value, minimum, maximum):
    return max(minimum, min(maximum, maximum-value))

def mapValue(OldValue, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)
    NewRange = (NewMax - NewMin)
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

def polygon(sides, radius, offset=None):
    if offset == None:
        offset = Vector.Vector([0, 0])
    points = [[radius*math.sin(2*math.pi*float(i/sides))+offset.x, radius*math.cos(2*math.pi*float(i/sides))+offset.y] for i in linspace(1,sides)]
    points.append(points[0])
    points = np.array(points)
    return points

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)
