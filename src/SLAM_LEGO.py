#!/usr/bin/env python3
__author__ = "Sergio Noriega Heredia"
__date__ = "$Mar 21, 2017 1:49:55 PM$"

from math import *
from time import sleep
from lego_module import *

def distance(tup1,tup2):#Gives the distance between two tuples
    return sqrt(pow(abs(tup1[0]-tup2[0]),2)+pow(abs(tup1[1]-tup2[1]),2))

def inertia_vector(factor, distance_exponent, vehicle_position, object_position):
    dist=distance(vehicle_position,object_position)
    if dist==0: dist=0.000001
    inertia=factor/pow(dist,distance_exponent)
    return to_cartesian((inertia,calculate_angle(vehicle_position, object_position)))

def calculate_angle(vector1, vector2):
    x=vector2[0]-vector1[0]
    y=vector2[1]-vector1[1]
    if x==0: x=0.000001
    angle=atan(y/x)
    if x<0: angle+=pi
    if angle<0: angle+=2*pi
    return angle

def add_vectors(vector1,vector2):
    return [vector1[0]+vector2[0],vector1[1]+vector2[1]]
        
def to_polar(tup):#Converts cartesian tuple into polar
    return [sqrt(pow(abs(tup[0]),2)+pow(abs(tup[1]),2)), calculate_angle((0,0),tup)]

def to_cartesian(tup):#Converts polar tuple into cartesian
    return [tup[0]*cos(tup[1]), tup[0]*sin(tup[1])]

def objective_completed(objective,position):
    return distance(objective,position)<3

def middle_point(point1,point2):
    return [(point2[0]+point1[0])/2,(point2[1]+point1[1])/2]

def make_obstacle_line(wall,list,safe_distance):
    if(distance(wall[0],wall[1])<safe_distance):
        if not wall[0] in list:
            list.append(wall[0])
        if not wall[1] in list:
            list.append(wall[1])
    else:
        middle=middle_point(wall[0], wall[1])
        make_obstacle_line((middle, wall[0]), list, safe_distance)
        make_obstacle_line((middle, wall[1]), list, safe_distance)
    
