## Local Development 

``` 
 git clone https://github.com/jakobant/dasher.git
 cd dasher
 virtualenv venv
 source ./venv/bin/activate
 ./venv/bin/pip install -r requirements.txt
 ```
Start chrome with --remote-debugging-port=9222 parameter. 
Set environment for MPLAYER and MYID, MPLAYER=mplayer and MYID=local and start:
```source ./venv/bin/activate && ./venv/bin/python server.py```

Open browser to http://localhost:5000 for the Simple Web Admin.  The default user is pi, and 
default password is **admin**, please change that by setting the environment D_API_KEY.

### Ubuntu development
Install packages needed: ```sudo apt-get install imagemagick ffmpeg virtualenv fswebcam```

Install script

Run:
```bash
wget https://raw.githubusercontent.com/jakobant/dasher/master/setup/install_ubuntu.sh
bash ./install_ubuntu.sh
```

### Fedora development

Install script for Fedora

Run:
```bash
wget https://raw.githubusercontent.com/jakobant/dasher/master/setup/install_fedora.sh
bash ./install_fedora.sh
```

### MacOS development

Install script for MacOS

Run:

```bash
wget https://raw.githubusercontent.com/jakobant/dasher/master/setup/install_osx.sh
bash ./install_osx.sh
```

