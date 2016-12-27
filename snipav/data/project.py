# TODO import / export

import json
from .ids import IDNotFoundError
from .composite import Composite

class Project:
    count = 0

    def __init__(self):
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
            src = None
            return src
        p = cls()
        p.sources = [_source_from_dict(p, srcd) for srcd in d['sources']]
        return p

    @classmethod
    def from_json(cls, json):
        return cls.from_dict(json.loads(json))
    
    @classmethod
    def load(cls, filepath):
        pass
