from qtpy import QtGui, QtWidgets, QtCore
from ..data.uistate.track import TrackUIState

class TrackHeaderUI(QtWidgets.QFrame):
    def __init__(self, track, state, parent=None):
        super().__init__(parent)
        self.track = track
        self.state = state

        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(self.track.name))

        self.setLayout(layout)

class TrackBodyUI(QtWidgets.QFrame):
    def __init__(self, track, state, parent=None):
        super().__init__(parent)
        self.track = track
        self.state = state

        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(self.track.name))

        self.setLayout(layout)


