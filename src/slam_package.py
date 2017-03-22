__author__ = "Sergio Noriega Heredia"
__date__ = "$Mar 21, 2017 1:49:55 PM$"

from math import *
from tkinter import *
from time import sleep

def distance(tup1,tup2):#Gives the distance between two tuples
    return sqrt(pow(abs(tup1[0]-tup2[0]),2)+pow(abs(tup1[1]-tup2[1]),2))

def belongs(item,list):#Checks if the given item belongs to a list.
    result=False
    for i in list:
        if item==i:
            result=True
            break
    return result
        
def to_polar(tup):#Converts cartesian tuple into polar
    return (sqrt(pow(abs(tup[0]),2)+pow(abs(tup[1]),2)), arctan(tup[1]/tup[0]))

def to_cartesian(tup):#Converts polar tuple into cartesian
    return (tup[0]*cos(tup[1]), tup[0]*sin(tup[1]))
    
if __name__ == "__main__":
    ##SCREEN RELATED STUFF##
    screen_size=(201,201)###CONSTANT
    frame=Frame(width=screen_size[0],height=screen_size[1])
    frame.pack()
    canvas=Canvas(frame,width=screen_size[0],height=screen_size[1])
    canvas.pack()
    
    ##INITIALIZATION##
    pan=(50,50)
    position=[0,0]
    inittial_direction=pi/2
    velocity=[1,inittial_direction]
    obstacles=[] #[(x,y) for x in range(100) for y in range(100)]
    graphical_position=canvas.create_oval(pan[0]+position[0]-2,screen_size[1]-(pan[1]+position[1]-2), pan[0]+position[0]+2,screen_size[1]-(pan[1]+position[1]+2), fill="red")
    print(graphical_position)
    
    ##MAIN LOOP##
    canvas.update()
    for i in range(200):
        #Position
        
        canvas.move(graphical_position, velocity[0]*cos(velocity[1]), -velocity[1]*sin(velocity[1]))
        position[0]+=velocity[0]*cos(velocity[1])
        position[1]+=velocity[0]*sin(velocity[1])
        print(str(position))
        #graphical_position=canvas.create_oval(pan[0]+position[0]-2,screen_size[1]-(pan[1]+position[1]-2), pan[0]+position[0]+2,screen_size[1]-(pan[1]+position[1]+2), fill="red")
        
        #Obstacles
        sensor_input=(30,30)
        if(not belongs(sensor_input, obstacles)):
            #If it does not remember that obstacle, it adds it to the obstacles section and the screen.
            print("Not in obstacles yet."+str(sensor_input))
            obstacles.append(sensor_input)
            canvas.create_oval(pan[0]+sensor_input[0]-2,screen_size[1]-(pan[1]+sensor_input[1]-2), pan[0]+sensor_input[0]-2,screen_size[1]-(pan[1]+sensor_input[1]-2), fill="black")
        sleep(1/10)
        canvas.update()