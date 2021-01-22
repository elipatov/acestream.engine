#! /bin/sh

set -e

echo "Installing Ace Stream Engine...\n"
systemctl is-active --quiet acestream && systemctl stop acestream && echo "acestream service stopped"

mkdir -p /opt/acestream/androidfs
cp -R ./androidfs /opt/acestream/
cp ./acestream.service /opt/acestream/
cp ./acestream.start /opt/acestream/
cp ./acestream.stop /opt/acestream/

if [ ! -f /opt/acestream/androidfs/acestream.engine/env ]; then
     cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 13 | head -n 1 > /opt/acestream/androidfs/acestream.engine/env
fi

if [ ! -h /etc/systemd/system/acestream.service ]; then
     ln -s /opt/acestream/acestream.service /etc/systemd/system/acestream.service
fi

systemctl daemon-reload
PASS=$(cat /opt/acestream/androidfs/acestream.engine/env)
sed -i 's/<-access-token->/'$PASS'/g' /opt/acestream/androidfs/acestream.engine/acestream.conf

systemctl start acestream
systemctl status acestream
echo "Web UI: http://$(hostname -I | awk '{print $1}'):6878/webui/app/$PASS/server"
echo "Ace Stream Engine installed.\n"