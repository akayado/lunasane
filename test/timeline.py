import sys, os
sys.path.append(os.curdir)
from qtpy import QtWidgets, QtGui
from lunasane.i18n import _
from lunasane.ui.timeline import TimelineUI
from lunasane.data.project import Project
from lunasane.data.track import Track

def main():
    app = QtWidgets.QApplication(sys.argv)

    proj = Project.load('test/test.json')

    tl_ui = TimelineUI(proj.ui_states[0])

    tl_ui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
