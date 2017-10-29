#!/bin/sh
wmctrl -s "VNCDESKTOP Desktop"
cd /home/ros/Desktop/detectStream
python3 StartDetectFlask.py

