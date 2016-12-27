from qtpy import QtGui, QtWidgets, QtCore
from ..data.uistate.track import TrackUIState

class TrackHeaderUI(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("head"))

        self.setLayout(layout)

class TrackBodyUI(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("body"))

        self.setLayout(layout)


