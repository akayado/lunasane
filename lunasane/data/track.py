from .ids import DomainHolder, new_id_classes
from .clip import clip_from_dict

TrackID, TrackIDHolder = new_id_classes('trk')

class Track(TrackIDHolder, DomainHolder):
    """The abstract superclass of all tracks.

    Tracks exist in Composites and can own Clips of their own type.
    Tracks are descriminated by a TrackID.
    """
    count = 0
    domain_dict = {}
    
    def __init__(self, composite, name, track_id=None):
        TrackIDHolder.__init__(self, composite.domain, track_id)

        # initialize DomainHolder for discriminating clips etc. with same IDs etc.
        DomainHolder.__init__(self, Track)

        self.composite = composite
        self.name = name
        self.clips = []

    
    # get a child clip by its ID

    def clip(self, clp_id):
        for c in self.clips:
            if c.id.serializable() == clp_id:
                return c


    # import / export functionalities

    def to_dict(self, basepath):
        d = {
                'id': self.id,
                'name': self.name,
                'clips': [c.to_dict(basepath) for c in self.clips],
            }
        return d
    
    def _link_items(self):
        for c in self.clips:
            c._link_items()

    @classmethod
    def from_dict(cls, composite, d):
        pass

class AudioTrack(Track):
    """The (super)class of all Tracks that have audio-related data.
    """
    def __init__(self, composite, name, track_id=None):
        Track.__init__(self, composite, name, track_id)


    # import / export functionalities

    def to_dict(self, basepath):
        d = Track.to_dict(self, basepath)
        d['type'] = 'audio'
        return d

    @classmethod
    def from_dict(cls, composite, d):
        t = cls(composite, d['name'])
        t.clips = [clip_from_dict(t, cd) for cd in d['clips']]
        return t

class PianoTrack(AudioTrack):
    """The (super)class of all Tracks that can be shown as a piano roll.
    """

    def __init__(self, composite, name, track_id=None):
        AudioTrack.__init__(self, composite, name, track_id)


    # import / export functionalities

    def to_dict(self, basepath):
        d = AudioTrack.to_dict(self, basepath)
        d['type'] = 'piano'
        return d

    @classmethod
    def from_dict(cls, composite, d):
        t = cls(composite, d['name'])
        t.clips = [clip_from_dict(t, cd) for cd in d['clips']]
        return t


def track_from_dict(composite, d):
    if d['type'] == 'audio':
        t = AudioTrack.from_dict(composite, d)
    elif d['type'] == 'piano':
        t = PianoTrack.from_dict(composite, d)
    return t

