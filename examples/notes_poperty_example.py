from notescompy import init_session, open_database
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
print(db.notes_property.ReplicaID)