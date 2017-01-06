import sys, os, av
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
    src.prepare()
    print(src.ref, src.duration)

    for s in src.ref.streams:
        print(s, s.duration)
        print(s.type)

        pkts = src.ref.demux(s)
        pkt = next(pkts)
        print(1, pkt.pts)

        pkts = src.ref.demux(s)
        pkt = next(pkts)
        print(1, pkt.pts)

        s.seek(10 * av.time_base)

        pkts = src.ref.demux(s)
        pkt = next(pkts)
        print(2, pkt.pts)

        pkts = src.ref.demux(s)
        pkt = next(pkts)
        print(2, pkt.pts)



    import gc
    
    src.release()
    del proj
    gc.collect()


if __name__ == "__main__":
    main()
