from . import handle, collection, database, session
import datetime
import pywintypes

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
        pass

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
        values = [self._convert_value(v) for v in self.handle.GetItemValue(field_name)]
        if not as_text:
            return values
        return sep.join(values)


    # HasItem
    # Remove
    # RemoveItem

    @classmethod
    def _convert_value(cls, value):
        if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
            ndt = session.Session().CreateDateTime(value.isoformat())
            ndt.SetAnyTime()
            v = ndt
        elif isinstance(value, datetime.time):
            ndt = session.Session().CreateDateTime(value.isoformat())
            ndt.SetAnyDate()
            v = ndt
        # elif isinstance(value, pywintypes.datetime):
        #     v = datetime.datetime(
        #         year=value.year,
        #         month=value.month,
        #         day=value.day,
        #         hour=value.hour,
        #         minute=value.minute,
        #         second=value.second
        #     )
        else:
            v = value

        return v

    def ReplaceItemValue(self, field_name, value):
        if isinstance(value, (list, tuple, set)):
            values = [self._convert_value(v) for v in value]
        else:
            values = self._convert_value(value)

        item_handle = self.handle.ReplaceItemValue(field_name, values)

        # TODO Return Item class instance
        return item_handle


    # Save

