# TODO MidiToneClip

from .source import Source

class Clip:
    def __init__(self, track):
        self.track = track

    # import / export functionalities

    def to_dict(self, basepath):
        d = {}
        return d

class MidiToneClip(Clip):
    pass

class SourceClip(Clip):
    def __init__(self, track, source):
        super().__init__(track)
        if isinstance(source, Source):
            self.source = source
        else:
            self.source = track.composite.project.source(source)

class AudioClip(SourceClip):
    def __init__(self, track, source):
        super().__init__(track, source)


    # import / export functionalities

    def to_dict(self, basepath):
        d = super().to_dict()
        d['type'] = 'audio'
        return d

def clip_from_dict(track, d):
    if d['type'] == 'audio':
        c = AudioClip(track, d['source'])
    return c
