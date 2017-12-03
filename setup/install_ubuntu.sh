#!/bin/bash

git clone https://github.com/jakobant/dasher.git
git clone https://github.com/jakobant/piwify.git

TOOLS="imagemagick ffmpeg virtualenv fswebcam"
for tool in $TOOLS
do
    sudo apt-get install $tool -y
done

cd dasher
virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
cd ..

cd piwify
virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt

echo "Start chrome with --remote-debugging-port=9222"
