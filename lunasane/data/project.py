import json
import os.path
from .ids import DomainHolder, IDNotFoundError, new_id_classes
from .composite import Composite
from .uistate import UIState

def source_from_dict(p, srcd):
    if srcd['type'] == 'composite':
        src = Composite.from_dict(p, srcd)
    return src


projects = {}

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
        


    # get a source by its ID

    def source(self, src_id):
        src = list(filter(lambda c: c.id == src_id, self.sources))
        if len(src) > 0:
            return src[0]
        else:
            raise IDNotFoundError(src_id)


    # import / export functionalities

    def to_dict(self):
        srcs_d = [c.to_dict() for c in self.sources]
        states_d = [s.to_dict() for s in self.ui_states]
        d = {
                'sources': srcs_d,
                'ui_states': states_d
            }
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    def save(self, filepath):
        #save

        if self.abspath == None:
            self.abspath = os.path.abspath(filepath)

    @classmethod
    def from_dict(cls, d):
        p = cls()
        p.sources = [source_from_dict(p, srcd) for srcd in d['sources']]
        p.ui_states = [UIState.from_dict(p, sd) for sd in d['ui_states']]
        return p

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def load(cls, filepath):
        f = open(filepath)
        text = f.read()
        f.close()

        p = cls.from_json(text)
        p.abspath = os.path.abspath(filepath)
        return p

def project_from_id(i):
    pass

def project_from_path(i):
    pass
