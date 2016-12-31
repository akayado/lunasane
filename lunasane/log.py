import sys, os
from datetime import datetime
from .data.preferences import replace_vars, preferences, on_pref_update

timefmt = '%Y/%m/%d %H:%M:%S'
log_verbose = False
log_filename = None
err_filename = None

def log_init():
    global log_filename, err_filename
    log_filename = replace_vars(preferences['log']['standard'])
    err_filename = replace_vars(preferences['log']['error'])
    if not os.path.exists(os.path.dirname(log_filename)):
        os.makedirs(os.path.dirname(log_filename))
    if not os.path.exists(os.path.dirname(err_filename)):
        os.makedirs(os.path.dirname(err_filename))

def set_log_verbose(b):
    global log_verbose
    log_verbose = b

def _log(s):
    full = datetime.now().strftime(timefmt) + ' ' + s
    if log_verbose:
        print(full)
    if preferences['log']['do_standard']:
        with open(log_filename, 'a') as fp:
            fp.write(full)
            fp.write(os.linesep)
            fp.close()

def print_exc():
    import traceback
    with open(err_filename, 'a') as fp:
        fp.write('EXCEPTION: '+datetime.now().strftime(timefmt))
        fp.write(os.linesep)
        traceback.print_exc(file=fp)
        fp.write(os.linesep)
        fp.close()
    traceback.print_exc()

on_pref_update(log_init)

log_init()
