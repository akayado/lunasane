from .ids import new_id_class
from .timeline import Timeline
from .source import Source, SourceID


class Composite(Source):
    def __init__(self, project, comp_id=None):
        super().__init__(project, comp_id)


    # import / export functionalities

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, project, d):
        comp = cls(project, d['id'])
        return comp
