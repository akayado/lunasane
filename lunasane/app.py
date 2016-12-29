import sys
from qtpy import QtWidgets, QtGui
from .i18n import _
from .ui.timeline import TimelineUI


"""
QApplication subclass.
"""

class Application(QtWidgets.QApplication):
    pass


class SingletonError(Exception):
    def __init__(self, cls):
        self.cls = cls

    def __str__(self):
        return str(self.cls)


"""
Master object of the software, holds an instance of Application.
Singleton.
"""

class Lunasane:
    instance = None

    def __init__(self, argv):
        if self.__class__.instance == None:
            self.app = Application(argv)
            self.__class__.instance = self
        else:
            raise SingletonError(self.__class__)

    def exec_(self):
        return self.app.exec_()
