import sys
from qtpy import QtWidgets, QtGui
from .i18n import _
from .ui.timeline import TimelineUI

class Application(QtWidgets.QApplication):
    pass

class Lunasane:
    def __init__(self, argv):
        self.app = Application(argv)

    def exec_(self):
        return self.app.exec_()
