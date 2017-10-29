import mplleaflet
import csv
from matplotlib import pyplot as plt
x,y = [],[]
with open('/home/ros/Documents/archive/GPS_Delta_log (copy).txt') as f:
    reader = csv.reader(f)
    for row in reader:
        x.append(row[0])
        y.append(row[1])
fig = plt.figure()
plt.plot(x[:],y[:])
plt.plot(x[:],y[:],'ro');
plt.show()

mplleaflet.display(fig=fig)