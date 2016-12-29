# TODO MidiToneClip

from .source import Source

class Clip:
    def __init__(self, track):
        self.track = track

    # import / export functionalities

    def to_dict(self, basepath):
        d = {}
        return d

    def _link_items(self):
        pass

class MidiToneClip(Clip):
    pass

class SourceClip(Clip):
    def __init__(self, track, source):
        Clip.__init__(self, track)
        self.source = source
        self.track = track

    def _link_items(self):
        if not isinstance(self.source, Source):
            self.source = self.track.composite.project.source(self.source)

class AudioClip(SourceClip):
    def __init__(self, track, source):
        SourceClip.__init__(self, track, source)


    # import / export functionalities

    def to_dict(self, basepath):
        d = SourceClip.to_dict(basepath)
        d['type'] = 'audio'
        return d

def clip_from_dict(track, d):
    if d['type'] == 'audio':
        c = AudioClip(track, d['source'])
    return c
