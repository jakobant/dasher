#!/bin/bash
set -x

cd /home/pi/dasher

if [ "$#" -le 0 ]; then
    echo "Illegal number of parameters"
    echo "Usage $0 path <date, ie 2017-11-26>"
    exit 1
fi

BASEPATH=$1
FULLPATH="./screenshots/$1"
FRAMES=${FRAMES:-5}
if [ ! -d "$FULLPATH" ]; then
    echo "Directory $FULLPATH does not exist!!"
    exit 1
fi
if [ "$#" -eq 2 ]; then
    DD=$2
else
    DD=`date +%Y-%m-%d --date="1 days ago"`
fi

find $FULLPATH -type f -size -100k -name '$DD*.png' -exec rm {} \;

cd $FULLPATH
tar cvf ${DD}_backup.tar $DD*.png
ls $DD*.png| awk 'BEGIN{ a=0 }{ printf "cp %s timelaps%04d.png\n", $0, a++ }'| bash
COUNT=`ls timelaps*png|wc -w`
if [ $COUNT -gt 700 ]; then
    FRAMES=10
fi

if [ -f /etc/fedora-release ]; then
	ffmpeg -y -r $FRAMES -start_number 0 -i 'timelaps%04d.png' -c:v libx264 -pix_fmp yuv420p -preset slow -crf 15 ${DD}_${BASEPATH}_timelaps_final.mp4
elif [ -f /etc/lsb-release  ]; then
	ffmpeg -y -r $FRAMES -start_number 0 -i 'timelaps%04d.png' -c:v libx264 -pix_fmt yuv420p -preset slow -crf 15 ${DD}_${BASEPATH}_timelaps_final.mp4
else
	avconv -y -r $FRAMES -i timelaps%04d.png -r $FRAMES -vcodec libx264 -pix_fmt yuv420p -q:v 20 -vf scale=1280:720 ${DD}_${BASEPATH}_timelaps_final.mp4
fi

rm -f timelaps*png
