import sys, os, json
from .data.preferences import var_prefix, consts, replace_vars, preferences, on_pref_update

dictionary = None
i18n_dir = None
language = None
languages = None

check_all_langs = False

def i18n_init(lang=None):
    """ (Re-)initializes i18n module.

    This must be called each time the "i18n" section of the preferences is modified.
    In this module we register this func with on_pref_update(), so as long as the
    preferences are not modified irregularly you don't need to care.
    This is automatically called when the module is first loaded,
    so you don't need to care about that either.

    :param lang: The language to initialize to.
    """

    global dictionary, i18n_dir, language, languages

    i18n_dir = replace_vars(preferences['i18n']['dir'])
    languages = [replace_vars(l) for l in preferences['i18n']['languages']]

    if lang == None:
        language = preferences['i18n']['language']
    else:
        language = lang

    i18n_fp = open(os.path.join(i18n_dir, language+'.json'))
    dictionary = json.load(i18n_fp)
    i18n_fp.close()

def add_to_dicts(key):
    """Adds a key to dictionaries of all languages, if it doesn't exist.

    Intended to be used internally by _().

    :param key: The key to add.
    """

    global dictionary, languages, i18n_dir
    if key not in dictionary:
        dictionary[key] = key
    for l in languages:
        with open(os.path.join(i18n_dir, l+'.json')) as fp:
            d = json.load(fp)
            fp.close()
        if key not in d:
            d[key] = key
        with open(os.path.join(i18n_dir, l+'.json'), 'w') as fp:
            json.dump(d, fp, ensure_ascii=False, indent=4, sort_keys=True)
            fp.close()

def _(s):
    """Translation.

    If s is not in the current language's dictionary, it is going to
    be added to each language's dictionary that doesn't have it
    for convenience.

    :param s: str to be translated.
    """

    if s in dictionary:
        return dictionary[s]
    if s not in dictionary or check_all_langs:
        add_to_dicts(s)
        return s

on_pref_update(i18n_init)

i18n_init()
