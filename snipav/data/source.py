from .ids import new_id_class

SourceID = new_id_class('src')

class Source:
    def __init__(self, project, src_id=None):
        self.project = project

        if src_id == None:
            self.id = SourceID(project.domain)
        elif src_id.__class__ == SourceID:
            self.id = src_id
        else:
            self.id = SourceID(project.domain, src_id)

    def to_dict(self):
        d = {
                'id': self.id.serializable(),
            }
        return d

    @classmethod
    def from_dict(cls, project, d):
        return None
