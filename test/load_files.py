import sys, os
sys.path.append(os.curdir)
from qtpy import QtWidgets, QtGui
from lunasane.i18n import _
from lunasane.data.project import Project

from memory_profiler import profile

@profile
def main():
    app = QtWidgets.QApplication(sys.argv)

    proj = Project.load('test/test_load.json')
    
    src = proj.sources[0]
    print(src)
    print(src.ref)

    #frame = src.ref.get_frame(0)
    #print(frame)

    import gc

    del proj
    gc.collect()


if __name__ == "__main__":
    main()
