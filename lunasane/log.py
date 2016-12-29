import sys, os
from datetime import datetime
from .data.preferences import replace_vars, preferences, on_pref_update

log_verbose = False
log_filename = None

def log_init():
    global log_filename
    log_filename = replace_vars(preferences['log']['standard'])
    if not os.path.exists(os.path.dirname(log_filename)):
        os.makedirs(os.path.dirname(log_filename))

def set_log_verbose(b):
    global log_verbose
    log_verbose = b

def _log(s):
    full = datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' ' + s
    if log_verbose:
        print(full)
    if preferences['log']['do_standard']:
        with open(log_filename, 'a') as fp:
            fp.write(full)
            fp.write(os.linesep)
            fp.close()

on_pref_update(log_init)

log_init()
