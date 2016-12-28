from ..data.ids import new_id_classes

UIID, UIIDHolder = new_id_classes('wgt')

class UIBase:
    def __init__(self):
        self.id = None
        self.project = None
        self._id_holder = None

    def ui_base_init(self, project):
        self.project = project
        self._id_holder = UIIDHolder(self.project.domain)
        self.id = self._id_holder.id
