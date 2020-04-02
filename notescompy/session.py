from .handle import _NotesHandle
import win32com.client


class SessionType:
    LotusNotesSession = "Lotus.NotesSession"
    NotesNotesSession = "Notes.NotesSession"
    Types = [LotusNotesSession, NotesNotesSession]


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Session(_NotesHandle, metaclass=SingletonMeta):
    is_init = False

    def __init__(self, password=None, session_type=SessionType.LotusNotesSession):
        super().__init__(None)
        self.session_type = session_type

        if session_type not in SessionType.Types:
            raise ValueError(f"Unknown session type {session_type}")

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
