from notescompy import init_session, open_database, log

s = init_session("python")

logdb = open_database('PyLN', 'dblog.nsf')
l = log.notes_log(logdb, "Python log", log.LogLevel.DEBUG)
# l = log.FileLog("log.log", "Python log", log.LogLevel.INFO)

l.debug("Start")
l.info("Something important")
l.error("Scary error")

try:
    logdb.acl.DeleteRole("ROLE")
except Exception as e:
    l.error(f"Cant delete role: {e}", 5001)

l.info("Done")
l.debug("End")
