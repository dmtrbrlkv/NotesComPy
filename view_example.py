from notescompy import init_session, open_database
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
view = db.get_view("Levels")

doc = view.get_first_document()
while doc:
    print(doc.universal_id)
    doc = view.get_next_document()


for doc in view:
    print(doc.universal_id)


view = db.get_view("srchPersonsByLanguage")
col = view.get_all_documents_by_key("3F1B416909DE674043258541003445AA")
print(col.count)

view = db.get_view("Persons")
values = view.get_values(no_list=True, sep= "/")
print(values)