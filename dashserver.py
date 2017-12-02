#!/bin/python
import datetime
from time import sleep
from chromote import Chromote
import json
import re
import subprocess
import glob
import urllib2
import srvlookup
import os
import pafy

"""{"sites": [{"url": "https://storage.googleapis.com/cdn.thenewstack.io/media/2016/02/lithium-dashboard-1024x529.png", "time": 10, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "0", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "https://datadog-prod.imgix.net/img/blog/monitor-cloud-foundry/cloud-foundry-dashboard.png?fit=max", "time": 10, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "0", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "https://ga1.imgix.net/screenshot/o/91489-1454960580-6049945?ixlib=rb-1.0.0&ch=Width%2CDPR&auto=format", "time": 10, "type": "chrome", "zoom": 1, "screenshot": "false", "delay": "0", "device": "0", "prefix": "geo", "startat": "00:00:00" },
  {"url": "http://play.grafana.org/dashboard/db/big-dashboard?orgId=1", "time": 60, "type": "chrome", "zoom": 1, "screenshot": "true", "delay": "22", "device": "0", "prefix": "grafana", "startat": "00:00:00" },
  {"url": "https://www.youtube.com/watch?v=Gam5iWi4R_M", "time": 67, "type": "mxplayer", "zoom": 1, "screenshot": "false", "delay": "22", "device": "0", "prefix": "grafana", "startat": "00:00:00" } ]}
"""

