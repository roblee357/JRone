#!/bin/sh
#mate-terminal --working-directory="/home/ros/Desktop/uBloxStream" --command "./startGPS_log.sh"
mate-terminal --working-directory="/home/ros/Desktop/detectStream" --command "./StartDetectFlask.sh"
mate-terminal --working-directory="/home/ros/Desktop/Q500Stream" --command "./StartQ500Flask.sh"
mate-terminal --working-directory="/home/ros/Desktop/ST10+Stream" --command "./StartST10+Flask.sh"
mate-terminal --working-directory="/home/ros/Desktop/iPhoneStream" --command "./startiPhoneFlask.sh"
mate-terminal --working-directory="/home/ros/Desktop/UI" --command "./startUI.sh"
