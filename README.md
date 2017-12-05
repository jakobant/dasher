# Digital Signage DashScreenOS

DashScreenOS setup that in basic uses chrome browser for display all web content, chrome is
started with remote-debugging to allow local remote control.  Video files from youtube
are cached locally to minimize download.  The DashScreenOS has a timelaps function that can
capture screenshots form the displayed dashboard and create a timelaps videos.  DashOS
is also capable off capture timelaps images form USB Webcam or Raspberry Pi camera and
create timelaps videos

## Dasher
 Features

 1. Simple setup, will for Raspberry Pi, Ubuntu like and Fedora like OS.
 2. Chrome browser in kiosk mode with local remote control.
 3. Local API to allow remote control, i.e. send a video override for the screen.
 4. Local cache for youtube/facebook videos.
 5. Does not depend on remote server setup, but designed to look for it.
 6. Timed screenshots support for displayed screens.
 7. Capture images from webcam or Raspberry Pi Camera.
 8. Creates time laps videos from screenshots and webcam images.
 9. Simple UI for screenshots and timelaps view and control.
 
### Play list json tags descriptions:
There few basic type for a playlist acton tag, ```chrome, mxplayer, stream, raspitill and usbcam```, 
rest of the tags do have different meaning depending on the tags:
 - **type:** playlist type as described before.
 - **url:** url to display, media or stream.
 - **time:** how long the type is displayed, this is seconds.
 - **zoom:** browser zoom in or out, (0.9 = 90% zoom), only used with chrome type.
 - **screenshot:** true/false, screenshot can be used with all types, but only logical with chrome.
 - **delay:** the delay for the screenshot, chrome can take many seconds to fully load a page.
 - **prefix:** the folder name for the screenshots, when creating a timelaps video from screenshots
 it is good to have this uniq.
 - **startat:** used with mxplayer, when playing videos we can start playing in 00:01:00, the time to play 
 the video is controled by the time tag. This is only used in mxplayer and stream.
 - **device** this is the device number for usbcam screenshots. There can be multiple usbcam
 connected and used.

**Type descriptions**
 - **chrome** the chrome browser is remote controlled to display a url and zoom, tags used with
 this type are url, zoom, time, screenshot, delay and prefix.
 - **mxplayer** the default mxplayer is omxplayer for Raspberry Pi, the player type can be set
 with the environment MPLAYER to mplayer for Fedora, Ubuntu and MacOS. This type will cache the
 youtube and facebook videos locally. The url played here are browser urls ```https://www.youtube.com/watch?v=l2VCPDboU6k```
 this media type can be a video off a Power point show or some other magical message that you want
 to display, tags used with this type are url, startat, time (recommend to set screenshot to false).
 - **stream** the player is the same as mxplayer with this type, here the player is set to play direct 
 url stream for a video, tags used with this type are url, startat, time (recommend to set screenshot to false).
 - **raspistill** the raspistill will take a image shot from the Raspberry Pi camera and store with the 
 prefix tag. Tags used with this type are prefix and time.
 - **usbcam** a usbcam will take a image shot with fswebcam and store with the prefix tag. Tags used 
 with this type are prefix, time and device.

### Install to Rarspberry Pi
Install the demo dashboard, it will rotate the demo.json configuration.

Run:
```bash
wget https://raw.githubusercontent.com/jakobant/dasher/master/setup/install.sh
bash ./install.sh
```
To install the local dashboard to use local configuration, This setup does allow the
install that config only once to allow local updates, this enables the setup as a local
DashScreenOS, it initialy fetches the local.json as template.

Run:
```bash
bash ./install.sh local
```
That dashboard will install the local.json configuration.  This setup does allow the
install that config only once to allow local updates, this enables the setup as a local
DashScreenOS.

To install dashboard to look for remote config.  This example uses the domain: local.it, and 
id: itscreen1.  The DashScreenOs will look for DNS SRV record _dasher._tcp.local.it for the 
remote path config.  DNS SRV record : _dasher._tcp.local.it,screens.local.it,8080 . The 
DashScreenOS fetches ```http://screens.local.it:8080/artifacts/itscreen1.json``` for examples see
[Sceens artifacts](/artifacts)
```bash
wget https://raw.githubusercontent.com/jakobant/dasher/master/setup/install.sh
#bash ./install.sh <id> <domain>
bash ./install.sh itscreen1 local.it
```
### Development on Ubuntu or Fedora

[Local Development Ubuntu / Fedora / MacOS](/setup/Development.md)

### Demo content
```json
{"sites": [
  {"url": "https://storage.googleapis.com/cdn.thenewstack.io/media/2016/02/lithium-dashboard-1024x529.png", "time": 20, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "http://play.grafana.org/dashboard/db/big-dashboard?orgId=1", "time": 60, "type": "chrome", "zoom": 1, "screenshot": "true", "delay": "22", "device": "0", "prefix": "grafana", "startat": "00:00:00" },
  {"url": "https://www.youtube.com/watch?v=Gam5iWi4R_M", "time": 67, "type": "mxplayer", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "grafana", "startat": "00:00:00" },
  {"url": "", "time": 20, "type": "usbcam", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "usbcam", "startat": "00:00:00" }
]}
```
### Example timelaps videos created with DashScreenOS

<a href="http://www.youtube.com/watch?feature=player_embedded&v=ker6GrcVjL4" target="_blank"><img src="http://img.youtube.com/vi/ker6GrcVjL4/0.jpg"
alt="Kibana Netflow GEO Dashboard" width="480" height="360" border="1" /></a>

<a href="http://www.youtube.com/watch?feature=player_embedded&v=j4yiJGcR9Hw" target="_blank"><img src="http://img.youtube.com/vi/j4yiJGcR9Hw/0.jpg"
alt="Short Winter day in Iceland(timelaps)" width="480" height="360" border="1" /></a>

<a href="http://www.youtube.com/watch?feature=player_embedded&v=l2VCPDboU6k" target="_blank"><img src="http://img.youtube.com/vi/l2VCPDboU6k/0.jpg"
alt="DataDog timelaps dashboard" width="480" height="360" border="1" /></a>

