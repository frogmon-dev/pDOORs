#!/bin/bash

python3 /home/pi/DOORs/src/doorDetector.py &
sleep 1
python3 /home/pi/DOORs/src/doorImager.py &
sleep 7
python3 /home/pi/DOORs/src/doorMqtt.py &

exit
