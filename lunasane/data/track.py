from .ids import new_id_classes
from .clip import clip_from_dict

TrackID, TrackIDHolder = new_id_classes('trk')

class Track(TrackIDHolder):
    count = 0
    
    def __init__(self, composite, name, track_id=None):
        super().__init__(composite.domain, track_id)

        # the domain for discriminating clips etc. with same IDs etc.
        self.domain = self.__class__.count
        self.__class__.count += 1

        self.composite = composite
        self.name = name
        self.clips = []


    # import / export functionalities

    def to_dict(self):
        d = {
                'id': self.id,
                'name': self.name,
                'clips': [c.to_dict() for c in self.clips],
            }
        return d

    @classmethod
    def from_dict(cls, composite, d):
        pass

class AudioTrack(Track):
    def __init__(self, composite, name, track_id=None):
        super().__init__(composite, name, track_id)


    # import / export functionalities

    def to_dict(self):
        d = super().to_dict()
        d['type'] = 'audio'
        return d

    @classmethod
    def from_dict(cls, composite, d):
        t = cls(composite, d['name'])
        t.clips = [clip_from_dict(cd) for cd in d['clips']]
        return t

class PianoTrack(AudioTrack):
    def __init__(self, composite, name, track_id=None):
        super().__init__(composite, name, track_id)


    # import / export functionalities

    def to_dict(self):
        d = super().to_dict()
        d['type'] = 'piano'
        return d

    @classmethod
    def from_dict(cls, composite, d):
        t = cls(composite, d['name'])
        t.clips = [clip_from_dict(cd) for cd in d['clips']]
        return t


def track_from_dict(composite, d):
    if d['type'] == 'audio':
        t = AudioTrack.from_dict(composite, d)
    elif d['type'] == 'piano':
        t = PianoTrack.from_dict(composite, d)
    return t

