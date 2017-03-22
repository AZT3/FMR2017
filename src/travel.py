from tkinter import *
from random import *
from time import *

def fact(x):
    y=1
    while x!=1:
        y=y*x
        x-=1
    return y
def distance(tuple1,tuple2):
    return ((tuple1[0]-tuple2[0])**2+(tuple1[1]-tuple2[1])**2)**(1/2)
def getx(spots,x):
    return spots[x][0]
def gety(spots,y):
    return spots[y][1]
def minimumS(list):
    min=float("inf")
    for i in list:
        if i<min and i!=0:
            min=i
    return min
def checkPolygon(log,i,path):
    newPath=path
    log[i]=path
    maxLen=len(log)
    state=False
    while state==False and maxLen!=1:
        i=newPath
        newPath=log[i]
        if newPath==float("inf"):
            break
        if newPath==path:
            state=True
        maxLen-=1
        #print(i)
    return state

def main():
    frame=Frame(width=500,height=500)
    frame.pack()
    canvas=Canvas(frame,width=500,height=500)
    canvas.pack()
    numSpots=500
    spots=[(randint(1,500),randint(1,500))for i in range(numSpots)]
    #print(spots)
    for i in range(numSpots):
        canvas.create_oval(getx(spots,i)-1,gety(spots,i)-1,getx(spots,i)+1,gety(spots,i)+1,fill="black")
        canvas.create_text(getx(spots,i),gety(spots,i)-10,text=str(i))
        canvas.update()
    ###EXPERIMENTAL###
    distances=[[distance(spots[i],spots[j])for i in range(numSpots)]for j in range(numSpots)]
    distances2=[[distance(spots[i],spots[j])for i in range(numSpots)]for j in range(numSpots)]
    #print(distances)
    keeper=[]
    usedLines=[float("inf") for i in range(numSpots)]
    for i in range(numSpots):
        while True:
            #print(str(minimumS(distances[i]))+"in"+str(distances[i]))
            goto=distances2[i].index(minimumS(distances[i]))
            if keeper.count(goto)==1 or usedLines[i]==goto:
                print("deleted "+str(i)+"to"+str(goto)+" path")
                distances[i].remove(minimumS(distances[i]))
            elif checkPolygon(usedLines,i,goto)==True:
                print("deleted "+str(i)+"to"+str(goto)+" polygon")
                distances[i].remove(minimumS(distances[i]))
            else:
                usedLines[i]=goto
                keeper.append(goto)
                print(str(i)+"to"+str(goto))
                #print(usedLines)
                canvas.create_line(getx(spots,i),gety(spots,i),getx(spots,goto),gety(spots,goto))
                canvas.update()
                break

#if __name__ == '__main__':
    main()
    sleep(10)
