import sys
from qtpy import QtWidgets, QtGui
from i18n import _
from ui.timeline import TimelineUI

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    timeline = dict()
    tl_ui = TimelineUI(timeline)

    tl_ui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
