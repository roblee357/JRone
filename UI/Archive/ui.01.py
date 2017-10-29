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
import matplotlib.animation as animation
import numpy as np
from math import sqrt

fig = plt.figure()
ax = fig.add_subplot(111)
x,y,x2,y2 = [],[],[],[]
data_tail =20
heading = 30
cHeading = 90 - heading
vAngle = 20

    
def animate(i):
    ##
    ## Read uBlox
    x,y = [],[]
    xOS,yOS = 0.0093513,0.3762786
    dataSource = '/home/ros/Desktop/uBlox Stream/GPS_Delta_log.txt'
    with open(dataSource) as f:
        num_lines = sum(1 for line in f)
    if num_lines > 21:
        with open(dataSource) as f:
            beginning = [next(f) for x in range(num_lines-data_tail)]
            beginning = [next(f) for x in range(data_tail)]
            reader = csv.reader(beginning)
    else:
        with open(dataSource) as f:
            reader = csv.reader(f)        
    for row in reader:
        y.append(float(row[0])/100 + yOS)
        x.append(float(row[1])/-100 - xOS)
    ##
    ## Read iPhone
    x2,y2 = [],[]
    xOS2,yOS2 = 0.0,0.0
    dataSource = '/home/ros/Desktop/iPhone Stream/out/iPhone_Sensor_log.txt'
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
        headingI = row[16][24:]
    ax.clear()
    dx,dy = [x[data_tail-1],x2[data_tail-1]],[y[data_tail-1],y2[data_tail-1]]
    ax.plot(x2[:],y2[:],'ro',x[:],y[:],'g^',dx,dy,'k');
    

    #plt.plot(x2[:],y2[:],'ro',x[:],y[:],'g^',dx,dy,'k');
    plt.axes().set_aspect('equal')
    #print(str(headingI))
    # add a wedge
    mPatches = []
    wedgeD = mpatches.Wedge([x[data_tail-1],y[data_tail-1]], 0.00001, cHeading - vAngle, cHeading + vAngle, ec="none")
    mPatches.append(wedgeD)
    wedgeI = mpatches.Wedge([x2[data_tail-1],y2[data_tail-1]], 0.00001, 90 - float(headingI) - vAngle, 90 - float(headingI)  + vAngle, ec="none")
    mPatches.append(wedgeI)
    collection = PatchCollection(mPatches,cmap=plt.cm.hsv,alpha=0.3)
    ax.add_collection(collection)
    #print(str(len(x)))
    #print('uBlox pts: ' + str(num_lines) + ' iOS pts: ' + str(num_lines2))
    distance = sqrt((x2[data_tail-1] -x[data_tail-1])**2+(y2[data_tail-1]-y[data_tail-1])**2)*363972
    print('distance: ' + str(round(distance,2)))

im_ani = animation.FuncAnimation(fig, animate,interval = 1000)

plt.show()
