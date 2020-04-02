import notescompy

s = notescompy.Session("bdoolo87")
print(s.UserName)
print(s.isonserver)

db = notescompy.Database.OpenDatabase('PyLN', 'names.nsf')

alldocs = db.AllDocuments
doc = alldocs.GetFirstDocument()
unid = doc.universalid

doc = db.get_document_by_unid(unid)
print(doc)

print(db)

# all_docs = db.AllDocuments
# for doc in all_docs:
#     form, unid = doc.getitemvalue('Form')[0], doc.universalid
#     print(f"name = {form}, unid = {unid}")

# v = db.get_view('people')
# doc = v.get_first_document()
# while doc:
#     name = doc.getitemvalue('LastName')[0]
#     print(f"name = {name}")
#     doc = v.get_next_document()
#
#
# for doc in v:
#     name = doc.getitemvalue('LastName')[0]
#     print(f"name = {name}")
#
#
# for doc in v:
#     name = doc.getitemvalue('LastName')[0]
#     print(f"name = {name}")



v = db.get_view('testForm')
autoupdate = v.AutoUpdate
v.AutoUpdate = False

keys = ["testform", "AGENT"]
for doc in v.GetAllDocumentsByKey(keys):
    form, unid = doc.getitemvalue('Form')[0], doc.universalid
    print(f"name = {form}, unid = {unid}")

print()

v = db.get_view('testForm')
keys = ["testform", "AGENT"]
for doc in v.GetAllDocumentsByKey("testform"):
    form, unid = doc.getitemvalue('Form')[0], doc.universalid
    print(f"name = {form}, unid = {unid}")


print(s.username)
print(s.ServerName)
print(s)