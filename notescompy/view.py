from . import handle, iterdoc, document, collection
import json


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



    def GetValues(self, as_text=False, sep=", "):
        res = {}

        fields = None
        properties = None
        formulas = self.formulas
        formulas_names = self.titles

        for doc in self:
            doc_res = doc.GetValues(fields, properties, formulas, formulas_names, as_text, sep)
            res[doc.UniversalID] = doc_res

        return res

    def toJSON(self, as_text=False, sep=", ",
               default=str, sort_keys=True, indent=4):
        values = self.GetValues(as_text, sep)
        return json.dumps(values, default=default, sort_keys=sort_keys, indent=indent)

    @property
    def formulas(self):
        formulas = []
        columns = self.handle.Columns
        for column in columns:
            if column.isFormula:
                formulas.append(column.Formula)
            else:
                formulas.append(column.ItemName)
        return formulas

    @property
    def titles(self):
        titles = []
        columns = self.handle.Columns
        for column in columns:
            if column.Title:
                titles.append(column.Title)
            else:
                titles.append(column.ItemName)
        return titles
