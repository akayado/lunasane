from .ids import new_id_classes
from .source import Source, SourceID
from .track import Track, track_from_dict

class Composite(Source):
    count = 0

    def __init__(self, project, comp_id=None):
        super().__init__(project, comp_id)

        # the domain for discriminating tracks with same IDs etc.
        self.domain = self.__class__.count
        self.__class__.count += 1

        self.project = project
        self.tracks = []


    # import / export functionalities

    def to_dict(self):
        d = super().to_dict()
        d['type'] = 'composite'
        d['tracks'] = [t.to_dict for t in self.tracks]
        return d

    @classmethod
    def from_dict(cls, project, d):
        comp = cls(project, d['id'])
        comp.tracks = [track_from_dict(comp, track_d) for track_d in d['tracks']]
        return comp
