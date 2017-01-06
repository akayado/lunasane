"""
Process data management of the app.
"""

import json
import os.path
from .ids import DomainHolder, IDNotFoundError, new_id_classes
from .composite import Composite
from .source import AliasSource, FileSource
from .uistate import UIState

def source_from_dict(p, srcd):
    """Generate a Source object from a dictionary.

    A Project must be supplied as well because all Sources need
    a parent Project.

    :param p: Parent Project.
    :param srcd: The dictionary to be converted to a Source instance.
    """

    if srcd['type'] == 'composite':
        src = Composite.from_dict(p, srcd)
    elif srcd['type'] == 'alias':
        src = AliasSource.from_dict(p, srcd)
    elif srcd['type'] == 'file':
        src = FileSource.from_dict(p, srcd)
    return src


ProjectID, ProjectIDHolder = new_id_classes('prj')


class Project(ProjectIDHolder, DomainHolder):
    """Represents a project.

    Projects save/load project data and UI states.
    A Project corresponds to a main window.

    Projects hold ProjectIDs that CANNOT be used to refer resources among projects.
    Usage of these ProjectIDs don't exist yet, though may occur in the future.

    Each project has a domain number of Sources and UIStates so that Sources in
    different Projects loaded at the same time can have same IDs.
    """

    count = 0 #Counts how many Project domains are created so far.
    domain_dict = {} #Keeps track of which Project corresponds to which domain number.
    instances = {} #dict of IDs as keys and their corresponding Projects as values.

    def __init__(self):
        """Initializes a Project.

        This also updates the domain_dict and instances dict and count.
        Hence just calling Project() is ok for creating a new Project.
        (Then you would set its name etc.)
        """

        # initialize ProjectIDHolder with domain 0, the only domain.
        ProjectIDHolder.__init__(self, 0)

        self.abspath = None
        self.name = "My Project"

        # initialize DomainHolder for discriminating sources with same IDs etc.
        DomainHolder.__init__(self)

        # main data
        self.sources = []

        # UI state data
        self.ui_states = []

        self.__class__.instances[self.id.serializable()] = self
        


    def source(self, src_id):
        """
        Get a source from this Project by its SourceID.

        :param src_id: ID, can be either SourceID or a str.
        """

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
        """Convert Project to a dict.

        :param basepath: Optional, the path of the project file can be set here. If not, self.abspath is used instead.
        """
        if basepath == None:
            basepath = self.abspath
        srcs_d = [c.to_dict(basepath) for c in self.sources]
        states_d = [s.to_dict(basepath) for s in self.ui_states]
        d = {
                'name': self.name,
                'sources': srcs_d,
                'ui_states': states_d
            }
        return d

    def to_json(self, basepath=None):
        """Convert Project to json str.

        :param basepath: Optional, the path of the project file can be set here. If not, self.abspath is used instead.
        """
        return json.dumps(self.to_dict(basepath), sort_keys=True, indent=4)

    def save(self, filepath):
        """Save Project to a json file.

        :param filepath: Where to save it.
        """
        if self.abspath == None:
            self.abspath = os.path.abspath(filepath)
        json_str = self.to_json(os.path.abspath(filepath))

    def _link_items(self):
        for s in self.sources:
            s._link_items()

    @classmethod
    def from_dict(cls, d, abspath):
        """Generate a Project from a dict read from a json file.

        :param d: The dict.
        :param abspath: Absolute path of the json file.
        """
        p = cls()
        p.abspath = abspath
        if 'name' in d:
            p.name = d['name']
        if 'sources' in d:
            p.sources = [source_from_dict(p, srcd) for srcd in d['sources']]
        if 'ui_states' in d:
            p.ui_states = [UIState.from_dict(p, sd) for sd in d['ui_states']]
        p._link_items()
        return p

    @classmethod
    def from_json(cls, json_str, abspath):
        """Generate a Project from json str.

        :param json_str: The json str.
        :param abspath: Absolute path of the json file.
        """
        return cls.from_dict(json.loads(json_str), abspath)
    
    @classmethod
    def load(cls, filepath):
        """Load Project from a json file.

        :param filepath: Where to load from.
        """
        with open(filepath) as f:
            text = f.read()
            f.close()

        p = cls.from_json(text, os.path.abspath(filepath))
        return p

def project_from_id(i):
    """Obtain the corresponding Project instance by an ID.

    :param i: The ID, can be either a str or a ProjectID.
    """
    try:
        p = Project.instances[i]
        return p
    except KeyError:
        raise IDNotFoundError(i, 0)
    except:
        raise

def loaded_project_from_path(p, load_if_not_found=True):
    """Obtain the corresponding Project instance by a file path.

    If the project is not loaded yet, you can choose whether to load it
    with the following option (Defaults to True, which means "load it").

    Thus you can just always use this function to load projects.

    :param p: The file path. Can be relative.
    :param load_if_not_found: Whether or not to load the project if its not loaded yet.
    """

    for v in Project.instances.values():
        if v.abspath == os.path.abspath(p):
            return v
    if load_if_not_found:
        return Project.load(p)
