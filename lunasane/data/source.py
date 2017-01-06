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

        #below are placeholders
        self.duration = -1
        self.media_types = []

    def to_dict(self, basepath):
        d = {
                'id': self.id.serializable(),
                'name': self.name,
            }
        return d


class FileSource(Source):
    """Image/audio/video sources that are loaded from files.

    Extracting different ranges/streams of a file should be done with AliasSources.
    """

    AV_TIME_BASE = 1000000

    def __init__(self, project, path, src_id=None):
        """
        :param project: The parent project.
        :param path: The file path, can be a relative path to the project file.
        :param offset: The offset of the source in frames.
        :param duration: The duration of the source in frames. None means use the duration of the FileBuffer.
        """
        super().__init__(project, src_id)
        self.path_original = path
        self.abspath = os.path.abspath(os.path.join(os.path.dirname(project.abspath), path))

        #below are placeholders
        self.ref = None
        self.n_video_streams = -1
        self.n_audio_streams = -1


    # import / export functionalities

    def to_dict(self, basepath):
        d = Source.to_dict(self, basepath)
        d['type'] = 'file'
        d['ref'] = self.path_original
        return d

    def _link_items(self):
        """Internally called when a parent Project is opened.

        Nothing need to be done here.
        """
        pass

    @classmethod
    def from_dict(cls, project, d):
        src = cls(project, d['ref'], d['id'])
        return src


    # Memory management

    def load(self):
        """Opens the file and replace the placeholders.
        """
        if self.ref == None:
            self.ref = av.open(self.abspath)
            self.n_audio_streams = len([s for s in self.ref.streams if s.type == 'audio'])
            self.n_video_streams = len([s for s in self.ref.streams if s.type == 'video'])
            if self.n_audio_streams > 0:
                self.media_types += ['audio']
            if self.n_video_streams > 0:
                self.media_types += ['video']
            self.duration = self.ref.duration / self.AV_TIME_BASE

    def prepare(self, time_range=None):
        """Load data to the buffer if it is not yet, and tell the buffer object to deflate the needed part of it.

        This is a stub.

        :param time_range: What range of data we want. The entire Source by default.
        """
        if self.ref == None:
            self.load()

        ########DO PREPARING###########

    def release(self):
        """Called when a parent Project is closed.

        This is a stub.

        I need to make sure that the gc releases memory as I intend.
        To do that, I need to del the element of self.buffers as well.
        Refcount needed...?
        """
        del self.ref
        self.ref = None
        gc.collect()


    def __del__(self):
        self.release()



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
