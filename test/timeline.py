import sys, os
sys.path.append(os.curdir)
from qtpy import QtWidgets, QtGui
from lunasane.i18n import _
from lunasane.ui.timeline import TimelineUI
from lunasane.data.project import Project

def main():
    app = QtWidgets.QApplication(sys.argv)

    proj = Project.load('test/test.json')
    
    timeline = dict()
    tl_ui = TimelineUI(timeline)

    tl_ui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
