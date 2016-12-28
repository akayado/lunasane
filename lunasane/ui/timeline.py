#TODO: Remove composite from __init__'s args.

from qtpy import QtGui, QtWidgets, QtCore
from .track import TrackHeaderUI, TrackBodyUI
from ..data.uistate import UIState
from .uibase import UIBase


class TimelineUI(QtWidgets.QFrame, UIBase):
    def __init__(self, state, parent=None):
        super().__init__(parent)
        self.state = state
        self.composite = state.project.source(state.params['composite_id'])
        self.ui_base_init(self.composite.project)
        self.track_heads = []
        self.track_bodies = []
        self.initialize_ui()

    def initialize_ui(self):
        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()

        vsplitter = QtWidgets.QSplitter(self)

        self.header_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, vsplitter)
        self.body_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, vsplitter)


        # Connect track header splitters to track body splitters

        last_moved = None
        def header_moved(a,b):
            nonlocal last_moved
            if last_moved != None:
                return
            last_moved = 'header'
            self.body_splitter.moveSplitter(a,b)
            last_moved = None
        def body_moved(a,b):
            nonlocal last_moved
            if last_moved != None:
                return
            last_moved = 'body'
            self.header_splitter.moveSplitter(a,b)
            last_moved = None
            
        self.header_splitter.splitterMoved.connect(header_moved)
        self.body_splitter.splitterMoved.connect(body_moved)

        
        # Generate track UIs

        for track in self.composite.tracks:
            track_head = TrackHeaderUI(track, self.state, self.header_splitter)
            self.track_heads += [track_head]
            self.header_splitter.addWidget(track_head)

            track_body = TrackBodyUI(track, self.state, self.body_splitter)
            self.track_bodies += [track_body]
            self.body_splitter.addWidget(track_body)

        vsplitter.addWidget(self.header_splitter)
        vsplitter.addWidget(self.body_splitter)

        layout.addWidget(vsplitter)

        self.setLayout(layout)
        

