#!flask/bin/python
from flask import Flask, jsonify 
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import request
import time
from dashserver import Dasher
from time import sleep
import json
import threading

auth = HTTPBasicAuth()
dasher = Dasher("mplayer", "/Users/jakobant")

class Loop:
    def __init__(self, dasher):
        self.dasher = dasher
        self.sites = self.dasher.get_json()
        self.ssize = len(self.sites['sites'])
        self.current = 0
        self.one_thread = None
        self.stop_now = False

    def wait_for_it(self, timer):
        while not self.stop_now and timer > 0:
            timer = timer - 1
            time.sleep(1)
        if not self.stop_now:
            self.start(self.get_next())

    def get_next(self):
        x = self.current
        site = self.sites['sites'][x]
        if self.current == self.ssize-1:
            self.sites = self.dasher.get_json()
            self.ssize = len(self.sites['sites'])
            self.current = 0
        else:
            self.current = self.current + 1
        return site

    def switch(self, site):
        self.dasher.kill_mxplayer()
        self.dasher.udisplay(site)
        time.sleep(1)
        self.wait_for_it(int(site['time']))

    def start(self, site):
        print(site)
        self.stop_now=False
        self.dasher.udisplay(site)
        t = threading.Thread(target=self.wait_for_it, args=[int(site['time'])])
        t.start()

    def stop(self,):
        self.stop_now = True

ll = Loop(dasher)
ll.switch(ll.get_next())

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'pi'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/stop')
@auth.login_required
def stop():
    ll.stop()
    return make_response(jsonify({'success': 'stopping thread'}), 200)


@app.route('/switch')
@auth.login_required
def get_index():
    site =ll.get_next()
    print (site)
    ll.switch(site)
    return make_response(jsonify(site), 200)

@app.route('/sites')
@auth.login_required
def get_sites():
    sites =ll.sites
    return make_response(jsonify(sites), 200)

@app.route('/show',  methods = ['POST'])
@auth.login_required
def set_show():
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({'error': 'set Content-Type: application/json'}), 403)
    data = request.json
    print (data['url'])
    ll.switch(data )
    return make_response(jsonify({'response': 'Success'}), 200)


if __name__ == '__main__':
    app.run(debug=True)
