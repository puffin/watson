import subprocess
import platform
import os
import sys
import colorama

COLOR_EXCEPTION = colorama.Fore.RED
COLOR_RESET = colorama.Fore.RESET

from watson.ui.base import WatsonUI

class TerminalNotifierError(Exception):
    pass


def run_script(script):

    args = list(reduce(lambda x, y: x + y, script.items()))
    proc = subprocess.Popen(['terminal-notifier'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = proc.communicate()
    if proc.returncode != 0:
        raise TerminalNotifierError('terminal-notifier failure: %s'%err)
    out = out.strip()
    if out == 'true':
        return True
    elif out == 'false':
        return False
    elif out.isdigit():
        return int(out)
    else:
        return out

def is_available():
    """ Returns whether or not the current platform is Mac OS X 10.8, or higher."""
    return platform.system() == 'Darwin' and platform.mac_ver()[0] >= '10.8'

def is_terminal_notifier_installed():
    proc = subprocess.Popen(["which", "terminal-notifier"], stdout=subprocess.PIPE)

    env_bin_path = proc.communicate()[0].strip()
    if env_bin_path and os.path.exists(env_bin_path):
        bin_path = os.path.realpath(env_bin_path)
    else:
        bin_path = os.path.join("/usr/local/bin/", "terminal-notifier")

    if not is_available():
        raise TerminalNotifierError("terminal-notifier UI is only supported on Mac OS X 10.8, or higher.")

    if not os.path.exists(bin_path):
        raise TerminalNotifierError("terminal-notifier was not properly installed. Head over to https://github.com/alloy/terminal-notifier for more information")

    if not os.access(bin_path, os.X_OK):
        os.chmod(bin_path, 111)
        if not os.access(bin_path, os.X_OK):
            raise TerminalNotifierError("You have no privileges to execute \"%s\"" % bin_path)
    

def notify(type, title, msg):
    script = {'-title': type, '-message': msg}
    run_script(script)

class TerminalNotifierUI(WatsonUI):
    """A Watson UI that uses OSX terminal-notifier. Only supported on OS X."""
    
    name = 'osx'
    platform = 'darwin'
    
    def __init__(self):
        try:
            is_terminal_notifier_installed()
        except TerminalNotifierError, e:
            print(COLOR_EXCEPTION + e.__str__())
            print(COLOR_RESET)
            sys.exit(0)

    @classmethod
    def enabled(cls):
        try:
            is_terminal_notifier_installed()
            return True
        except:
            return False

    def notify(self, failure, title, msg, icon):
        title = 'Watson'
        type = failure and 'Test Failure' or 'Test Successful'
        notify(type, title, msg)