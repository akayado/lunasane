class LoggedException(Exception):
    def __init__(self, *arg):
        print('logged!')
        super().__init__(**arg)
