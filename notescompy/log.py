from . import session, handle, database
import enum

class LogLevel(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    ERROR = 2


class Log(handle.NotesHandle):
    def __init__(self, handle, level=LogLevel.INFO):
        super().__init__(handle)
        self.level = level

    def log(self, msg , isError=False, errNo=0):
        if isError:
            self.handle.LogError(errNo, msg)
        else:
            self.handle.LogAction(msg)

    def debug(self, msg):
        if self.level > LogLevel.DEBUG:
            return
        self.log(msg)

    def info(self, msg):
        if self.level > LogLevel.INFO:
            return
        self.log(msg)

    def error(self, msg, errNo=0):
        self.log(msg, True, errNo)



def FileLog(fp, programName=None, level=LogLevel.INFO, overwrite=False):
    if programName is None:
        programName = ""
    log_handle = session.Session().notes_property.CreateLog(programName)
    log_handle.OverwriteFile = overwrite
    log_handle.OpenFileLog (fp)

    log = Log(log_handle, level)
    return log


def NotesLog(db, programName=None, level=LogLevel.INFO):
    if programName is None:
        programName = ""

    server = db.server
    fp = db.file_path

    log_handle = session.Session().notes_property.CreateLog(programName)
    log_handle.OpenNotesLog(server, fp)

    log = Log(log_handle, level)
    return log