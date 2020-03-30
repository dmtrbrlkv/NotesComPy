import notescompy

s = notescompy.Session("bdoolo87")
print(s.UserName)
print(s.isonserver)

db = notescompy.Database('PyLN', 'names.nsf')

alldocs = db.AllDocuments
doc = alldocs.GetFirstDocument()
unid = doc.universalid

doc = db.get_document_by_unid(unid)
print(doc)

print(db)

v = db.get_view('people')
doc = v.get_first_document()
while doc:
    name = doc.getitemvalue('LastName')[0]
    print(f"name = {name}")
    doc = v.get_next_document(doc)

print(s.username)
print(s.ServerName)
print(s)