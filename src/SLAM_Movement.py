__author__ = "Sergio Noriega Heredia"
__date__ = "$Mar 21, 2017 1:49:55 PM$"

from math import *
from tkinter import *
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

def make_obstacle_line(wall,list):
    if(distance(wall[0],wall[1])<20):
        if not wall[0] in list:
            list.append(wall[0])
        if not wall[1] in list:
            list.append(wall[1])
    else:
        middle=middle_point(wall[0], wall[1])
        make_obstacle_line((middle, wall[0]), list)
        make_obstacle_line((middle, wall[1]), list)
    
if __name__ == "__main__":
    ##INITIALIZATION##
    active_objective=0
    pan=(100,100)###Constant
    position=[100,-10]
    direction=pi/2
    velocity=[0,0]
    max_velocity=0.5
    mode="normal"


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
    ###Black Hole Walls
    ((245,90),(270,115)),
    ((245,90),(270,65)),
    ###Moveable
    ((110,270),(180,280)),
    ((110,270),(180,260))
    ]                       #List of walls to avoid
    obstacles=[
    ]                       #List obstacles to avoid
    black_holes=[
    (270,90)
    ]
    for new_obstacle in defined_walls: make_obstacle_line(new_obstacle, obstacles)
    wanted_dummies=[
    
    ]       #List of dummies to get to
    
    
    objectives=[
    (90,90),
    (180,90),
    (200,90),
    (300,90),
    "scan",
    "return",
    "delete_route",
    (90,270),
    
    (90,-30)
    ]                       #List of objectives to go to
    route=[]
    
    ##SCREEN RELATED STUFF##
    screen_size=(500,500)###CONSTANT
    frame=Frame(width=screen_size[0],height=screen_size[1])
    frame.pack()
    canvas=Canvas(frame,width=screen_size[0],height=screen_size[1])
    canvas.pack()
    graphical_position=canvas.create_oval(pan[0]+position[0]-2,screen_size[1]-(pan[1]+position[1]-2), pan[0]+position[0]+2,screen_size[1]-(pan[1]+position[1]+2), fill="red")
    text_position=canvas.create_text(200,10,text="Position: "+str(position))
    text_velocity=canvas.create_text(200,20,text="velocity: "+str(velocity),fill="blue")
    text_angle=canvas.create_text(200,30,text="angle: "+str(velocity),fill="brown")
    dobj=objectives[0]
    graphical_objective=canvas.create_oval(pan[0]+dobj[0]-4,screen_size[1]-(pan[1]+dobj[1]-4), pan[0]+dobj[0]+4,screen_size[1]-(pan[1]+dobj[1]+4), fill="blue")
    for dobs in obstacles:
        canvas.create_oval(pan[0]+dobs[0]-2,screen_size[1]-(pan[1]+dobs[1]-2), pan[0]+dobs[0]+2,screen_size[1]-(pan[1]+dobs[1]+2), fill="brown")
    for w in defined_walls:
        canvas.create_line(pan[0]+w[0][0],screen_size[1]-pan[1]-w[0][1],pan[0]+w[1][0],screen_size[1]-pan[1]-w[1][1])
    for b in black_holes:
        canvas.create_oval(pan[0]+b[0]-25,screen_size[1]-(pan[1]+b[1]-25), pan[0]+b[0]+25,screen_size[1]-(pan[1]+b[1]+25), fill="black")
    canvas.update()
    
    
    ##MAIN LOOP##
    while not len(objectives)==0:
        if mode=="normal":    
            #Velocity Calculation#
            new_velocity=velocity
            new_velocity=add_vectors(new_velocity, inertia_vector(1, 0.5, position, objectives[active_objective]))
            for vobs in obstacles:
                new_velocity=add_vectors(new_velocity, inertia_vector(-50, 3, position, vobs))
            new_velocity=add_vectors(new_velocity, inertia_vector(-100, 2, position, black_holes[0]))
            new_velocity=to_polar(new_velocity)
            #print(new_velocity)
            if new_velocity[0]>max_velocity: new_velocity[0]=max_velocity
            new_velocity=to_cartesian(new_velocity)
            velocity=new_velocity
            canvas.itemconfigure(text_velocity,text="velocity: "+str(to_polar(velocity)))

            #Position Calculation#
            canvas.delete(graphical_position)
            graphical_position=canvas.create_oval(pan[0]+position[0]-2,screen_size[1]-(pan[1]+position[1]-2), pan[0]+position[0]+2,screen_size[1]-(pan[1]+position[1]+2), fill="red")
            position[0]+=velocity[0]
            position[1]+=velocity[1]
            direction=calculate_angle((0,0), velocity)
            canvas.itemconfigure(text_position,text="Position: "+str(position))
            canvas.itemconfigure(text_angle,text="angle: "+str(direction)+" rad")
        elif(mode=="scan"):
            False
        
        #Objectives Calculation#
        if not len(objectives)==0:
            if type(objectives[active_objective])==tuple:
                mode="normal"
                canvas.delete(graphical_objective)
                if objective_completed(objectives[active_objective], position):
                    route.append(objectives.pop(0))
                    print("Objective Completed")
                    print(str(route))
                else:
                    dobj=objectives[active_objective]
                    graphical_objective=canvas.create_oval(pan[0]+dobj[0]-4,screen_size[1]-(pan[1]+dobj[1]-4), pan[0]+dobj[0]+4,screen_size[1]-(pan[1]+dobj[1]+4), fill="blue")
            if(objectives[active_objective]=="scan"):
                ###CODE FOR SCANNING IS MISSING HERE!
                objectives.pop(0)
                mode="scan"
                print("Scanned")
            elif(objectives[active_objective]=="return"):
                objectives.pop(0)
                for r in range(len(route)):
                    objectives.insert(0,route[r])
                mode="normal"
                print("Returing route "+str(route))
            elif(objectives[active_objective]=="delete_route"):
                objectives.pop(0)
                route=[]
                print(route)
        else:
            print("Finished!")

        #Obstacles#
        sensor_input=0,0
        if(not sensor_input in obstacles):
            #If it does not remember that obstacle, it adds it to the obstacles section and the screen.
            obstacles.append(sensor_input)
            canvas.create_oval(pan[0]+sensor_input[0]-2,screen_size[1]-(pan[1]+sensor_input[1]-2), pan[0]+sensor_input[0]-2,screen_size[1]-(pan[1]+sensor_input[1]-2), fill="black")
        sleep(1/25)
        canvas.update()
    
    canvas.mainloop()
    