from .ids import DomainHolder, new_id_classes
from .source import Source, SourceID
from .track import Track, track_from_dict

class Composite(Source, DomainHolder):
    count = 0
    domain_dict = {}

    def __init__(self, project, comp_id=None):
        Source.__init__(self, project, comp_id)

        # initialize DomainHolder for discriminating tracks with same IDs etc.
        DomainHolder.__init__(self)

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
