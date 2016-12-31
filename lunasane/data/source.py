from .ids import new_id_classes, IDNotFoundError
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

SourceID, SourceIDHolder = new_id_classes('src')

class Source(SourceIDHolder):
    def __init__(self, project, src_id=None):
        super().__init__(project.domain, src_id)
        self.project = project

    def to_dict(self, basepath):
        d = {
                'id': self.id.serializable(),
                'name': self.name,
            }
        return d


media_ref_dict = {}

def load_media(ref):
    global media_ref_dict

    if ref in media_ref_dict:
        return media_ref_dict[ref]

    media_ref_dict[ref] = VideoFileClip(ref)

    return media_ref_dict[ref]


class FileSource(Source):
    def __init__(self, project, ref_str, src_id=None):
        super().__init__(project, src_id)
        self.ref_str_original = ref_str
        self.ref_str = os.path.join(os.path.dirname(project.abspath), ref_str)
        self.ref = None

    # import / export functionalities

    def to_dict(self, basepath):
        d = Source.to_dict(self, basepath)
        d['type'] = 'file'
        d['ref'] = self.ref_str_original
        return d

    def _link_items(self):
        self.ref = load_media(self.ref_str)


    @classmethod
    def from_dict(cls, project, d):
        src = cls(project, d['ref'], d['id'])
        return src

class AliasSource(Source):
    def __init__(self, project, ref, src_id=None):
        super().__init__(project, src_id)
        if isinstance(ref, Source):
            self.ref = ref
            self.ref_id = full_id_from_instance(ref)
        else:
            self.ref_id = ref
            try:
                self.ref = project.source(ref)
            except(IDNotFoundError):
                self.ref = None
            except:
                raise


    # import / export functionalities

    def to_dict(self, basepath):
        d = Source.to_dict(self, basepath)
        d['type'] = 'alias'
        d['ref'] = self.ref_id
        return d

    def _link_items(self):
        from .fullids import full_id_to_instance
        if self.ref == None:
            self.ref = full_id_to_instance(self.ref_id, self.project)


    @classmethod
    def from_dict(cls, project, d):
        src = cls(project, d['ref'], d['id'])
        return src
