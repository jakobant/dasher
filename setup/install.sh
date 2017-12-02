#!/bin/bash

MYID=${1:-demo}
DOMAIN=${2:-no}
git clone https://github.com/jakobant/dasher.git
git clone https://github.com/jakobant/piwify.git

sudo apt-get install imagemagick ffmpeg libav-tools fswebcam -y
sudo pip install virtualenv

cd dasher
virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
cd ..

cd piwify
virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt

if [ "$DOMAIN" == "no" ]; then
    STARTD="MYID=\"$MYID\""
else
    STARTD="DOMAIN=\"$DOMAIN\" MYID=\"$MYID\""
fi
cat <<EOF>/home/pi/.config/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@point-rpi
@xset s noblank
@xset s off
@xset -dpms
@/home/pi/dasher/chrome.sh
@/home/pi/dasher/start.sh
EOF

cat <<EOF>/home/pi/dasher/start.sh
#!/bin/bash
cd /home/pi/dasher
source /home/pi/dasher/venv/bin/activate
while true
do
$STARTD /home/pi/dasher/venv/bin/python /home/pi/dasher/server.py
sleep 30
done
EOF

cat <<EOF>/home/pi/dasher/chrome.sh
#!/bin/bash
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/'Local State'
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences
chromium-browser --kiosk --remote-debugging-port=9222 --no-default-browser-check --no-first-run --disable-infobars --disable-session-crashed-bubble
EOF

cat <<EOF>/tmp/c
0 1 * * * /home/pi/dasher/utils/cron.sh
EOF
crontab /tmp/c

chmod 755 /home/pi/dasher/*.sh

