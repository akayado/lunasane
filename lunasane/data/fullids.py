import os

from .project import Project, source_from_dict, project_from_id, project_from_path
from .uistate import UIState

from .source import Source
from .composite import Composite
from .track import Track
from .clip import Clip

from ..ui.uibase import UIBase

def full_id_from_id(i, domain=None, basepath=None):
    if domain == None:
        domain = i.domain
    return full_id_from_instance(i.ids[domain][i.serializable()], basepath)

def full_id_from_instance(i, basepath=None):
    if isinstance(i, Clip):
        prefix = full_id_from_instance(i.track)
    elif isinstance(i, Track):
        prefix = full_id_from_instance(i.composite)
    elif isinstance(i, Source) or isinstance(i, UIBase):
        prefix = full_id_from_instance(i.project)
    elif isinstance(i, Project):
        pass

    if isinstance(i, Project):
        return 'prj:' + os.path.relpath(i.abspath, basepath)
    else:
        return prefix + '::' + i.id.typed_serializable()

def relative_full_id(fi, project):
    fis = fi.split('::')
    for i, v in enumerate(fis):
        cat, val = v.split(':')
        if cat == 'prj' and project.abspath != None:
            if os.path.abspath(val) == project.abspath:
                fis.pop(i)
            else:
                fis[i] = 'prj:' + os.path.relpath(val, project.abspath)
    return '::'.join(fis)

def full_id_to_instance(fi, baseproject=None):
    fis = fi.split('::')

    for i, v in enumerate(fis):
        cat, val = v.split(':')

        if i == 0:
            if cat == 'prj':
                obj = project_from_id(val)
                if obj == None:
                    obj = project_from_path(val)
            else:
                obj = baseproject
        
        if cat == 'src':
            obj = obj.source(val)
        elif cat == 'trk':
            pass
        elif cat == 'clp':
            pass
        elif cat == 'wgt':
            pass
    
    return obj