if __name__ == "__main__":
    ##INITIALIZATION##
    safe_distance=5
    active_objective=0
    position=[110,-10]
    direction=pi/2
    rotation_start=0
    velocity=[0,0]
    max_velocity=0.5
    mode="normal"
    home=(90,-30)
    route_home=[home]
    route_arena1=[(90,90),(180,90)]
    route_arena2=[(90,90),(90,180)]
    target_dummie=1
    ####BLACK=1
    ####WHITE=6
    lego=lego_init()

    ##ACTIVITY VARIABLES##
    defined_walls=[
    ((0,0),(70,0)),
    ((110,0),(360,0)),
    ((180,0),(180,70)),
    ((180,110),(180,360)),
    ((0,0),(0,70)),
    ((0,110),(0,360)),
    ((0,180),(70,180)),
    ((110,180),(360,180)),
    ((360,0),(360,180)),
    ((0,360),(180,360)),
    ###Moveable
    ((110,270),(180,270))
    ]                       #List of walls to avoid
    obstacles=[
    ]                       #List obstacles to avoid
    black_holes=[
    (270,90)
    ]
    for new_wall in defined_walls: make_obstacle_line(new_wall, obstacles, 4*safe_distance)
    dummies=[]              #List of dummies to get to
    objectives=[]           #List of objectives to go to
    objectives.extend(route_arena1)
    objectives.append("scan")
    
    objectives.extend(route_arena2)
    objectives.append("scan")
    
    objectives.extend(route_home)
    objectives.append("home")
    
    route=()
    
    ##MAIN LOOP##
    while not len(objectives)==0:
        seconds_running+=1/18
        #LEGO DEBUGGING#
        distance_to_object=ultra_input(lego["ultra_sensor"])
        legoradial_direction=gyro_input(lego["gyro_sensor"]*pi/180)
        sensor_input=add_vectors(to_cartesian([distance_to_object,radial_direction]),position)
        direction=gyro_input(lego["gyro_sensor"]*pi/180)
        color=color_input(lego["color_sensor"])
        
        if mode=="normal":    
            #Velocity Calculation#
            new_velocity=velocity
            new_velocity=add_vectors(new_velocity, inertia_vector(1, 0.5, position, objectives[active_objective]))
            for vobs in obstacles:
                new_velocity=add_vectors(new_velocity, inertia_vector(-100, 3, position, vobs))
            new_velocity=add_vectors(new_velocity, inertia_vector(-100, 2, position, black_holes[0]))
            new_velocity=to_polar(new_velocity)
            if(new_velocity[0]>max_velocity): new_velocity[0]=max_velocity
            new_velocity=to_cartesian(new_velocity)
            velocity=new_velocity
            motor_command(lego["motors"],to_polar(velocity),direction)
            
            #Position Calculation#
            if(distance_to_object>=60 or distance_to_object<=5):
                pass
            else:
                position[0]+=velocity[0]
                position[1]+=velocity[1]
                direction=calculate_angle((0,0), velocity)
            
        elif(mode=="scan"):
            if(distance_to_object<100 and distance_to_object>15):
                sensor_input=add_vectors(to_cartesian([distance_to_object,direction]),position)
                is_usable=True
                for comb1 in obstacles:
                    if(distance(comb1, sensor_input)<=safe_distance):
                        is_usable=False
                for comb2 in dummies:
                    if(distance(comb2, sensor_input)<=safe_distance):
                        is_usable=False
                if(distance(black_holes[0], sensor_input)<=25):
                        is_usable=False
                if(is_usable):
                    objectives.insert(1,"rescue")
                    objectives.insert(2,route)
                    dummies.append(tuple(sensor_input))
                    dobs=sensor_input
                    print("Dummie at "+str(sensor_input))
        
        #Objectives Calculation#
        if not len(objectives)==0:
            if type(objectives[active_objective])==tuple:
                mode="normal"
                if objective_completed(objectives[active_objective], position):
                    mode="evaluate"
                    route=objectives.pop(0)
                    rotation_start=direction
                    print("Objective Completed")
                else:
                    dobj=objectives[active_objective]
            elif(objectives[active_objective]=="scan"):
                if(rotation_start+2*pi<direction):
                    objectives.pop(0)
                    print("Scanned")
                else:
                    mode="scan"
            elif(objectives[active_objective]=="rescue"):
                objectives.pop(0)
                objectives.insert(0,dummies[0])
                objectives.insert(1,"check_color")
                dummies.pop(0)
            elif(objectives[active_objective]=="return"):
                objectives.pop(0)
                objectives.insert(0,route)
                mode="normal"
                print("Returning route "+str(route))
#            elif(objectives[active_objective]=="delete_route"):
#                objectives.pop(0)
#                route=[]
#                print("Deleted route")
            elif(objectives[active_objective]=="return_home"):
                objectives.pop(0)
                ###LEGO STUFF MISSING FOR UNLOADING
                for rh in route_home:
                    objectives.insert(0,rh)
            elif(objectives[active_objective]=="home"):
                objectives.pop(0)
                print(str(objectives))
            elif(objectives[active_objective]=="check_color"):
                objectives.pop(0)
                color=randrange(0,7)
                print("Checked color")
                if(color==1):
                    print("BLACK DUMMIE DETECTED")
                elif(color==5):
                    print("RED DUMMIE DETECTED")
                elif(color==6):
                    print("WHITE DUMMIE DETECTED")
                elif(color==0):
                    print("NOTHING DETECTED! - WARNING")
                else:
                    print("NO MATCH TO COLORS- WARNING")
                if(color==target_dummie):
                    #LEGO STUFF MISSING FOR LOADING
                    print("Dummie loaded")
                    objectives.insert(1,objectives[0])
                    objectives.insert(1,"return_home")
                    objectives.insert(2,(90,90))
        else:
            print("Finished!")
        sleep(1/25)
    