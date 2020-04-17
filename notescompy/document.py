from . import handle, collection, database, utils, view
from collections.abc import Iterable


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
    def items(self):
        return self.handle.Items
    Items = items

    @property
    def note_id(self):
        return self.handle.NoteID
    NoteID = note_id

    @property
    def notes_url(self):
        return self.handle.notesURL
    NotesURL = notes_url

    @property
    def parent_database(self):
        db_handle = self.handle.ParentDatabase
        return database.Database(db_handle)
    ParentDatabase = parent_database

    @property
    def parent_document_unid(self):
        return self.handle.ParentDocumentUNID
    ParentDocumentUNID = parent_document_unid

    @property
    def responses(self):
        col_handle = self.handle.Responses
        return collection.DocumentCollection(col_handle)
    Responses = responses

    @property
    def universal_id(self):
        return self.handle.UniversalID
    UniversalID = universal_id

    def compute_with_form(self, doDataTypes=False, raiseError=False):
        return self.handle.ComputeWithForm(doDataTypes, raiseError)
    ComputeWithForm = compute_with_form

    def copy_all_items(self, doc, replace=False):
        if isinstance(doc, Document):
            return self.handle.CopyAllItems(doc.handle, replace)
        else:
            return self.handle.CopyAllItems(doc, replace)
    CopyAllItems = copy_all_items

    def copy_to_database(self, db):
        if isinstance(db, database.Database):
            new_doc_handle = self.handle.CopyToDatabase(db.handle)
        else:
            new_doc_handle = self.handle.CopyToDatabase(db)

        return Document(new_doc_handle)
    CopyToDatabase = copy_to_database

    def get_item_value(self, field_name, no_list=False, sep=None):
        values = [utils.convert_item_value(v) for v in self.handle.GetItemValue(field_name)]

        if sep is None:
            if no_list and len(values) == 1:
                values = values[0]
            return values

        values = [utils.item_value_to_str(v) for v in values]
        return sep.join(values)
    GetItemValue = get_item_value

    def get_item_value0(self, field_name):
        return self.GetItemValue(field_name)[0]

    GetItemValue0 = get_item_value0

    def has_item(self, itemName):
        return self.handle.HasItem(itemName)
    HasItem = has_item

    def remove(self, force=True):
        return self.handle.Remove(force)
    Remove = remove

    def remove_item(self, itemName):
        self.handle.RemoveItem(itemName)
    RemoveItem = remove_item

    def replace_item_value(self, field_name, value):
        if isinstance(value, (list, tuple, set)):
            values = [utils.convert_item_value(v) for v in value]
        else:
            values = utils.convert_item_value(value)

        item_handle = self.handle.ReplaceItemValue(field_name, values)

        # TODO Return Item class instance
        return item_handle
    ReplaceItemValue = replace_item_value

    def save(self, force=True, createResponse=False, markRead=False):
        return self.handle.Save(force, createResponse, markRead)
    Save = save

    def get_values(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=False, sep=None):
        res = {}

        if fields is None and properties is None and formulas is None:
            fields = []
            for item in self.Items:
                if not item.Name.startswith("$"):
                    fields.append(item.Name)
            properties = ["UniversalId", "Created"]

        if fields:
            for field in fields if not isinstance(fields, str) and isinstance(fields, Iterable) else [fields]:
                res[field] = self.GetItemValue(field, no_list, sep)

        if properties:
            for prop in properties if not isinstance(properties, str) and isinstance(properties, Iterable) else [properties]:
                value = getattr(self.notes_property, prop)
                value = utils.convert_item_value(value)
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
        values = self.get_values(fields, properties, formulas, formulas_names, no_list, sep)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.get_values(fields, properties, formulas, formulas_names, no_list, sep)
        utils.save_to_json(values, fp, default, sort_keys, indent)

    def get_values_t(self, *fields):
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
    def is_new_note(self):
        return self.handle.IsNewNote
    IsNewNote = is_new_note

    @property
    def has_backup(self):
        if self.backup is None:
            return False
        return True

    def create_backup(self):
        if not self.is_new_note:
            backup = self.copy(from_disk=True)
            self.backup = backup
            return backup

    def restore_backup(self):
        if not self.has_backup:
            raise ValueError("Backup not created")

        backup = self.backup
        backup.copy_all_items(self, True)


    def __eq__(self, other):
        return self.parent_database.file_path + self.universal_id == other.parent_database.file_path + other.universal_id

