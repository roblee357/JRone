## matplotlib tutorial 16 - Live graphs
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import mplleaflet
import csv
from matplotlib import pyplot as plt
from matplotlib import animation, rc
from IPython import display
from IPython.display import HTML
import time
import math
import matplotlib.animation as animation
import numpy as np
import itertools
from math import sqrt
from math import sin
from math import cos
from numpy import interp

fig = plt.figure()
ax = fig.add_subplot(111)
x,y,oX,oY = [],[],[],[]
data_tail =20
heading = 30
cHeading = 90 - heading
vAngle = 40
vDist = 0.00005
cameraAngle = 120 # degrees
detectionDistance = [2,300] # feet
deg2feet = 363972 #fix is a fuunction of longitude
dataRecord = True

def animate(i):
    ##
    ## Read Q500
    dX,dY = [],[]
    xOS,yOS = 0.0093513,0.3762786
    dataSource = '/home/ros/Desktop/Q500Stream/Q500log.txt'
    with open(dataSource) as f:
        reader = csv.reader(f)        
        for row in reader:
            dY.append(float(row[5]))
            dX.append(float(row[6]))
            dH = 360-int(float(row[12]))+90+19
        print(str(cHeading),'source')
    with open(dataSource,'r+') as f:
        something = 'somthing else'
        for xIt in range(data_tail):
            f.readline()
            i = i+1
        f.truncate(f.tell())
##    print(cHeading)

## Read ST10+
    oX,oY = [],[]
    xOS2,yOS2 = 0.0,0.0
    dataSource = '/home/ros/Desktop/ST10+Stream/ST10+_log.txt'
    with open(dataSource) as f:
        num_lines2 = sum(1 for line in f)
    #         print(str(num_lines2))
    if num_lines2 > 21:
        with open(dataSource) as f:
            beginning = [next(f) for x in range(num_lines2-data_tail)]
            beginning = [next(f) for x in range(data_tail)]
    reader = csv.reader(beginning)
    for row in reader:
        oY.append(float(row[6]))
        oX.append(float(row[8]))
        headingI = float(row[20])
        altl =  float(row[12])
    ##
    ##
    ## Read Lappy (tensorflow)
    tfX,tfY,tfW,tfH,bX,bY = [],[],[],[],[],[]
    dataSource = '/home/ros/Desktop/detectStream/detectLog.txt'
    with open(dataSource) as f:
##        f.readline()
##        lines = f.readlines()
##        print(str(len(lines)))
        readerL = csv.reader(f)   
        for row in readerL:
            tfX.append(abs(float(row[2]) ))
            tfY.append(abs(float(row[1]) ))
            tfW.append(abs(float(row[5]) ))
            tfH.append(abs(float(row[4][:7]) ))
#### Delete first line
    with open(dataSource) as f:
        f.readline()
        lines = f.readlines()
    #    if len(lines)>data_tail:
    with open(dataSource,'r') as f:
         for x3 in range(len(lines)-data_tail):
             next(f)
         newFile = f.readlines()
    with open(dataSource,'w') as f:
        for line in newFile:
            f.write(line)
            

        

##
## Make boggie offsets
    itr = 19
    bogieHeading = dH + tfX[itr] * cameraAngle -cameraAngle/2
    bogieDistance =  interp(tfW[itr],[.4,1],[300,2])/deg2feet #fix is not linear should be tan/arctan       
    bX = dX[itr] + bogieDistance * cos((bogieHeading/180)*math.pi)
    bY = dY[itr] + bogieDistance * sin((bogieHeading/180)*math.pi)
    line3 = str(bX) + ',' + str(bY)
    dataSource = '/home/ros/Desktop/bogieStream/bogieStream.txt'
    with open(dataSource, 'r') as f:
       iii=0

       for line in f:
             iii = iii + 1
       if iii > data_tail+1:
            with open(dataSource, 'r') as f:
                 for x4 in range(iii - data_tail-1):
                     f.readline()
                 for line in f:
                     content = f.readlines()
            with open(dataSource, 'w') as f:
                   try:
                       f.writelines(content)
                   except:
                        print('no content yet')
            with open(dataSource, 'a+') as f:
                    f.write(line3+'\n')
       else:
             with open(dataSource, 'a+') as f:
                 f.write(line3+'\n')
##
##
## Read Bogie Locations
    bX,bY = [],[]
    with open(dataSource) as f:
        readerB = csv.reader(f)
        for row in readerB:
            bX.append(float(row[0]))
            bY.append(float(row[1]))
        
## Record
    if dataRecord:
        dataSource = '/home/ros/Desktop/calStream/calRecord.txt'
        calVector = [dX[1],dY[1],dH,oX[1],oY[1],bX[1],bY[1],tfX[1],tfY[1],tfW[1],tfH[1]]
        with open(dataSource, 'a+') as f:
                        f.write(str(calVector)+'\n')

                        
    ax.clear()
    erX,erY = [dX[data_tail-1],oX[data_tail-1]],[dY[data_tail-1],oY[data_tail-1]]
    ax.plot(oX[:],oY[:],'bo',dX[:],dY[:],'g^',erX,erY,'k',bX[:],bY[:],'ro');
    

    #plt.plot(oX[:],oY[:],'ro',x[:],y[:],'g^',dx,dy,'k');
    plt.axes().set_aspect('equal')
    blue_patch = mpatches.Patch(color='blue',label='Operator')
    green_patch = mpatches.Patch(color='green',label='Drone')
    red_patch = mpatches.Patch(color='red',label='Person')
    plt.legend(handles=[blue_patch,green_patch,red_patch])
    #print(str(headingI))
    # add a wedge
    mPatches = []
    print(str(cHeading))
    wedgeD = mpatches.Wedge([dX[data_tail-1],dY[data_tail-1]], vDist, cHeading - vAngle, cHeading + vAngle, ec="none")
    mPatches.append(wedgeD)
##    wedgeI = mpatches.Wedge([oX[data_tail-1],oY[data_tail-1]], vDist, 90 - float(headingI) - vAngle, 90 - float(headingI)  + vAngle, ec="none")
##    mPatches.append(wedgeI)
    collection = PatchCollection(mPatches,cmap=plt.cm.hsv,alpha=0.3)
    ax.add_collection(collection)
    #print(str(len(x)))
    #print('uBlox pts: ' + str(num_lines) + ' iOS pts: ' + str(num_lines2))
    distance = sqrt((oX[data_tail-1] -tfX[data_tail-1])**2+(oY[data_tail-1]-tfY[data_tail-1])**2)*deg2feet
    # print('distance: ' + str(round(distance,2)))

im_ani = animation.FuncAnimation(fig, animate,interval = 1000)

plt.show()
