#!/bin/bash

echo $#

if [ "$#" -le 0 ]; then
    echo "Illegal number of parameters"
    echo "Usage $0 path <date, ie 2017-11-26>"
    exit 1
fi

BASEPATH=$1
FULLPATH="./screenshots/$1"

if [ ! -d "$FULLPATH" ]; then
    echo "Directory $FULLPATH does not exist!!"
    exit 1
fi
if [ "$#" -eq 2 ]; then
    DD=$2
else
    DD=`date +%Y-%m-%d --date="1 days ago"`
fi

find $FULLPATH -type f -size -270k -name '$DD*.png' -exec rm {} \;

cd $FULLPATH
ls $DD*.png| awk 'BEGIN{ a=0 }{ printf "cp %s timelaps%04d.png\n", $0, a++ }'| bash


#avconv -y -r 5 -i timelaps%04d.png -r 5 -vcodec libx264 -q:v 20 -vf scale=1280:720 elk_timelaps_2811.mp4

ffmpeg -r 5 -pattern_type glob -i '*.png' -i timelaps%04d.png -s hd1080 -vcodec libx264 ${DD}_${BASEPATH}_timelaps.mp4

rm -f timelaps*png