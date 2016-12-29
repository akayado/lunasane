import sys
import argparse
from qtpy import QtWidgets, QtGui
from .i18n import _


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
Master singleton object of the software, holds an instance of Application.
"""

class Lunasane:
    instance = None

    def __init__(self, argv):
        if self.__class__.instance != None:
            raise SingletonError(self.__class__)
        self.app = Application(argv)
        self.__class__.instance = self

        parser = argparse.ArgumentParser(prog=_('lunasane'), description=_('app.description'))
        parser.add_argument('projects', metavar='project', type=str, nargs='+', help=_('cl.usage.project.help'))

        self.args = parser.parse_args()
        print(self.args.projects)
        self.projects = []

    def exec_(self):
        return self.app.exec_()
