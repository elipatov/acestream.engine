import sys
import os

DEBUG_MODULE = False
GOT_RCP_HOST = True

if DEBUG_MODULE:
    sys.path.insert(0, '/usr/share/acestream/lib')
    class droid:
        @staticmethod
        def getAceStreamHome():
            return os.path.abspath(os.path.dirname(sys.argv[0]))

        @staticmethod
        def makeToast(msg):
            print msg
else:
    try:
        import android
        droid = android.Android()
    except:
        traceback.print_exc()
        print "Continue without RPC host"
        GOT_RCP_HOST = False

#TODO: check for read-only filesystem

default_home_dir = "/sdcard/org.acestream.engine"
if not GOT_RCP_HOST:
    home_dir = default_home_dir
else:
    try:
        home_dir = droid.getAceStreamHome()
    except:
        print "Failed to get home"
        traceback.print_exc()
        home_dir = default_home_dir

if not DEBUG_MODULE:
    try:
        sys.stderr = open(os.path.join(home_dir, "acestream_std.log"), 'w')
        sys.stdout = sys.stderr
    except:
        pass

try:
    from acestreamengine import Core

    conf_file = os.path.join(home_dir, 'acestream.conf')
    print "try to load conf file", conf_file

    config = None
    parsed_params = []
    if os.path.isfile(conf_file):
        import argparse
        parser = argparse.ArgumentParser(prog="acestream", fromfile_prefix_chars="@")

        try:
            config, parsed_params = parser.parse_known_args(["@" + conf_file])
        except Exception, e:
            print "failed to load conf file: " + str(e)

    params = sys.argv[:]
    params.append('--client-console')
    if parsed_params:
        params.extend(parsed_params)

    Core.run(params)

except Exception, e:
    import traceback
    import time

    try:
        f = open(os.path.join(home_dir, "acestream_error.log"), 'a')
        traceback.print_exc(file=f)
        f.close()
    except:
        pass

    if GOT_RCP_HOST:
        droid.makeToast("%r" % e)
    time.sleep(5)

