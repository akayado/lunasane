import sys
import argparse
from qtpy import QtWidgets, QtGui
from .i18n import _
from .log import _log, set_log_verbose
from .data.project import Project


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
    version = '0.0.1'

    def __init__(self, argv):
        if self.__class__.instance != None:
            raise SingletonError(self.__class__)
        self.app = Application(argv)
        self.__class__.instance = self

        parser = argparse.ArgumentParser(prog=_('lunasane'), description=_('app.description'))
        parser.add_argument('projects', metavar='project', type=str, nargs='*', help=_('cl.usage.project.help'))
        parser.add_argument('-V', '--verbose', action='store_true', help=_('cl.usage.verbose.help'))
        parser.add_argument('-v', '--version', action='version', help=_('cl.usage.version.help'), version='Lunasane '+self.__class__.version)

        self.args = parser.parse_args()

        set_log_verbose(self.args.verbose)

        _log('started Lunasane')
        if len(self.args.projects) > 0:
            _log('started loading projects')
            self.projects = [Project.load(f) for f in self.args.projects]
            _log('finished loading projects')


    def exec_(self):
        return self.app.exec_()
