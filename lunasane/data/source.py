from .ids import new_id_classes

SourceID, SourceIDHolder = new_id_classes('src')

class Source(SourceIDHolder):
    def __init__(self, project, src_id=None):
        super().__init__(project.domain, src_id)
        self.project = project

    def to_dict(self):
        d = {
                'id': self.id.serializable(),
            }
        return d

    @classmethod
    def from_dict(cls, project, d):
        return None

