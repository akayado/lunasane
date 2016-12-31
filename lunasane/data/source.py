from .ids import new_id_classes

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

    def _link_items(self):
        pass

    @classmethod
    def from_dict(cls, project, d):
        return None

class AliasSource(Source):
    def __init__(self, project, ref, src_id=None):
        super().__init__(project.domain, project, src_id)
        if isinstance(ref, Source):
            self.ref = ref
            self.ref_id = full_id_from_instance(ref)
        else:
            self.ref_id = ref
            try:
                self.ref = project.source(ref)
            except(IDNotFoundError):
                self.ref = full_id_to_instance(ref)
            except:
                raise


    # import / export functionalities

    def __init__(self, project, src_id=None):
        super().__init__(project, src_id)
        self.project = project

    def to_dict(self, basepath):
        d = Source.to_dict(self, basepath)
        d['type'] = 'alias'
        d['ref'] = self.ref_id
        return d

    def _link_items(self):
        from .fullids import full_id_to_instance
        self.ref = full_id_to_instance(self.ref_id, self.project)


    @classmethod
    def from_dict(cls, project, d):
        src = cls(project, d['id'])
        src.ref_id = d['ref']
        return src
