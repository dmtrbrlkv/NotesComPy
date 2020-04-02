from .handle import _NotesHandle
from ._iterdoc import IterDocMixin


class DocumentCollection(_NotesHandle, IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        super(IterDocMixin).__init__()

    def __str__(self):
        return f"{self.handle.Count} documents from {self.handle.ParentDatabase.FilePath}"