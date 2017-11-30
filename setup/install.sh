#!/bin/bash

git clone https://github.com/jakobant/dasher.git
git clone https://github.com/jakobant/piwify.git

sudo apt-get install imagemagick ffmpeg libav-tools -y
sudo pip install virtualenv

cd dasher
virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
cd ..

cd pywify
virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt

cat <<EOF>/home/pi/.config/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@point-rpi
@xset s noblank
@xset s off
@xset -dpms
@chromium-browser --kiosk --disable-session-crashed-bubble --remote-debugging-port=9222
@/home/pi/dasher/start.sh
EOF

cat <<EOF>/home/pi/dasher/start.sh
#!/bin/bash
cd /home/pi/dasher
source /home/pi/dasher/venv/bin/activate
while true
do
MYID="kobbi" /home/pi/dasher/venv/bin/python /home/pi/dasher/server.py
sleep 30
done
EOF

