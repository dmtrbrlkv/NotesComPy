from .handle import _NotesHandle
from .document import Document


class View(_NotesHandle):
    def __init__(self, handle):
        super().__init__()
        self.handle = handle
        self.current_doc = None

    def get_first_document(self):
        doc_handle = self.handle.getFirstDocument()
        self.current_doc = Document(doc_handle)

    def get_next_document(self):
        if self.current_doc is None:
            raise ValueError("Current doc not set")

        doc_handle = self.handle.getNextDocument(self.current_doc.handle)
        self.current_doc = Document(doc_handle)