from . import handle, session, view, document, collection, agent, const, acl


class Database(handle.NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)


    @classmethod
    def OpenDatabase(cls, server, filepath, s=None):
        if not s:
            s = session.Session()

        if not s.is_init:
            raise RuntimeError("Session not initialized")

        session_handle = s.handle
        handle = session_handle.GetDatabase(server, filepath)
        return Database(handle)


    @property
    def all_documents(self):
        col_handle = self.handle.AllDocuments
        return collection.DocumentCollection(col_handle)
    AllDocuments = all_documents

    @property
    def file_name(self):
        return self.handle.FileName
    FileName = file_name

    @property
    def file_path(self):
        return self.handle.FilePath
    FilePath = file_path

    @property
    def is_open(self):
        return self.handle.IsOpen
    IsOpen = is_open

    @property
    def server(self):
        return self.handle.server
    Server = server

    @property
    def size(self):
        return self.handle.Size
    size = size

    @property
    def title(self):
        return self.handle.title
    Title = title

    def get_document_by_id(self, note_id):
        doc_handle = self.handle.GetDocumentByID(note_id)
        doc = document.Document(doc_handle)
        return doc

    GetDocumentByID = get_document_by_id

    def get_document_by_unid(self, unid):
        doc_handle = self.handle.GetDocumentByUNID(unid)
        if not doc_handle:
            return None
        return document.Document(doc_handle)

    GetDocumentByUNID = get_document_by_unid

    def get_view(self, view_name):
        view_handle = self.handle.GetView(view_name)
        if not view_handle:
            return None
        return view.View(view_handle)

    GetView = get_view


    def get_agent(self, agent_name):
        agent_handle = self.handle.GetAgent(agent_name)
        return agent.Agent(agent_handle)

    def search(self, formula, notesDateTime=const.nothing, maxDocs=0):
        col_handle = self.handle.search(formula, notesDateTime, maxDocs)
        return collection.DocumentCollection(col_handle)

    def create_document(self):
        return document.Document(self.handle.CreateDocument())


    @property
    def acl(self):
        acl_handle = self.handle.ACL
        return acl.ACL(acl_handle)


    def __str__(self):
        return f"{self.title} ({self.server} {self.file_path})" if self.is_open else "Not open"



