from . import handle, collection, database, utils, view
from collections.abc import Iterable
import random

class Document(handle.NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)
        self.backup = None

    def __str__(self):
        return f"{self.handle.UniversalId} {self.GetItemValue0('Form')} {self.handle.ParentDatabase.FilePath}"

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
        return self.handle.UniversalID

    def ComputeWithForm(self, doDataTypes=False, raiseError=False):
        return self.handle.ComputeWithForm(doDataTypes, raiseError)

    def CopyAllItems(self, doc, replace=False):
        if isinstance(doc, Document):
            return self.handle.CopyAllItems(doc.handle, replace)
        else:
            return self.handle.CopyAllItems(doc, replace)

    def CopyToDatabase(self, db):
        if isinstance(db, database.Database):
            new_doc_handle = self.handle.CopyToDatabase(db.handle)
        else:
            new_doc_handle = self.handle.CopyToDatabase(db)

        return Document(new_doc_handle)

    def GetItemValue(self, field_name, no_list=False, sep=None):
        values = [utils.convert_item_value(v) for v in self.handle.GetItemValue(field_name)]

        if sep is None:
            if no_list and len(values) == 1:
                values = values[0]
            return values

        values = [utils.item_value_to_str(v) for v in values]
        return sep.join(values)

    def GetItemValue0(self, field_name):
        return self.GetItemValue(field_name)[0]

    def HasItem(self, itemName):
        return self.handle.HasItem(itemName)

    def Remove(self, force=True):
        raise ValueError("Cant remove")
        return self.handle.Remove(force)

    def RemoveItem(self, itemName):
        self.handle.RemoveItem(itemName)

    def ReplaceItemValue(self, field_name, value):
        if isinstance(value, (list, tuple, set)):
            values = [utils.convert_item_value(v) for v in value]
        else:
            values = utils.convert_item_value(value)

        item_handle = self.handle.ReplaceItemValue(field_name, values)

        # TODO Return Item class instance
        return item_handle

    def Save(self, force=True, createResponse=False, markRead=False):
        if random.randint(1, 5) == 1:
            raise ValueError("Random Save Error")

        return self.handle.Save(force, createResponse, markRead)

    def GetValues(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=False, sep=None):
        res = {}

        if fields is None and properties is None and formulas is None:
            fields = []
            for item in self.Items:
                fields.append(item.Name)
            properties = ["UniversalId", "Created"]

        if fields:
            for field in fields if not isinstance(fields, str) and isinstance(fields, Iterable) else [fields]:
                res[field] = self.GetItemValue(field, no_list, sep)

        if properties:
            for prop in properties if not isinstance(properties, str) and isinstance(properties, Iterable) else [properties]:
                value = getattr(self.notes_property, prop)
                if sep:
                    value = utils.item_value_to_str(value)
                res[prop] = value

        if isinstance(formulas_names, view.View):
            formulas_names = formulas_names.titles

        if formulas:
            if formulas_names is None:
                formulas_names = formulas

            if isinstance(formulas, view.View):
                formulas = formulas.formulas

            for formula, name in zip(formulas, formulas_names) if not isinstance(formulas, str) and isinstance(formulas, Iterable) else zip([formulas], [formulas_names]):
                res[name] = utils.evaluate(formula, self.handle, no_list, sep)

        return res

    def to_json(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
        utils.save_to_json(values, fp, default, sort_keys, indent)

    def GetValuesT(self, fields):
        return tuple(zip(*[self.GetItemValue(field) for field in fields]))

    def copy(self, db=None, from_disk=False):
        if db is None:
            db = self.ParentDatabase

        copy_doc = db.create_document()
        if from_disk:
            from_disk_doc = db.get_document_by_unid(self.UniversalID)
            from_disk_doc.CopyAllItems(copy_doc)
        else:
            self.CopyAllItems(copy_doc)
        return copy_doc

    @property
    def IsNewNote(self):
        return self.handle.IsNewNote

    @property
    def has_backup(self):
        if self.backup is None:
            return False
        return True

    def create_backup(self):
        if not self.IsNewNote:
            backup = self.copy(from_disk=True)
            self.backup = backup
            return backup

    def restore_backup(self):
        if not self.has_backup:
            raise ValueError("Backup not created")

        backup = self.backup
        backup.CopyAllItems(self, True)



