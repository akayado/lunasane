# TODO import / export

import json
from .ids import IDNotFoundError, new_id_classes
from .composite import Composite

ProjectID, ProjectIDHolder = new_id_classes('prj')

class Project(ProjectIDHolder):
    count = 0

    def __init__(self):
        # initialize ProjectIDHolder with domain 0, the only domain.
        super().__init__(0)

        # the domain for discriminating sources with same IDs etc.
        self.domain = self.__class__.count
        self.__class__.count += 1

        self.sources = []


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
        d = {
                'sources': srcs_d,
            }
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    def save(self, filepath):
        pass

    @classmethod
    def from_dict(cls, d):
        def _source_from_dict(p, srcd):
            if srcd['type'] == 'composite':
                src = Composite.from_dict(p, srcd)
            return src
        p = cls()
        p.sources = [_source_from_dict(p, srcd) for srcd in d['sources']]
        return p

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def load(cls, filepath):
        f = open(filepath)
        text = f.read()
        f.close()
        return cls.from_json(text)
