#!/bin/sh
wmctrl -s "VNCDESKTOP Desktop"
cd /home/ros/Desktop/Q500Stream
python3 StartQ500Flask.py
pause