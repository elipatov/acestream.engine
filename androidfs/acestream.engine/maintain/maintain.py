import sys
import os

try:
    import app_bridge
    droid = app_bridge.Android()
    IS_ANDROID = True

    try:
        home_dir = droid.getAceStreamHome()
    except:
        home_dir = "/sdcard"
except ImportError:
    IS_ANDROID = False
    home_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

if IS_ANDROID:
    try:
        sys.stderr = open(os.path.join(home_dir, "maintain_std.log"), 'w')
        sys.stdout = sys.stderr
    except:
        pass

try:
    import maintain
    params = sys.argv[1:]
    maintain.run(params)

except Exception as e:
    import traceback
    import time

    try:
        if IS_ANDROID:
            with open(os.path.join(home_dir, "maintain_error.log"), 'a') as f:
                traceback.print_exc(file=f)
        else:
            traceback.print_exc()
    except:
        pass

    try:
        droid.makeToast("%r" % e)
        time.sleep(5)
    except:
        pass
