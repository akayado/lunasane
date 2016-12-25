import sys
from qtpy import QtWidgets, QtGui

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
