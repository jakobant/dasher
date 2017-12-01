#!/bin/bash

cd /home/pi/dasher
DIR=`ls screenshots`

for dd in $DIR
do
  echo $dd
  /home/pi/dasher/utils/timelaps.sh $dd
done
