#!/bin/bash

WAIT=${1:-20}
sleep $WAIT
export PRE=${2:-temp}
mkdir -p $HOME/screenshots/$PRE
export DISPLAY=:0
export DD=`date +%Y-%m-%d-%H%M%S`
if [ -f /etc/fedora-release ]
then
	gnome-screenshot -f ${DD}.png
	mogrify -font Liberation-Sans -fill yellow -undercolor "#00000080" -pointsize 26 -annotate +30+30 "`date`" ${DD}.png
	mv ${DD}_fedora.png $HOME/screenshots/$PRE
elif [ -f /etc/redat-release ]
then
	gnome-screenshot -f ${DD}.png
	mogrify -font Liberation-Sans -fill yellow -undercolor "#00000080" -pointsize 26 -annotate +30+30 "`date`" ${DD}.png
	mv ${DD}_redhat.png $HOME/screenshots/$PRE
else
	scrot ${DD}.png
	mogrify -font Liberation-Sans -fill yellow -undercolor "#00000080" -pointsize 26 -annotate +30+30 "`date`" ${DD}.png
	mv ${DD}_fedora.png $HOME/screenshots/$PRE
fi

