"""
A class for objects that store states of UIs (seekbar position, background etc.).
A UIState must be provided when initializing a UI.
UIs must refer to corresponding UIState objects time to time.
This makes saving/loading UI states and showing multiple views that refer to a 
single set of data possible.
"""

class UIState:
    TYPE_TIMELINE = 'timeline'

    def __init__(self):
        self.type = self.TYPE_TIMELINE
        self.params = {}

    def to_dict(self):
        d = {
                'type': self.type,
                'params': self.params,
            }
        return d

    @classmethod
    def from_dict(cls, d):
        s = cls()
        s.type = d['type']
        s.params = d['params']
        return s