class Dasher:
    def __init__(self, player, home):
        self.player = player
        self.home = home
        self.chrome = Chromote()
        self.tab = self.chrome.tabs[0]
        self.one_player = None
        self.thread = None
        self.myid = os.getenv('MYID', self.getMAC(self.getId()))
        self.play_url = "{}/artifacts/{}.json".format(self.get_srv_url(), self.myid)


    def override_play_url(self, url="https://elk.mikkari.net/artifacts/default.json"):
        self.play_url = url

    def getId(self):
        try:
            with open("/proc/net/route") as fh:
                for line in fh:
                    fields = line.strip().split()
                    if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                        continue
            return fields[0]
        except:
            # gguessin mac
            return "en0"

    def getMAC(self, interface='eth0'):
        try:
            line = open('/sys/class/net/%s/address' % interface).read()
        except:
            line = "000000000000"
        return line[0:17].replace(":", "").strip()

    def save_json(self, sites):
        try:
            f = open(self.home + "/.dash_cache", "w")
            f.write(json.dumps(sites, indent=4))
            f.close()
        except:
            None
        return sites


    def get_json(self):
        if self.myid=="local":
            try:
                print("Read local from cache")
                f = open(self.home + "/.dash_cache", "r")
                sites = json.loads(f.read())
                f.close()
            except:
                self.override_play_url("https://raw.githubusercontent.com/jakobant/dasher/master/artifacts/local.json")
                req = urllib2.Request(self.play_url)
                opener = urllib2.build_opener()
                fq = opener.open(req)
                sites = json.loads(fq.read())
                f = open(self.home + "/.dash_cache", "w")
                f.write(json.dumps(sites, indent=4))
                f.close()
            return sites

        try:
            req = urllib2.Request(self.play_url)
            opener = urllib2.build_opener()
            fq = opener.open(req)
            sites = json.loads(fq.read())
            f = open(self.home + "/.dash_cache", "w")
            f.write(json.dumps(sites, indent=4))
            f.close()
        except Exception as e:
            print(e)
            print("Read from cache")
            f = open(self.home + "/.dash_cache", "r")
            sites = json.loads(f.read())
            f.close()
        return sites

    def udisplay(self, site):
        if site['type'] == "mxplayer" or site['type'] == "stream":
            return self.mxplayer(site)
        if site['type'] == "raspistill" or site['type'] == "usbcam":
            self.webcam(site)
        else:
            self.chromedisplay(site)
        return int(site['time'])

    def chromedisplay(self, site):
        self.tab.set_url(site['url'])
        sleep(1)
        self.tab.set_zoom(site['zoom'])

    def webcam(self, site):
        today = datetime.datetime.now()
        dd_file = today.strftime('%Y-%m-%d-%H%M%S')
        base_path = "./screenshots/{}".format(site['prefix'])
        type = site['type']
        device = site['device']
        p = subprocess.Popen(["./utils/webcam_shot.sh", type, device, dd_file, base_path])
        p.communicate()[0]
        pic={'url': 'file://{}/{}/{}.png'.format(os.getcwd(), base_path, dd_file), 'zoom': 1}
        self.chromedisplay(pic)

    def mxplayer(self, site):
        if site['type'] == "stream":
            if self.player == "mplayer":
                subprocess.Popen(["mplayer", "-cache", "128", "-fs", site['url']])
            else:
                subprocess.Popen(["omxplayer", "-o", "hdmi", "-b", site['url']])
            time = int(site['time'])
        else:
            time, start = self.get_youtube_length(site)
            print(time)
            print(start)
            print(self.get_id(site['url']))
            file = self.get_download_file(self.get_id(site['url']))
            if file == "none":
                self.videodl(site)
                sleep(10)
            file = self.get_download_file(self.get_id(site['url']))
            print(file)
            if self.player == "mplayer":
                subprocess.Popen(["mplayer", "-fs", file, "-ss", start])
            else:
                subprocess.Popen(["omxplayer", "-o", "hdmi", "-b", file, "-l", start])
        return time

    def kill_mxplayer(self):
        try:
            if self.player == "mplayer":
                subprocess.Popen(["killall", "-9", "mplayer"])
            else:
                subprocess.Popen(["killall", "-9", "omxplayer.bin"])
            self.thread.cancel()
        except:
            None

    def get_download_file(self, id_file):
        file = glob.glob(self.home + "/Downloads/%s.mp4" % id_file)
        if len(file) > 0:
            return file[0]
        file = glob.glob(self.home + "/Downloads/%s*part*" % id_file)
        if len(file) > 0:
            return file[0]
        return "none"

    def get_id(self, url):
        if re.search("youtube|youtu.be", url):
            #youtube.com/watch?v=asdfasdf
            ma = re.compile(".*=(.*)$")
            match = ma.match(url)
            if match:
                return match.groups()[0]
            #youtu.be/adsfdsff
            ma = re.compile(".*/(.*)$")
            match = ma.match(url)
            if match:
                return match.groups()[0]
        elif re.search("facebook", url):
            ma = re.compile(".*/(.*)$")
            match = ma.match(url)
            if match:
                return match.groups()[0]

    def videodl(self, site):
        if re.search("youtube", site['url']) or re.search("youtu.be", site['url']):
            self.download_youtube(site['url'])
        elif re.search("facebook", site['url']):
            self.download_facebook(site['url'])

    def download_facebook(self, url):
        print("download facebook")
        subprocess.Popen(["youtube-dl", "-o", self.home + "/Downloads/%(id)s.%(ext)s", url])

    def get_screenshot(self, delay, prefix):
        print("Get screenshot delay:{} prefix:{}").format(delay, prefix)
        p = subprocess.Popen(["./utils/screenshot.sh", delay, prefix])
        print(p.communicate())

    def download_youtube(self, url):
        print("download youtube")
        subprocess.Popen(["youtube-dl", "-f", "22,18", "-o", self.home + "/Downloads/%(id)s.%(ext)s", url])

    def get_youtube_length(self, site):
        url = site['url']
        video = pafy.new(url)
        try:
            time = int(site['time'])
        except:
            time = video.length
        if time == 0:
            time = video.length
        try:
            start_at = self.get_sec(site['startat'])
            start_at_str = site['startat']
        except:
            start_at = 0
            start_at_str = "00:00:00"
        if start_at > 0:
            return time, start_at_str
        else:
            return time, start_at_str

    def get_sec(self, time_str):
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    def get_srv_url(self):
        if self.myid=="demo":
            return "https://raw.githubusercontent.com/jakobant/dasher/master/artifacts"
        try:
            domain = os.getenv('DOMAIN')
            if domain:
                srv = srvlookup.lookup('dasher', domain=domain)[0]
            else:
                srv = srvlookup.lookup('dasher')[0]
            if srv.port == 443:
                url = "https://{}/artifacts".format(srv.host)
            else:
                url = "http://{}:{}/artifacts".format(srv.host, srv.port)
            return url
        except:
            return "https://dasher.mikkari.net/artifacts"

