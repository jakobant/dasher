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

### Demo content
```json
{"sites": [
  {"url": "https://storage.googleapis.com/cdn.thenewstack.io/media/2016/02/lithium-dashboard-1024x529.png", "time": 20, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "https://datadog-prod.imgix.net/img/blog/monitor-cloud-foundry/cloud-foundry-dashboard.png?fit=max", "time": 20, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "https://ga1.imgix.net/screenshot/o/91489-1454960580-6049945?ixlib=rb-1.0.0&ch=Width%2CDPR&auto=format", "time": 20, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "http://play.grafana.org/dashboard/db/big-dashboard?orgId=1", "time": 60, "type": "chrome", "zoom": 1, "screenshot": "true", "delay": "22", "device": "0", "prefix": "grafana", "startat": "00:00:00" },
  {"url": "https://www.youtube.com/watch?v=Gam5iWi4R_M", "time": 67, "type": "mxplayer", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "grafana", "startat": "00:00:00" },
  {"url": "", "time": 20, "type": "usbcam", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "usbcam", "startat": "00:00:00" }
]}
```
### Example timelaps videos created with DashScreenOS

<a href="http://www.youtube.com/watch?feature=player_embedded&v=ker6GrcVjL4" target="_blank"><img src="http://img.youtube.com/vi/ker6GrcVjL4/0.jpg"
alt="Kibana Netflow GEO Dashboard" width="480" height="360" border="1" /></a>
ker6GrcVjL4

### Other fun demo
<a href="http://www.youtube.com/watch?feature=player_embedded&v=Gam5iWi4R_M" target="_blank"><img src="http://img.youtube.com/vi/Gam5iWi4R_M/0.jpg"
alt="Grafana development .." width="480" height="360" border="1" /></a>
