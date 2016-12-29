import os

from .project import Project, source_from_dict, project_from_id, project_from_path
from .uistate import UIState

from .source import Source
from .composite import Composite
from .track import Track
from .clip import Clip

from ..ui.uibase import UIBase

from .ids import seps, IDNotFoundError

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
        return 'prj' + seps[0] + os.path.relpath(i.abspath, basepath)
    else:
        return prefix + seps[1] + i.id.typed_serializable()

def relative_full_id(fi, project):
    fis = fi.split(seps[1])
    for i, v in enumerate(fis):
        cat, val = v.split(seps[0])
        if cat == 'prj' and project.abspath != None:
            if os.path.abspath(val) == project.abspath:
                fis.pop(i)
            else:
                fis[i] = 'prj' + seps[0] + os.path.relpath(val, project.abspath)
    return seps[1].join(fis)

def full_id_to_instance(fi, baseproject=None):
    fis = fi.split(seps[1])

    for i, v in enumerate(fis):
        cat, val = v.split(seps[0])

        if i == 0:
            if cat == 'prj':
                try:
                    obj = project_from_id(val)
                except IDNotFoundError:
                    if baseproject == None:
                        obj = project_from_path(val)
                    else:
                        obj = project_from_path(os.path.join(os.path.dirname(baseproject.abspath), val))
                except:
                    raise
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

