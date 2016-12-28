import sys, os
sys.path.append(os.curdir)
from qtpy import QtWidgets, QtGui
from lunasane.i18n import _
from lunasane.ui.timeline import TimelineUI
from lunasane.data.project import Project
from lunasane.data.track import Track
from lunasane.data.fullids import full_id_from_instance, full_id_from_id

def main():
    app = QtWidgets.QApplication(sys.argv)

    proj = Project.load('test/test.json')

    tl_ui = TimelineUI(proj.ui_states[0])
    track = Track.from_domain(1)

    print(tl_ui.id.typed_serializable(), full_id_from_instance(tl_ui))
    print(track.id.typed_serializable(), full_id_from_instance(track))

    tl_ui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
