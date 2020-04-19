from notescompy import init_session, open_database

s = init_session("python")
print(s.UserName)

db = open_database('PyLN', 'itcrowd.nsf')
print(db.title, db.size)

all_col = db.all_documents
acl = db.acl
doc = db.get_document_by_unid("9A899214038E229843258541003BFFDB")
new_doc = db.create_document()
view = db.get_view("Levels")
agent = db.get_agent("UpdatePerson")
col = db.search("@contains(FullName;'John')")
pass
