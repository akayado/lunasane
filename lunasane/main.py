import sys, os
from qtpy import QtWidgets, QtGui
from .i18n import _
from .ui.timeline import TimelineUI
from .app import Lunasane
from .log import print_exc

def main():
    try:
        lunasane = Lunasane(sys.argv)
        sys.exit(lunasane.exec_())
    except(SystemExit):
        pass
    except:
        print_exc()

if __name__ == "__main__":
    main()
