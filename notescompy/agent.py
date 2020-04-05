from . import handle, document


class Agent(handle.NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)


    def __str__(self):
        return f"{self.handle.Name} from {self.handle.Parent.FilePath}"

    def Run(self, doc=None):
        if isinstance(doc, str):
            noteid = doc
        elif isinstance(doc, document.Document):
            noteid = doc.NoteID
        else:
            noteid = None

        if noteid:
            return self.handle.Run(noteid)
        else:
            return self.handle.Run()

    def RunOnServer(self, doc=None):
        if isinstance(doc, str):
            noteid = doc
        elif isinstance(doc, document.Document):
            noteid = doc.NoteID
        else:
            noteid = None

        if noteid:
            return self.handle.RunOnServer(noteid)
        else:
            return self.handle.RunOnServer()


