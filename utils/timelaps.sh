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

ffmpeg -y -r 5 -pattern_type glob -i '*.png' -i timelaps%04d.png -c:v copy ${DD}_${BASEPATH}_timelaps.avi

rm -f timelaps*png

if [ -f /etc/fedora-release ]; then
	ffmpeg -y -i ${DD}_${BASEPATH}_timelaps.avi -c:v libx264 -preset slow -crf 15 ${DD}_${BASEPATH}_timelaps_final.mp4
elif [ -f /etc/redat-release ]; then
	ffmpeg -y -i ${DD}_${BASEPATH}_timelaps.avi -c:v libx264 -preset slow -crf 15 ${DD}_${BASEPATH}_timelaps_final.mp4
else
	avconv -y -r 10 -i ${DD}_${BASEPATH}_timelaps.avi -r 10 -vcodec libx264 -pix_fmt yuv420p -q:v 20 -vf scale=1280:720 ${DD}_${BASEPATH}_timelaps_final.mp4
fi
rm -f ${DD}_${BASEPATH}_timelaps.avi
