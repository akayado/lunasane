from .ids import new_id_class
from .timeline import Timeline

CompositeID = new_id_class('comp')

class Composite:
    def __init__(self, project, comp_id=None):
        self.project = project

        if comp_id == None:
            self.id = CompositeID(project.domain)
        elif comp_id.__class__ == CompositeID:
            self.id = comp_id
        else:
            self.id = CompositeID(project.domain, comp_id)


    # get timeline object for this composite

    def timeline(self):
        timeline = Timeline()
        return timeline


    # import / export functionalities

    def to_dict(self):
        d = {
                'id': self.id.serializable(),
            }
        return d

    @classmethod
    def from_dict(cls, project, d):
        comp = cls(project, d['id'])
        return comp
