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
x,y,x2,y2 = [],[],[],[]
data_tail =20
heading = 30
cHeading = 90 - heading
vAngle = 40
vDist = 0.00005
cameraAngle = 120 # degrees
detectionDistance = [2,300] # feet
deg2feet = 363972 #fix is a fuunction of longitude
    
def animate(i):
    ##
    ## Read uBlox
    x,y = [],[]
    xOS,yOS = 0.0093513,0.3762786
    dataSource = '/home/ros/Desktop/uBloxStream/GPS_Delta_log.txt'
    with open(dataSource) as f:
        reader = csv.reader(f)        
        for row in reader:
            y.append(float(row[0])/100 + yOS)
            x.append(float(row[1])/-100 - xOS)
            heading = float(row[2])
    with open(dataSource,'r+') as f:
        something = 'somthing else'
        for xIt in range(data_tail):
            f.readline()
            i = i+1
        f.truncate(f.tell())
    ##
     ##
    ## Read iPhone
    x2,y2 = [],[]
    xOS2,yOS2 = 0.0,0.0
    dataSource = '/home/ros/Desktop/iPhoneStream/out/iPhone_Sensor_log.txt'
    with open(dataSource) as f:
        num_lines2 = sum(1 for line in f)
    #         print(str(num_lines2))
    if num_lines2 > 21:
        with open(dataSource) as f:
            beginning = [next(f) for x in range(num_lines2-data_tail)]
            beginning = [next(f) for x in range(data_tail)]
    reader = csv.reader(beginning,delimiter='&')
    for row in reader:
        y2.append(float(row[3][17:]) + yOS2)
        x2.append(float(row[4][18:]) - xOS2)
        headingI = float(row[16][24:])
    ##
    ##
    ## Read Lappy (tensorflow)
    centerX,centerY,boxWidth,boxHeight,bogieLat,bogieLong = [],[],[],[],[],[]
    dataSource = '/home/ros/Desktop/detectStream/detectLog.txt'
    with open(dataSource) as f:
        readerL = csv.reader(f)   
        for row in readerL:
            centerX.append(float(row[1]) )
            centerY.append(float(row[2]) )
            boxWidth.append(float(row[4]) )
            boxHeight.append(float(row[5][:7]) )
    with open(dataSource,'r+') as f:
        for xIt in range(data_tail):
            f.readline()
            i = i+1
        f.truncate(f.tell())
    #print(' centerX[19] : ' + str(  centerX[19]  ) + ' centerY[19]: ' + str(  centerY[19] )+ ' boxWidth[19] : ' + str(  boxWidth[19]  ) + ' boxHeight[19]: ' + str(  boxHeight[19]    ))
##
##
## Make boggie offsets
    itr = 19
    bogieHeading = headingI + centerX[itr] * cameraAngle -cameraAngle/2
    bogieDistance =  interp(boxWidth[itr],[.4,1],[300,2])/deg2feet #fix is not linear should be tan/arctan       
    bogieLat = x[itr] + bogieDistance * cos((bogieHeading/180)*math.pi)
    bogieLong = y[itr] + bogieDistance * sin((bogieHeading/180)*math.pi)
    line = str(bogieLat) + ',' + str(bogieLong)
    dataSource = '/home/ros/Desktop/bogieStream/bogieStream.txt'
    with open(dataSource,'a+') as f:
        content = f.read()
        for i in itertools.islice(content,data_tail):
            content = i + content
            
        f.seek(0,0)
        f.write(line.rstrip('\r\n') + '\n' + content)
        i=0
    with open(dataSource,'r+') as f:
        for xIt in range(data_tail):
            f.readline()
            i = i+1
        f.truncate(f.tell())
##
##
## Read Bogie Locations
    bogieLat,bogieLong = [],[]
    with open(dataSource) as f:
        readerB = csv.reader(f)
        for row in readerB:
            bogieLat.append(float(row[0]))
            bogieLong.append(float(row[1]))
        

        

    ax.clear()
    dx,dy = [x[data_tail-1],x2[data_tail-1]],[y[data_tail-1],y2[data_tail-1]]
    ax.plot(x2[:],y2[:],'bo',x[:],y[:],'g^',dx,dy,'k',bogieLat[:],bogieLong[:],'ro');
    

    #plt.plot(x2[:],y2[:],'ro',x[:],y[:],'g^',dx,dy,'k');
    plt.axes().set_aspect('equal')
    blue_patch = mpatches.Patch(color='blue',label='Operator')
    green_patch = mpatches.Patch(color='green',label='Drone')
    red_patch = mpatches.Patch(color='red',label='Person')
    plt.legend(handles=[blue_patch,green_patch,red_patch])
    #print(str(headingI))
    # add a wedge
    mPatches = []
    wedgeD = mpatches.Wedge([x[data_tail-1],y[data_tail-1]], vDist, cHeading - vAngle, cHeading + vAngle, ec="none")
    mPatches.append(wedgeD)
    wedgeI = mpatches.Wedge([x2[data_tail-1],y2[data_tail-1]], vDist, 90 - float(headingI) - vAngle, 90 - float(headingI)  + vAngle, ec="none")
    mPatches.append(wedgeI)
    collection = PatchCollection(mPatches,cmap=plt.cm.hsv,alpha=0.3)
    ax.add_collection(collection)
    #print(str(len(x)))
    #print('uBlox pts: ' + str(num_lines) + ' iOS pts: ' + str(num_lines2))
    distance = sqrt((x2[data_tail-1] -x[data_tail-1])**2+(y2[data_tail-1]-y[data_tail-1])**2)*deg2feet
    # print('distance: ' + str(round(distance,2)))

im_ani = animation.FuncAnimation(fig, animate,interval = 1000)

plt.show()
