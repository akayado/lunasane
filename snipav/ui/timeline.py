from qtpy import QtGui, QtWidgets, QtCore

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

class TimelineUI(QtWidgets.QFrame):
    def __init__(self, timeline, parent=None):
        super().__init__(parent)
        self.timeline = timeline
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

        for i in range(3):
            header_splitter.addWidget(TrackHeaderUI())
            body_splitter.addWidget(TrackBodyUI())

        hsplitter.addWidget(header_splitter)
        hsplitter.addWidget(body_splitter)

        layout.addWidget(hsplitter)

        self.setLayout(layout)
        

