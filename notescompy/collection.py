from . import handle, iterdoc
import json


class DocumentCollection(handle.NotesHandle, iterdoc.IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        super(iterdoc.IterDocMixin).__init__()

    def __str__(self):
        return f"{self.handle.Count} documents from {self.handle.ParentDatabase.FilePath}"


    def GetValues(self, fields=None, properties=None, formulas=None, formulas_names=None, as_text=False, sep=", "):
        res = {}

        for doc in self:
            doc_res = doc.GetValues(fields, properties, formulas, formulas_names, as_text, sep)
            res[doc.UniversalID] = doc_res

        return res

    def toJSON(self, fields=None, properties=None, formulas=None, formulas_names=None, as_text=False, sep=", ",
               default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, as_text, sep)
        return json.dumps(values, default=default, sort_keys=sort_keys, indent=indent)