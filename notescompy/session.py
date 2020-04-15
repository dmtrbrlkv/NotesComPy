from . import handle, database
import win32com.client
import enum


class SessionType(enum.Enum):
    LotusNotesSession = "Lotus.NotesSession"
    NotesNotesSession = "Notes.NotesSession"


class UserSession(handle.NotesHandle):
    is_init = False

    def __init__(self, username, password):
        super().__init__(None)
        self.session_type = SessionType.LotusNotesSession
        handle = win32com.client.Dispatch(self.session_type)
        self.handle = handle
        handle.InitializeUsingNotesUserName(username, password)
        Session.is_init = True

    @property
    def username(self):
        return self.handle.username

    UserName = username

    @property
    def _session_type(self):
        return self.session_type

    def __str__(self):
        return self.username if self.handle else "Not initialized"


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Session(handle.NotesHandle, metaclass=SingletonMeta):
    is_init = False

    def __init__(self, password=None, session_type=SessionType.LotusNotesSession):
        super().__init__(None)
        self.session_type = session_type

        if isinstance(session_type, SessionType):
            handle = win32com.client.Dispatch(session_type.value)
        else:
            handle = win32com.client.Dispatch(session_type)

        self.handle = handle

        if not password is None:
            handle.initialize(password)
        else:
            handle.initialize()

        Session.is_init = True

    @property
    def username(self):
        return self.handle.username

    UserName = username

    @property
    def _session_type(self):
        return self.session_type

    def __str__(self):
        return self.username if self.handle else "Not initialized"


def open_database(server, filepath, username=None, password=None):
    if not username:
        db = database.Database.OpenDatabase(server, filepath)
    else:
        user_session = UserSession(username, password)
        db = database.Database.OpenDatabase(server, filepath, user_session)

    return db





