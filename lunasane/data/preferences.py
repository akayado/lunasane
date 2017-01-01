import sys, os
import json

var_prefix = '@'
consts = {
    'SCRIPT_ROOT': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')),
    'USER_HOME': os.path.abspath(os.path.expanduser('~')),
}

pref_path = os.path.join(consts['SCRIPT_ROOT'], 'config', 'preferences.json')
preferences = {}

def load_prefs():
    global preferences
    with open(pref_path) as pref_fp:
        preferences = json.load(pref_fp)
        pref_fp.close()

load_prefs()

def replace_vars(s):
    res = str(s)
    for k in consts.keys():
        res = res.replace(var_prefix+k, consts[k])
    return res


on_pref_update_funcs = []
def on_pref_update(func):
    global on_pref_update_funcs
    on_pref_update_funcs += [func]

def update_preferences(reload_prefs=False):
    from ..log import _log
    if reload_prefs:
        _log('Reloading preferences.')
        load_prefs()
        _log('Reloaded preferences.')
    _log('Firing preference update event.')
    for f in on_pref_update_funcs:
        _log('Preference update callback: ' + str(a))
        f()
    _log('Fired preference update event, all update callbacks were executed.')
