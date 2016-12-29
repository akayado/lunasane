from .ids import DomainHolder
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


    # get a child track by its ID
    
    def track(self, trk_id):
        pass


    # import / export functionalities

    def to_dict(self, basepath):
        d = Source.to_dict(self, basepath)
        d['type'] = 'composite'
        d['tracks'] = [t.to_dict(basepath) for t in self.tracks]
        return d

    def _link_items(self):
        for t in self.tracks:
            t._link_items()

    @classmethod
    def from_dict(cls, project, d):
        comp = cls(project, d['id'])
        comp.tracks = [track_from_dict(comp, track_d) for track_d in d['tracks']]
        comp.name = d['name']
        return comp
