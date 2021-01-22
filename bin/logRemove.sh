#!/bin/bash
find ./logs/*.log -ctime +30 -exec sudo rm -f {} \;
find ./facelog/*.png -ctime +7 -exec sudo rm -f {} \;
