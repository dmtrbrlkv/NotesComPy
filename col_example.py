from notescompy import init_session, open_database
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
view = db.get_view("srchPersonsByLanguage")
col = view.get_all_documents_by_key("3F1B416909DE674043258541003445AA")
doc = col.GetFirstDocument()
while doc:
    print(doc.universal_id)
    doc = col.GetNextDocument()

for doc in col:
    print(doc.universal_id)

persons_view = db.get_view("Persons")

print(col.get_values())
print(col.get_values(formulas=persons_view, formulas_names=persons_view))