from . import handle, iterdoc, document, collection


class View(handle.NotesHandle, iterdoc.IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        super(iterdoc.IterDocMixin).__init__()

    def get_all_documents_by_key(self, keys, exact_match=False):
        col_handle = self.handle.GetAllDocumentsByKey(keys, exact_match)
        return collection.DocumentCollection(col_handle)
    GetAllDocumentsByKey = get_all_documents_by_key

    def get_document_by_key(self, keys, exact_match=False):
        doc_handle = self.handle.GetDocumentByKey(keys, exact_match)
        if doc_handle:
            return document.Document(doc_handle)
        else:
            return None
    GetDocumentByKey = get_document_by_key


    @property
    def auto_update(self):
        return self.handle.AutoUpdate

    @auto_update.setter
    def auto_update(self, value):
        self.handle.AutoUpdate = value
    AutoUpdate = auto_update


    @property
    def entry_count(self):
        return self.handle.EntryCount
    EntryCount = entry_count

    @property
    def name(self):
        return self.handle.Name
    Name = name


    def __str__(self):
        return f"View {self.name}, {self.entry_count} entries"

