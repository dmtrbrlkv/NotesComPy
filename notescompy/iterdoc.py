class IterDocMixin:
    def __init__(self):
        self._current_doc = None

    def get_first_document(self):
        iterator = iter(self)
        return next(iterator)

    def get_next_document(self):
        try:
            return next(self)
        except StopIteration:
            return None

    def __iter__(self):
        self._current_doc = None
        return self

    def __next__(self):
        from .document import Document

        if not self._current_doc:
            doc_handle = self.handle.getFirstDocument()
        else:
            doc_handle = self.handle.getNextDocument(self._current_doc.handle)
        if not doc_handle:
            self._current_doc = None
            raise StopIteration
        self._current_doc = Document(doc_handle)
        return self._current_doc