from notescompy import init_session, open_database

s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')

view = db.get_view("Persons")

with open("view.json", "w") as f:
    view.save_to_json(f)


view = db.get_view("srchPersonsByLanguage")
col = view.get_all_documents_by_key("3F1B416909DE674043258541003445AA")
with open("col.json", "w") as f:
    col.save_to_json(f, fields=["FullName", "Level"])


acl = db.acl
with open("acl.json", "w") as f:
    acl.save_to_json(f, asStr=True)
