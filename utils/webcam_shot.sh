#!/bin/bash

type=$1
device=$2
bfile=$3
base_path=$4

mkdir -p $base_path
if [ "$type" == "raspistill" ]; then
  raspistill -h 2592 -w 1944 -e png -o $base_path/$bfile.png
fi

if [ "$type" == "usbcam" ]; then
  fswebcam -S 40 -d /dev/video$device -r 2592x1944 --png 9 --save $base_path/$bfile.png
fi
