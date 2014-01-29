import subprocess

from watson.ui.base import img_path, WatsonUI

class AppleScriptError(Exception):
    pass


def run_script(script):
    proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(script)
    if proc.returncode != 0:
        raise AppleScriptError('osascript failure: %s'%err)
    out = out.strip()
    if out == 'true':
        return True
    elif out == 'false':
        return False
    elif out.isdigit():
        return int(out)
    else:
        return out

def is_growl_running():
    """Check if Growl is running. Run this before any other Growl functions."""
    script = """
    tell application "System Events"
        set isRunning to (count of (every process whose bundle identifier is "com.Growl.GrowlHelperApp")) > 0
    end tell
    """
    return run_script(script)

def register_app():
    script= """
    tell application id "com.Growl.GrowlHelperApp"
     -- Make a list of all the notification types 
     -- that this script will ever send:
     set the notificationsList to {"Test Successful" , "Test Failure"}

     -- Register our script with growl.
     -- You can optionally (as here) set a default icon 
     -- for this script's notifications.
     register as application "WatsonTest" all notifications notificationsList default notifications notificationsList
    end tell"""
    run_script(script)

def notify(type, title, msg, img='green.png'):
    script= """
    on get_image(imgPath)
        set imgfd to open for access POSIX file imgPath
        set img to read imgfd as "TIFF"
        close access imgfd
        return img
    end get_image
    set noteImage to get_image("%s")
    tell application id "com.Growl.GrowlHelperApp"
     notify with name "%s" title "%s" description "%s" application name "WatsonTest" image noteImage
    end tell"""%(img_path(img), type, title, msg)
    run_script(script)

class GrowlUI(WatsonUI):
    """A Watson UI that uses Growl2. Only supported on OS X."""
    
    name = 'growl2'
    platform = 'darwin'
    
    def __init__(self):
        self.has_growl = is_growl_running()
        if self.has_growl:
            register_app()
    
    def notify(self, failure, title, msg, icon):
        self.has_growl
        if self.has_growl:
            type = failure and 'Test Failure' or 'Test Successful'
            notify(type, title, msg, icon+'.png')