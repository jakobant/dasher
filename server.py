#!flask/bin/python
from flask import Flask, jsonify 
from flask.ext.httpauth import HTTPBasicAuth
from flask import render_template
from flask import make_response
from flask import request
import os
from dashserver import Dasher
from time import sleep
import json
import threading

auth = HTTPBasicAuth()
api_key=os.getenv('D_API_KEY', 'admin')

dasher = Dasher("mplayer", "/Users/jakobant")

class Loop:
    def __init__(self, dasher):
        self.dasher = dasher
        self.sites = self.dasher.get_json()
        self.ssize = len(self.sites['sites'])
        self.current = 0
        self.thread = None
        self.is_mxplayer = False

    def get_next(self):
        x = self.current
        site = self.sites['sites'][x]
        if self.current == self.ssize-1:
            self.sites = self.dasher.get_json()
            self.ssize = len(self.sites['sites'])
            self.current = 0
            self.sites = self.dasher.get_json()
            self.ssize = len(self.sites['sites'])
        else:
            self.current = self.current + 1
        return site

    def switch(self):
        self.start()

    def clean_sites(self):
        self.sites = { "sites": [] }
        self.current = 0
        self.ssize = 0

    def add_to_playlist(self, site):
        self.sites['sites'].append(site)
        self.ssize = self.ssize + 1

    def stop(self):
        try:
            self.thread.cancel()
        except:
            None
        if self.is_mxplayer:
            self.dasher.kill_mxplayer()

    def start(self, site=None):
        if self.thread:
            self.thread.cancel()
        if self.is_mxplayer:
            self.dasher.kill_mxplayer()
        if not site:
            site = self.get_next()
        if site['type'] in ['mxplayer', 'stream']:
            self.is_mxplayer = True
        else:
            self.is_mxplayer = False
        print(site)
        time = self.dasher.udisplay(site)
        self.thread = threading.Timer(time, self.start)
        self.thread.start()
        return site

looper = Loop(dasher)
#looper.start()

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'pi'
    elif username == api_key:
        return 'pi'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/')
def index():
    return render_template("index.html",
                           title='Home')

@app.route('/playlist_view')
def playlist_view():
    return render_template("playlist_view.html",
                           title='Play View')


@app.route('/clear_playlist')
@auth.login_required
def clear():
    looper.clean_sites()
    return make_response(jsonify({'success': 'cleanig sites'}), 200)

@app.route('/stop')
@auth.login_required
def stop():
    looper.stop()
    return make_response(jsonify({'success': 'stopping thread'}), 200)

@app.route('/switch')
@auth.login_required
def get_index():
    site = looper.start()
    print (site)
    return make_response(jsonify(site), 200)

@app.route('/playlist')
@auth.login_required
def get_sites():
    sites = looper.sites
    if request.args.get('json'):
        return make_response(jsonify(sites), 200)
    else:
        return render_template("playlist.html",
                           title='Home',
                           sites=sites)

@app.route('/add_to_playlist',  methods = ['POST', 'GET'])
@auth.login_required
def add_playlist():
    if request.method == 'GET':
        url = request.args.get('url')
        time = request.args.get('time')
        startat = request.args.get('startat')
        type = request.args.get('type')
        zoom = request.args.get('zoom')
        json = { 'url': url, 'time': time, 'startat': startat, 'type': type, 'zoom': zoom }
        print (json['url'])
        looper.add_to_playlist(json)
        return make_response(jsonify({'response': 'Success'}), 200)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({'error': 'set Content-Type: application/json'}), 403)
    data = request.json
    print (data['url'])
    looper.add_to_playlist(data)
    return make_response(jsonify({'response': 'Success'}), 200)


@app.route('/show',  methods = ['POST'])
@auth.login_required
def set_show():
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({'error': 'set Content-Type: application/json'}), 403)
    data = request.json
    print (data['url'])
    looper.start(data)
    return make_response(jsonify({'response': 'Success'}), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
