from . import handle, iterdoc, utils


class DocumentCollection(handle.NotesHandle, iterdoc.IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        super(iterdoc.IterDocMixin).__init__()

    def __str__(self):
        return f"{self.count} documents from {self.handle.ParentDatabase.FilePath}"

    @property
    def count(self):
        return self.handle.Count

    def GetValues(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=False, sep=None):
        res = {}

        for doc in self:
            doc_res = doc.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
            res[doc.UniversalID] = doc_res

        return res

    def to_json(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
        utils.save_to_json(values, fp, default, sort_keys, indent)