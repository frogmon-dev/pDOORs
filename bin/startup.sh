#!/bin/bash

sudo python3 /home/pi/DOORs/src/doorDetector.py &
sleep 1
sudo python3 /home/pi/DOORs/src/doorImager.py &
sleep 1
sudo python3 /home/pi/DOORs/src/face_copy.py &

exit
