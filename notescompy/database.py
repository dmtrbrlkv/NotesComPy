from .handle import _NotesHandle
from .session import Session
from .document import Document
from .view import View
import win32com.client


class Database(_NotesHandle):
    def __init__(self, server, filepath):
        super().__init__()
        if not Session.is_init:
            raise RuntimeError("Session not initialized")

        session_handle = Session().handle
        self.handle = session_handle.GetDatabase(server, filepath)

    # @property
    # def all_documents(self):
    #     pass
    # AllDocuments = all_documents

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
        doc = Document(doc_handle)
        return doc

    GetDocumentByID = get_document_by_id

    def get_document_by_unid(self, unid):
        doc_handle = self.handle.GetDocumentByUNID(unid)
        doc = Document(doc_handle)
        return doc

    GetDocumentByUNID = get_document_by_unid

    def get_view(self, view_name):
        view_handle = self.handle.GetView(view_name)
        return View(view_handle)

    GetView = get_view


    def __str__(self):
        return f"{self.title} ({self.server} {self.file_path})" if self.is_open else "Not open"



