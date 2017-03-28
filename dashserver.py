#!/bin/python

from time import sleep
from chromote import Chromote
import json
import threading
import re
import subprocess
import glob
import urllib2
import time
"""
sitess = { "sites": [
{ "url": "http://www.mbl.is", "time": 12, "type": "chrome", "zoom": 1.3 },
{ "url": "https://www.youtube.com/watch?v=qRfnQn0g5-Q", "time": 20, "type": "mxplayer", "zoom": 1, "startat": "00:06:00" },
{ "url": "http://www.cnn.com", "time": 20, "type": "chrome", "zoom": 1.5 }
] }"""
class Dasher:
    def __init__(self, player, home, play_url="https://elk.mikkari.net/roll/default.json"):
        self.player=player
        self.home=home
        self.chrome = Chromote()
        self.tab = self.chrome.tabs[0]
        self.play_url=play_url
        self.one_player = None
        self.stop_now = False

    def wait_for_it(self, timer):
        while not self.stop_now and timer >0:
            timer = timer - 1
            time.sleep(1)
        self.kill_mxplayer()

    def get_json(self):
        try:
            req = urllib2.Request(self.play_url)
            opener = urllib2.build_opener()
            fq = opener.open(req)
            sites = json.loads(fq.read())
            f = open(self.home+"/.dash_cache", "w")
            f.write(json.dumps(sites))
            f.close()
        except Exception as e:
            print(e)
            print("Read from cache")
            f =open(self.home+"/.dash_cache", "r")
            sites=json.loads(f.read())
            f.close()
        return sites

    def udisplay(self, site):
        if site['type'] == "mxplayer" or site['type'] == "stream":
            self.mxplayer(site)
        else:
            self.chromedisplay(site)

    def chromedisplay(self, site):
        self.tab.set_url(site['url'])
        sleep(1)
        self.tab.set_zoom(site['zoom'])

    def mxplayer(self, site):
        try:
            start=site['startat']
        except:
            start="0"
        if site['type'] == "stream":
            if self.player == "mplayer":
                subprocess.Popen(["/usr/local/bin/mplayer", "-fs", site['url']])
            else:
                subprocess.Popen(["omxplayer", "-o", "hdmi", "-b", site['url']])
        else:
            print(self.get_id(site['url']))
            file = self.get_download_file(self.get_id(site['url']))
            if file=="none":
                self.videodl(site)
                sleep(10)
            file = self.get_download_file(self.get_id(site['url']))
            print(file)
            if self.player=="mplayer":
                subprocess.Popen(["/usr/local/bin/mplayer", "-fs", file, "-ss", start])
            else:
                subprocess.Popen(["omxplayer", "-o", "hdmi", "-b", file, "-l", start])
        t = threading.Thread(target=self.wait_for_it, args=[int(site['time'])])
        t.start()


    def kill_mxplayer(self):
        try:
            if self.player == "mplayer":
                subprocess.Popen(["killall", "-9", "mplayer"])
            else:
                subprocess.Popen(["killall", "-9", "omxplayer.bin"])
        except:
            None

    def get_download_file(self, id_file):
        file = glob.glob(self.home+"/Downloads/%s.mp4" % id_file)
        #print (file)
        #print (self.home+"/Downloads/%s.mp4" % id_file)
        if len(file) > 0:
            return file[0]
        file = glob.glob(self.home + "/Downloads/%s*part*" % id_file)
        if len(file) > 0:
            return file[0]
        return "none"

    def get_id(self, url):
        if re.search("youtube", url):
            ma = re.compile(".*=(.*)$")
            match = ma.match(url)
            if match:
                return match.groups()[0]
        elif re.search("facebook", url):
            ma = re.compile(".*/(.*)$")
            match = ma.match(url)
            if match:
                return match.groups()[0]

    def videodl(self, site):
        if re.search("youtube", site['url']):
            self.download_youtube(site['url'])
        elif re.search("facebook", site['url']):
            self.download_facebook(site['url'])

    def download_facebook(self, url):
        print("download facebook")
        subprocess.Popen(["youtube-dl", "-o", self.home + "/Downloads/%(id)s.%(ext)s", url])


    def download_youtube(self, url):
        print("download youtube")
        subprocess.Popen(["youtube-dl", "-f", "22,18", "-o", self.home + "/Downloads/%(id)s.%(ext)s", url])

#while True:
#    pl = Dasher("mplayer", "/Users/jakobant")
#    sites = pl.get_json()
#    for site in sites['sites']:
#        pl.udisplay(site)
#        sleep(10)
        #sleep(int(site['time']))
