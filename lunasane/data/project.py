import json
import os.path
from .ids import DomainHolder, IDNotFoundError, new_id_classes
from .composite import Composite
from .source import AliasSource, FileSource
from .uistate import UIState

def source_from_dict(p, srcd):
    if srcd['type'] == 'composite':
        src = Composite.from_dict(p, srcd)
    elif srcd['type'] == 'alias':
        src = AliasSource.from_dict(p, srcd)
    elif srcd['type'] == 'file':
        src = FileSource.from_dict(p, srcd)
    return src


ProjectID, ProjectIDHolder = new_id_classes('prj')

"""
Projects save/load project data and UI states.
A Project corresponds to a main window.

Projects hold ProjectIDs that CANNOT be used to refer resources among projects.
Usage of these ProjectIDs don't exist yet, though may occur in the future.
Projects can refer to each other using their file paths (relatie/absolute).
Hence Projects must be saved to a file to be able to be referred to.
"""

class Project(ProjectIDHolder, DomainHolder):
    count = 0
    domain_dict = {}
    instances = {}

    def __init__(self):
        # initialize ProjectIDHolder with domain 0, the only domain.
        ProjectIDHolder.__init__(self, 0)

        self.abspath = None

        # initialize DomainHolder for discriminating sources with same IDs etc.
        DomainHolder.__init__(self)

        # main data
        self.sources = []

        # UI state data
        self.ui_states = []

        self.__class__.instances[self.id.serializable()] = self
        


    # get a source by its ID

    def source(self, src_id):
        src = list(filter(lambda c: c.id == src_id, self.sources))
        if len(src) > 0:
            return src[0]
        else:
            raise IDNotFoundError(src_id, self.domain)

    
    # get a top level ui by its ID

    def ui(self, ui_id):
        pass


    # import / export functionalities

    def to_dict(self, basepath=None):
        if basepath == None:
            basepath = self.abspath
        srcs_d = [c.to_dict(basepath) for c in self.sources]
        states_d = [s.to_dict(basepath) for s in self.ui_states]
        d = {
                'sources': srcs_d,
                'ui_states': states_d
            }
        return d

    def to_json(self, basepath=None):
        return json.dumps(self.to_dict(basepath), sort_keys=True, indent=4)

    def save(self, filepath):
        if self.abspath == None:
            self.abspath = os.path.abspath(filepath)
        json_str = self.to_json(os.path.abspath(filepath))

    def _link_items(self):
        for s in self.sources:
            s._link_items()

    @classmethod
    def from_dict(cls, d, abspath):
        p = cls()
        p.abspath = abspath
        p.sources = [source_from_dict(p, srcd) for srcd in d['sources']]
        p.ui_states = [UIState.from_dict(p, sd) for sd in d['ui_states']]
        p._link_items()
        return p

    @classmethod
    def from_json(cls, json_str, abspath):
        return cls.from_dict(json.loads(json_str), abspath)
    
    @classmethod
    def load(cls, filepath):
        with open(filepath) as f:
            text = f.read()
            f.close()

        p = cls.from_json(text, os.path.abspath(filepath))
        return p

def project_from_id(i):
    try:
        p = Project.instances[i]
        return p
    except KeyError:
        raise IDNotFoundError(i, 0)
    except:
        raise

def loaded_project_from_path(p, load_if_not_found=True):
    for v in Project.instances.values():
        if v.abspath == os.path.abspath(p):
            return v
    if load_if_not_found:
        return Project.load(p)
