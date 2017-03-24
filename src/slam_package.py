__author__ = "Sergio Noriega Heredia"
__date__ = "$Mar 21, 2017 1:49:55 PM$"

from math import *
from tkinter import *
from time import sleep

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

def belongs(item,list):#Checks if the given item belongs to a list.
    result=False
    for i in list:
        if item==i:
            result=True
            break
    return result
        
def to_polar(tup):#Converts cartesian tuple into polar
    return [sqrt(pow(abs(tup[0]),2)+pow(abs(tup[1]),2)), atan(tup[1]/tup[0])]

def to_cartesian(tup):#Converts polar tuple into cartesian
    return [tup[0]*cos(tup[1]), tup[0]*sin(tup[1])]

def objective_completed(objective,position):
    return distance(objective,position)<3
    
if __name__ == "__main__":
    ##INITIALIZATION##
    active_objective=0
    pan=(200,200)###Constant
    position=[100,-10]
    velocity=[0,0]
    position_mode="standard"
    
    
    ##ACTIVITY VARIABLES##
    defined_walls=[
    ((0,0),(70,0)),
    ((110,0),(180,0)),
    ((180,0),(180,70)),
    ((180,110),(180,180)),
    ((0,0),(0,70)),
    ((0,110),(0,180)),
    ((0,180),(70,180)),
    ((110,180),(180,180))
    ]                       #List of walls to avoid
    obstacles=[
    ]                       #List obstacles to avoid
    for new_obstacle in defined_walls:
        if not belongs(new_obstacle[0], obstacles): obstacles.append(new_obstacle[0])
        if not belongs(new_obstacle[1], obstacles): obstacles.append(new_obstacle[1])
    wanted_dummies=[]       #List of dummies to get to
    objectives=[
    (100,100),
    (200,100),
    (300,100),
    (50,100)
    ]                       #List of objectives to go to
    
    
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
    canvas.update()
    
    
    ##MAIN LOOP##
    while True:
        #Velocity Calculation#
        new_velocity=[0,0]
        new_velocity=add_vectors(new_velocity, inertia_vector(2, 0.5, position, objectives[active_objective]))
        for vobs in obstacles:
            new_velocity=add_vectors(new_velocity, inertia_vector(-5, 2, position, vobs))
        velocity=new_velocity
        canvas.itemconfigure(text_velocity,text="velocity: "+str(velocity))
        canvas.itemconfigure(text_angle,text="angle: "+str(calculate_angle((0,0), velocity))+" rad")
        
        #Position Calculation#
        canvas.delete(graphical_position)
        graphical_position=canvas.create_oval(pan[0]+position[0]-2,screen_size[1]-(pan[1]+position[1]-2), pan[0]+position[0]+2,screen_size[1]-(pan[1]+position[1]+2), fill="red")
        if position_mode=="standard":
            position[0]+=velocity[0]
            position[1]+=velocity[1]
        elif position_mode=="acquire":
            print("Acquiring position...")
        canvas.itemconfigure(text_position,text="Position: "+str(position))
        
        #Objectives Calculation#
        if objective_completed(objectives[active_objective], position):
            active_objective+=1
            canvas.delete(graphical_objective)
            dobj=objectives[active_objective]
            graphical_objective=canvas.create_oval(pan[0]+dobj[0]-4,screen_size[1]-(pan[1]+dobj[1]-4), pan[0]+dobj[0]+4,screen_size[1]-(pan[1]+dobj[1]+4), fill="blue")
            
        #Obstacles#
        sensor_input=0,0
        if(not belongs(sensor_input, obstacles)):
            #If it does not remember that obstacle, it adds it to the obstacles section and the screen.
            obstacles.append(sensor_input)
            canvas.create_oval(pan[0]+sensor_input[0]-2,screen_size[1]-(pan[1]+sensor_input[1]-2), pan[0]+sensor_input[0]-2,screen_size[1]-(pan[1]+sensor_input[1]-2), fill="black")
        sleep(1/60)
        canvas.update()
    canvas.mainloop()