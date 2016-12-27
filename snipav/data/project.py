# TODO import / export

import json
from .ids import NotFoundError
from .composite import Composite, CompositeID

class Project:
    count = 0

    def __init__(self):
        # the domain for discriminating sources with same IDs etc.
        self.domain = self.__class__.count
        self.__class__.count += 1

        self.composites = []


    # get a composite by its ID

    def composite(self, comp_id):
        comp = list(filter(lambda c: c.id == comp_id, self.composites))
        if len(comp) > 0:
            return comp[0]
        else:
            raise NotFoundError(comp_id)


    # import / export functionalities

    def to_dict(self):
        comps_d = [c.to_dict() for c in self.composites]
        d = {
                'composites': comps_d,
            }
        return d

    def to_json(self):
        return json.dumps(self.to_dict())

    def save(self, filepath):
        pass

    @classmethod
    def from_dict(cls, d):
        p = cls()
        p.composites = [Composite.from_dict(p, cd) for cd in d['composites']]
        return p

    @classmethod
    def from_json(cls, json):
        return cls.from_dict(json.loads(json))
    
    @classmethod
    def load(cls, filepath):
        pass
