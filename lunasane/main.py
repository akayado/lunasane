import sys, os
from .i18n import _
from .app import Lunasane
from .log import _log, print_exc

def main():
    try:
        lunasane = Lunasane(sys.argv)
        sys.exit(lunasane.exec_())
    except(SystemExit):
        _log('Bye-bye.')
        raise
    except:
        print_exc()

if __name__ == "__main__":
    main()
