import os
import sys
import threading
import traceback

from datetime import datetime

OUTPUT_CONSOLE = True
DEBUG_MODULE = True
GOT_RCP_HOST = True

if DEBUG_MODULE:
    sys.path.insert(0, '/usr/share/acestream/lib')
    class droid:
        @staticmethod
        def getAceStreamHome():
            return os.path.abspath(os.path.dirname(sys.argv[0]))

        @staticmethod
        def makeToast(msg):
            print(msg)
else:
    try:
        import app_bridge
        droid = app_bridge.Android()
    except:
        traceback.print_exc()
        print("Continue without RPC host")
        GOT_RCP_HOST = False

#TODO: check for read-only filesystem

default_home_dir = "/sdcard/org.acestream.engine"
if not GOT_RCP_HOST:
    home_dir = default_home_dir
else:
    try:
        home_dir = droid.getAceStreamHome()
    except:
        print("Failed to get home")
        traceback.print_exc()
        home_dir = default_home_dir

if not OUTPUT_CONSOLE:
    # Cannot redirect output before this point because `home_dir` need to be set
    try:
        sys.stderr = open(os.path.join(home_dir, "acestream_std.log"), 'w')
        sys.stdout = sys.stderr
    except:
        pass

def log(msg):
    try:
        with open(os.path.join(home_dir, 'acestream.log'), 'a') as f:
            f.write('{}|{}|bootstrap|{}\n'.format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                threading.currentThread().name,
                msg
                ))
    except:
        pass

try:
    log('got rpc host: {}'.format(GOT_RCP_HOST))
    from acestreamengine import Core

    conf_file = os.path.join(home_dir, 'acestream.conf')
    log('conf file: {}'.format(conf_file))

    config = None
    parsed_params = []
    if os.path.isfile(conf_file):
        import argparse
        parser = argparse.ArgumentParser(prog="acestream", fromfile_prefix_chars="@")

        try:
            config, parsed_params = parser.parse_known_args(["@" + conf_file])
        except Exception as e:
            log("failed to load conf file: " + str(e))

    params = sys.argv[:]
    params.append('--client-console')
    if parsed_params:
        params.extend(parsed_params)

    Core.run(params)

except Exception as e:
    if OUTPUT_CONSOLE:
        raise
    else:
        log('Got error on start: {}'.format(e))
        try:
            with open(os.path.join(home_dir, "acestream_error.log"), 'a') as f:
                traceback.print_exc(file=f)
        except Exception as e2:
            log('Failed to write to error log: {}'.format(e2))

        if GOT_RCP_HOST:
            droid.makeToast("%r" % e)
