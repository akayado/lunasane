import sys, os
sys.path.append(os.curdir)
from qtpy import QtWidgets, QtGui
from lunasane.i18n import _
from lunasane.ui.timeline import TimelineUI
from lunasane.data.project import Project, project_from_id, loaded_project_from_path
from lunasane.data.track import Track
from lunasane.data.fullids import full_id_from_instance, full_id_to_instance

def main():
    app = QtWidgets.QApplication(sys.argv)

    proj = Project.load('test/test1.json')
    proj2 = Project.load('test/test1_copy.json')

    tl_ui = TimelineUI(proj.ui_states[0])
    track = Track.from_domain(1)

    print(tl_ui.id.typed_serializable())
    print(track.id.typed_serializable())
    print(loaded_project_from_path('test/test1.json'))
    print(full_id_to_instance('src::src0000', proj))
    print(full_id_to_instance('src::src0000>trk::trk0001', proj))
    print(full_id_to_instance('src::src0000>trk::trk0001>clp::clp0000', proj))
    clip = full_id_to_instance('src::src0000>trk::trk0001>clp::clp0000', proj)
    print(full_id_from_instance(track))
    print(full_id_from_instance(tl_ui))
    print(full_id_from_instance(clip))

    print(full_id_to_instance('src::src0000', proj2))
    print(full_id_to_instance('src::src0000>trk::trk0000', proj2))

if __name__ == "__main__":
    main()
