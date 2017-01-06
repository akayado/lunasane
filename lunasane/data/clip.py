# TODO MidiToneClip

from .source import Source
from .ids import new_id_classes

ClipID, ClipIDHolder = new_id_classes('clp')

class Clip(ClipIDHolder):
    def __init__(self, track, cid):
        super().__init__(track.domain, cid)
        self.track = track

    # import / export functionalities

    def to_dict(self, basepath):
        d = {}
        d['id'] = self.id.serializable()
        return d

    def _link_items(self):
        pass

class MidiToneClip(Clip):
    pass

class SourceClip(Clip):
    def __init__(self, track, cid, source):
        Clip.__init__(self, track, cid)
        self.source = source
        self.track = track

    def _link_items(self):
        if not isinstance(self.source, Source):
            self.source = self.track.composite.project.source(self.source)

class AudioClip(SourceClip):
    def __init__(self, track, cid, source):
        SourceClip.__init__(self, track, cid, source)


    # import / export functionalities

    def to_dict(self, basepath):
        d = SourceClip.to_dict(self, basepath)
        d['type'] = 'audio'
        return d

def clip_from_dict(track, d):
    if 'id' in d:
        cid = d['id']
    else:
        cid = None

    if d['type'] == 'audio':
        c = AudioClip(track, cid, d['source'])

    return c
