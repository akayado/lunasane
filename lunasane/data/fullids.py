"""A module for full-ids 

A Full-ID is a str that has the following format.

src::SOURCE ID[>trk::TRACK ID[>clp::CLIP ID]]
wgt::TOP LEVEL WIDGET ID

An item can refer to another using a Full-ID.
"""

import os

from .project import Project, source_from_dict, project_from_id, loaded_project_from_path
from .uistate import UIState

from .source import Source
from .composite import Composite
from .track import Track
from .clip import Clip

from ..ui.uibase import UIBase

from .ids import seps, IDNotFoundError

def full_id_from_instance(i):
    if isinstance(i, Clip):
        prefix = full_id_from_instance(i.track)
    elif isinstance(i, Track):
        prefix = full_id_from_instance(i.composite)
    elif isinstance(i, Source) or isinstance(i, UIBase):
        return i.id.typed_serializable()

    return prefix + seps[1] + i.id.typed_serializable()

def full_id_to_instance(fi, baseproject):
    fis = fi.split(seps[1])

    obj = baseproject

    for i, v in enumerate(fis):
        cat, val = v.split(seps[0])

        if cat == 'src':
            obj = obj.source(val)
        elif cat == 'trk':
            obj = obj.track(val)
        elif cat == 'clp':
            obj = obj.clip(val)
        elif cat == 'wgt':
            obj = obj.ui(val)
    
    return obj

