 # Ace Stream Engine
Ace Stream Engine for Raspberry Pi 4 (ARMv7).

Official web site http://www.acestream.org/

It is running as service in chroot environment on Raspberry Pi OS.

WebUI is available at:
```
http://<IP>:6878/webui/app/<-access-token->/server
```
Access token is generated during install and printed on the screen.

## Installation
```
sudo ./install.sh
```

Send HTTP query to http://127.0.0.1:6878/webui/api/service?method=get_version&format=jsonp&callback=mycallback If app engine is running, then it return version.

## Uninstallation
```
sudo systemctl stop acestream
sudo rm /etc/systemd/system/acestream.service
sudo rm -rf /opt/acestream/
```
