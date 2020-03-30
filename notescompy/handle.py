class _NotesHandle:
    def __init__(self):
        self.handle = None

    @property
    def handle(self):
        return self._handle

    @handle.setter
    def handle(self, h):
        self._handle = h

    def __getattr__(self, item):
        return getattr(self.handle, item)