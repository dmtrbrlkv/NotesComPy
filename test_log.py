from notescompy import session, log
import os

s = session.Session("python")
logdb = session.open_database('PyLN', 'dblog.nsf')

l = log.NotesLog(logdb, "Test log by python", log.LogLevel.DEBUG)
# l = log.FileLog("log.log", "Test log by python", log.LogLevel.INFO)

l.debug("Start")
l.info("Something important")
l.error("Scary error")

try:
    logdb.acl.DeleteRole("ROLE")
except Exception as e:
    l.error(f"Cant delete role: {e}", 5001)

l.info("Done")
l.debug("End")
