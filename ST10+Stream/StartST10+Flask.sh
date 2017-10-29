#!/bin/sh
wmctrl -s "VNCDESKTOP Desktop"
cd /home/ros/Desktop/ST10+Stream
python3 StartST10+Flask.py
