from . import handle, collection, database, utils
from collections.abc import Iterable
import json


class Document(handle.NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)

    def __str__(self):
        return f"{self.handle.UniversalId} {self.handle.ParentDatabase.FilePath}"

    @property
    def is_response(self):
        return self.handle.IsResponse
    IsResponse = is_response

    @property
    def Items(self):
        return self.handle.Items

    @property
    def NoteID(self):
        return self.handle.NoteID

    @property
    def notesURL(self):
        return self.handle.notesURL

    @property
    def ParentDatabase(self):
        db_handle = self.handle.ParentDatabase
        return database.Database(db_handle)

    @property
    def ParentDocumentUNID(self):
        return self.handle.ParentDocumentUNID

    @property
    def Responses(self):
        col_handle = self.handle.Responses
        return collection.DocumentCollection(col_handle)

    @property
    def UniversalID(self):
        return self.handle.UniveralID

    def ComputeWithForm(self):
        pass

    def CopyAllItems(self):
        pass

    def CopyItem(self):
        pass

    def CopyToDatabase(self):
        pass

    def GetItemValue(self, field_name, as_text=False, sep=", "):
        values = [utils.convert_item_value(v) for v in self.handle.GetItemValue(field_name)]
        if not as_text:
            return values

        values = [utils.item_value_to_str(v) for v in values]
        return sep.join(values)


    # HasItem
    # Remove
    # RemoveItem



    def ReplaceItemValue(self, field_name, value):
        if isinstance(value, (list, tuple, set)):
            values = [utils.convert_item_value(v) for v in value]
        else:
            values = utils.convert_item_value(value)

        item_handle = self.handle.ReplaceItemValue(field_name, values)

        # TODO Return Item class instance
        return item_handle


    def Save(self, force=True, createResponse =False, markRead=False):
        return self.handle.Save(force, createResponse, markRead)

    def GetValues(self, fields=None, properties=None, formulas=None, formulas_names=None, as_text=False, sep=", "):
        res = {}

        if fields is None and properties is None and formulas is None:
            fields = []
            for item in self.Items:
                fields.append(item.Name)
            properties = ["UniversalId", "Created"]

        if fields:
            for field in fields if not isinstance(fields, str) and isinstance(fields, Iterable) else [fields]:
                res[field] = self.GetItemValue(field, as_text, sep)

        if properties:
            for prop in properties if not isinstance(properties, str) and isinstance(properties, Iterable) else [properties]:
                value = getattr(self, prop)
                if as_text:
                    value = utils.item_value_to_str(value)
                res[prop] = value

        if formulas:
            if formulas_names is None:
                formulas_names = formulas
            for formula, name in zip(formulas, formulas_names) if not isinstance(formulas, str) and isinstance(formulas, Iterable) else zip([formulas], [formulas_names]):
                res[name] = utils.evaluate(formula, self.handle, as_text, sep)

        return res

    def toJSON(self, fields=None, properties=None, formulas=None, formulas_names=None, as_text=False, sep=", ", default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, as_text, sep)
        return json.dumps(values, default=default, sort_keys=sort_keys, indent=indent)
