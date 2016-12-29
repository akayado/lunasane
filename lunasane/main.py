import sys, os
from qtpy import QtWidgets, QtGui
from .i18n import _
from .ui.timeline import TimelineUI
from .app import Application

def main():
    app = Application(sys.argv)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
