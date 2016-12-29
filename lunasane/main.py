import sys, os
from qtpy import QtWidgets, QtGui
from .i18n import _
from .ui.timeline import TimelineUI
from .app import Lunasane

def main():
    lunasane = Lunasane(sys.argv)
    sys.exit(lunasane.exec_())

if __name__ == "__main__":
    main()
