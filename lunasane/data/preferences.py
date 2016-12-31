import sys, os
import json

var_prefix = '@'
consts = {
    'SCRIPT_ROOT': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')),
    'USER_HOME': os.path.abspath(os.path.expanduser('~')),
}

pref_path = os.path.join(consts['SCRIPT_ROOT'], 'config', 'preferences.json')

pref_fp = open(pref_path)
preferences = json.load(pref_fp)
pref_fp.close()

def replace_vars(s):
    res = str(s)
    for k in consts.keys():
        res = res.replace(var_prefix+k, consts[k])
    return res


on_pref_update_funcs = []
def on_pref_update(func):
    global on_pref_update_funcs
    on_pref_update_funcs += [func]

def update_preferences():
    for f in on_pref_update_funcs:
        f()
