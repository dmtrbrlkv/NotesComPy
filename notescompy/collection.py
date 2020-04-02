from . import handle, iterdoc


class DocumentCollection(handle.NotesHandle, iterdoc.IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        super(iterdoc.IterDocMixin).__init__()

    def __str__(self):
        return f"{self.handle.Count} documents from {self.handle.ParentDatabase.FilePath}"
