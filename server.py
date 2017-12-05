#!flask/bin/python
from flask import Flask, jsonify, Response
from flask_httpauth import HTTPBasicAuth
from flask import render_template
from flask import make_response
from flask import request
from dashserver import Dasher
import threading, os, glob

auth = HTTPBasicAuth()
api_key = os.getenv('D_API_KEY', 'admin')
dasher_home = os.getenv('HOME', '/home/pi')
dasher_player = os.getenv('MPLAYER', 'mxplayer')

dasher = Dasher(dasher_player, dasher_home)


class Loop:
    def __init__(self, dasher):
        self.dasher = dasher
        self.sites = self.dasher.get_json()
        self.sites['myid'] = self.dasher.myid
        self.ssize = len(self.sites['sites'])
        self.current = 0
        self.thread = None
        self.is_mxplayer = False

    def get_next(self):
        x = self.current
        if self.ssize == 0:
            self.sites = self.dasher.get_json()
        site = self.sites['sites'][x]
        if self.current == self.ssize - 1 or self.ssize == 0:
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
        self.sites = {"sites": []}
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
        if site['screenshot'] == 'true':
            self.dasher.get_screenshot(site['delay'], site['prefix'] )
        return site


looper = Loop(dasher)
looper.start()

app = Flask(__name__)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_folders(path):
    folders = []
    for list in glob.glob(path):
        folders.append(os.path.basename(list))
    return folders

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.get_password
def get_password(username):
    if username == api_key:
        return 'pi'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
@auth.login_required
def index():
    folders = {'list': get_folders('./screenshots/*')}
    return render_template("index.html",
                           title='Home', screenshots=folders, timelaps=folders)


@app.route('/playlist_view')
def playlist_view():
    return render_template("playlist_view.html",
                           title='Play View')


@app.route('/clear_playlist')
@auth.login_required
def clear():
    looper.clean_sites()
    return make_response(jsonify({'result': 'clearing sites'}), 200)


@app.route('/stop')
@auth.login_required
def stop():
    looper.stop()
    return make_response(jsonify({'result': 'stopping thread'}), 200)


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
    return make_response(jsonify(sites), 200)


@app.route('/add_to_playlist', methods=['POST', 'GET'])
@auth.login_required
def add_playlist():
    if request.method == 'GET' and request.args.get('url') != None:
        url = request.args.get('url')
        time = request.args.get('time')
        startat = request.args.get('startat')
        type = request.args.get('type')
        zoom = request.args.get('zoom')
        screenshot = request.args.get('screenshot')
        delay = request.args.get('delay')
        prefix = request.args.get('prefix')
        device = request.args.get('device')
        json = {'url': url, 'time': time, 'startat': startat, 'type': type, 'zoom': zoom, 'screenshot': screenshot, 'delay': delay, 'prefix': prefix, 'device': device}
        print (json['url'])
        looper.add_to_playlist(json)
        dasher.save_json(looper.sites)
        return make_response(jsonify({'result': 'Success'}), 200)
    else:
        return make_response(jsonify({'result': 'Error missing data'}), 200)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({'result': 'Error set Content-Type: application/json'}), 403)
    data = request.json
    print (data['url'])
    looper.add_to_playlist(data)
    return make_response(jsonify({'result': 'Success'}), 200)


@app.route('/show', methods=['POST'])
@auth.login_required
def set_show():
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({'error': 'set Content-Type: application/json'}), 403)
    data = request.json
    print (data['url'])
    looper.start(data)
    return make_response(jsonify({'response': 'Success'}), 200)


@app.route('/screenshots', methods=['GET'])
@auth.login_required
def get_screenshots():
    if request.method == 'GET' and request.args.get('path') != None:
        path = request.args.get('path')
        files = glob.glob('./screenshots/'+path+'/*png')
        files.sort(key=os.path.getmtime)
        print({'results': files})
        return render_template("screenshots.html",
                               title='Screenshots', list={'results': files} )

@app.route('/timelaps')
@auth.login_required
def get_timelaps():
    if request.method == 'GET' and request.args.get('path') != None:
        path = request.args.get('path')
        files = glob.glob('./screenshots/'+path+'/*mp4')
        files.sort(key=os.path.getmtime)
        print({'results': files})
        return render_template("screenshots.html",
                               title='Timelaps', list={'results': files} )



@app.route('/media/<path:path>')
@auth.login_required
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".png": "image/png",
        ".mp4": "video/mp4"    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
