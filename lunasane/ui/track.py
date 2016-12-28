#TODO: Remove composite from __init__'s args.

from qtpy import QtGui, QtWidgets, QtCore
from ..data.uistate import UIState
from .uibase import UIBase

class TrackHeaderUI(QtWidgets.QFrame, UIBase):
    def __init__(self, track, state=None, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.ui_base_init(track.composite.project)
        self.track = track
        self.state = state

        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(self.track.name))

        self.setLayout(layout)

class TrackBodyUI(QtWidgets.QFrame, UIBase):
    def __init__(self, track, state=None, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.ui_base_init(track.composite.project)
        self.track = track
        self.state = state

        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(self.track.name))

        self.setLayout(layout)


