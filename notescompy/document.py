from .handle import _NotesHandle


class Document(_NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)

    def __str__(self):
        return f"{self.handle.UniversalId} {self.handle.ParentDatabase.FilePath}"
