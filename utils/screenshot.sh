#!/bin/bash
set -x
WAIT=${1:-20}
sleep $WAIT
export PRE=${2:-temp}
mkdir -p $HOME/screenshots/$PRE
export DISPLAY=:0
/usr/bin/scrot -e '/usr/bin/mogrify -font Liberation-Sans -fill yellow -undercolor "#00000080" -pointsize 26 -annotate +30+30 "`date`" $f ; mv $f `echo \$HOME`/screenshots/`echo \$PRE`'
