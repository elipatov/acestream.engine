#!/system/bin/busybox sh

export ACESTREAM_HOME=/acestream.engine
export ANDROID_ROOT=/system
export ANDROID_DATA=/data
export PYTHONHOME=$ACESTREAM_HOME/python
export PYTHONPATH=$PYTHONPATH:$ACESTREAM_HOME/python/lib/modules:$ACESTREAM_HOME/python/lib/stdlib.zip
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ACESTREAM_HOME/python/lib:$ACESTREAM_HOME/python/lib/modules
export TEMP=/tmp

if [ ! -d /bin ]; then
mkdir bin
fi
if [ ! -d /sbin ]; then
mkdir sbin
fi
if [ ! -d /data ]; then
mkdir data
fi
if [ ! -d /tmp ]; then
mkdir tmp
fi

if [ `ls /bin | wc -l` -eq 0 ]; then
/system/bin/busybox --install -s
fi
if [ `ls /sbin | wc -l` -eq 0 ]; then
/system/bin/busybox --install -s
fi

cd $ACESTREAM_HOME
$ACESTREAM_HOME/python/bin/python main.py
