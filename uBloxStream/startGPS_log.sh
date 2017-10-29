#!/bin/sh
wmctrl -s "VNCDESKTOP Desktop"
cd /home/ros/Desktop/uBloxStream
python3 write_GPS_Motion.py

