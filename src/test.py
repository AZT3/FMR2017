from math import *

def calculate_angle(vector1, vector2):
    x=vector2[0]-vector1[0]
    y=vector2[1]-vector1[1]
    if x==0: x=0.000001
    angle=atan(y/x)
    if x<0: angle+=pi
    if angle<0: angle+=2*pi
    return angle

def to_polar(tup):#Converts cartesian tuple into polar
    return [sqrt(pow(abs(tup[0]),2)+pow(abs(tup[1]),2)), calculate_angle((0,0),tup)]

if __name__ == "__main__":
    print(type((90,90)) == tuple)
