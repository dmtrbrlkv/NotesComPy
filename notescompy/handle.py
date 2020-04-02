class NotesHandle:
    def __init__(self, handle):
        self.handle = handle

    @property
    def handle(self):
        return self._handle

    @handle.setter
    def handle(self, h):
        self._handle = h

    def __getattr__(self, item):
        return getattr(self.handle, item)