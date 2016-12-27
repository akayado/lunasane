#TODO: Remove composite from __init__'s args.

from qtpy import QtGui, QtWidgets, QtCore
from .track import TrackHeaderUI, TrackBodyUI
from ..data.uistate.timeline import TimelineUIState

class TimelineUI(QtWidgets.QFrame):
    def __init__(self, composite, state, parent=None):
        super().__init__(parent)
        self.composite = composite
        self.state = state
        self.initialize_ui()

    def initialize_ui(self):
        self.setFrameStyle(self.NoFrame)

        layout = QtWidgets.QVBoxLayout()

        hsplitter = QtWidgets.QSplitter(self)

        header_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, hsplitter)
        body_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, hsplitter)


        # Connect track header splitters to track body splitters

        last_moved = None
        def header_moved(a,b):
            nonlocal last_moved
            if last_moved != None:
                return
            last_moved = 'header'
            body_splitter.moveSplitter(a,b)
            last_moved = None
        def body_moved(a,b):
            nonlocal last_moved
            if last_moved != None:
                return
            last_moved = 'body'
            header_splitter.moveSplitter(a,b)
            last_moved = None
            
        header_splitter.splitterMoved.connect(header_moved)
        body_splitter.splitterMoved.connect(body_moved)

        
        # Generate tracks

        for track in self.composite.tracks:
            header_splitter.addWidget(TrackHeaderUI(track, None, header_splitter))
            body_splitter.addWidget(TrackBodyUI(track, None, body_splitter))

        hsplitter.addWidget(header_splitter)
        hsplitter.addWidget(body_splitter)

        layout.addWidget(hsplitter)

        self.setLayout(layout)
        

