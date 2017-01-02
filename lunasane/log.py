import sys, os
from datetime import datetime
from .data.preferences import replace_vars, preferences, on_pref_update

timefmt = '%Y/%m/%d %H:%M:%S'
log_verbose = False
log_filename = None
err_filename = None
log_fp = None

def log_init():
    """(Re-)initializes the logging system referrencing the preferences.

    This must be called each time the "i18n" section of the preferences is modified.
    Though, in this module we register this func with on_pref_update(), so as long as the
    preferences are not modified irregularly you don't need to care.
    This is automatically called when the module is first loaded,
    so you don't need to care about that either.
    """
    global log_filename, err_filename, log_fp
    if log_fp != None:
        log_fp.close()
        log_fp = None
    log_filename = replace_vars(preferences['log']['standard'])
    err_filename = replace_vars(preferences['log']['error'])
    if (not os.path.exists(os.path.dirname(log_filename))) and preferences['log']['do_standard']:
        os.makedirs(os.path.dirname(log_filename))
    if (not os.path.exists(os.path.dirname(err_filename))) and preferences['log']['do_error']:
        os.makedirs(os.path.dirname(err_filename))
    if preferences['log']['do_standard']:
        log_fp = open(log_filename, 'a')

log_init()

def set_log_verbose(b):
    """Sets whether verbose mode (printing the log to stdout as well as the log file) is on or off.

    :param b: A bool.
    """
    global log_verbose
    log_verbose = b

def _log(s, category='MESSAGE'):
    """Main logging function.

    :param s: The log message.
    :param category: The category of the message (defaults to 'MESSAGE').
    """
    full = category + ' ' + datetime.now().strftime(timefmt) + ' ' + s
    if log_verbose:
        print(full)
    if preferences['log']['do_standard']:
        log_fp.write(full)
        log_fp.write(os.linesep)

def print_exc():
    """Prints the current exception to stderr (always) and to error log file if needed.

    Only intended for internal use.
    This is used in the very top level code (main.py).
    """
    import traceback
    tstr = datetime.now().strftime(timefmt)
    if preferences['log']['do_error']:
        with open(err_filename, 'a') as fp:
            fp.write('EXCEPTION: '+tstr)
            fp.write(os.linesep)
            traceback.print_exc(file=fp)
            fp.close()
    traceback.print_exc()
    if preferences['log']['do_standard']:
        with log_fp as fp:
            fp.write('EXCEPTION: '+tstr)
            fp.write(os.linesep)
            traceback.print_exc(file=fp)
            fp.close()

on_pref_update(log_init)

