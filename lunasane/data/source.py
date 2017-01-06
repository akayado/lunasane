from .ids import new_id_classes, IDNotFoundError
import os, gc, av
from .preferences import preferences

"""
SourceID is a subclass of str, whose instances are used to represent IDs of Source instances.
They can be compared with normal strs.

They don't have to be unique globally, but they have to be unique within a Project domain.
"""
SourceID, SourceIDHolder = new_id_classes('src')

class Source(SourceIDHolder):
    """The abstract superclass of all sources.

    Sources are entities that can be played, and can be placed in a Composite.
    """

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
    """Loads media from ref (abspath) and stores it if it isn't yet.

    ref must be an abspath so that they are unique.

    Returns the corresponding buffer class object.
    """

    global media_ref_dict

    if ref in media_ref_dict:
        return media_ref_dict[ref]

    media_ref_dict[ref] = av.open(ref)

    return media_ref_dict[ref]


class FileSource(Source):
    """Image/audio/video sources that are loaded from files.

    FileSources don't directly own their data (e.g. pixels, sound samples).
    Instead, they refer to a AudioBuffer and/or a VideoBuffer
    (single images are stored in ImageBuffers, which are specialized VideoBuffers).
    This is mainly because a user may want to give different names to the same data,
    and in that case managing the data at one place will save memory.
    """

    def __init__(self, project, ref_str, src_id=None):
        super().__init__(project, src_id)
        self.ref_str_original = ref_str
        self.ref_str = os.path.abspath(os.path.join(os.path.dirname(project.abspath), ref_str))
        self.ref = None

    # import / export functionalities

    def to_dict(self, basepath):
        d = Source.to_dict(self, basepath)
        d['type'] = 'file'
        d['ref'] = self.ref_str_original
        return d

    def _link_items(self):
        """Internally called when a parent Project is opened.
        """
        pass

    def prepare(self, time_range=None):
        """Load data to the buffer if it is not yet, and tell the buffer object to deflate the needed part it.

        This is a stub.

        :param time_range: What range of data we want. The entire Source by default.
        """
        self.ref = load_media(self.ref_str)


    def _release_items(self):
        """Internally called when a parent Project is closed.

        This is a stub.

        I need to make sure that the gc releases memory as I intend.
        """
        if preferences['memory']['release_files']:
            del media_ref_dict[self.ref_str]
        del self.ref
        self.ref = None
        gc.collect()


    @classmethod
    def from_dict(cls, project, d):
        src = cls(project, d['ref'], d['id'])
        return src


    def __del__(self):
        self._release_items()


class AliasSource(Source):
    """A Source that depends on data of another Source.

    Intended to be used for
    creating an alias of a certain time range of a Composite, just for convenience.

    If an AliasSource is an alias of a Composite, this is not a Composite so
    it is not editable.

    For that kind of use, the user should just copy a composite.
    """
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
