class ProxyProperty:
    @classmethod
    def create(cls, handle):
        pp = ProxyProperty()
        pp.__dict__["_handle"] = handle
        return pp

    def __init__(self,):
        pass

    def __getattr__(self, item):
        return getattr(self._handle, item)

    def __setattr__(self, name, value):
        setattr(self._handle, name, value)


class NotesHandle:
    def __init__(self, handle):
        self.handle = handle

    @property
    def handle(self):
        return self._handle

    @handle.setter
    def handle(self, h):
        self._handle = h
        self.pp = ProxyProperty.create(h)

    @property
    def notes_property(self):
        return self.pp

    # @notes_property.setter
    # def notes_property(self, v):
    #     return ProxyProperty(self.handle)
