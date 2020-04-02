from notescompy import session, database
from notescompy.utils import evaluate
import time, datetime

s = session.Session("bdoolo87")
print(s.UserName)
print(s.isonserver)

db = database.Database.OpenDatabase('PyLN', 'names.nsf')

alldocs = db.AllDocuments
doc = alldocs.GetFirstDocument()
unid = doc.universalid

doc = db.get_document_by_unid(unid)
print(doc)

print(db)

all_docs = db.AllDocuments
for doc in all_docs:
    form, unid = doc.getitemvalue('Form')[0], doc.universalid
    print(f"name = {form}, unid = {unid}")

v = db.get_view('people')
doc = v.get_first_document()
while doc:
    name = doc.getitemvalue('LastName')[0]
    print(f"name = {name}")
    doc = v.get_next_document()


for doc in v:
    name = doc.getitemvalue('LastName')[0]
    print(f"name = {name}")


for doc in v:
    name = doc.getitemvalue('LastName')[0]
    print(f"name = {name}")



v = db.get_view('testForm')
autoupdate = v.AutoUpdate
v.AutoUpdate = False

keys = ["testform", "AGENT"]
keys = evaluate("'testform':'AGENT'")
for doc in v.GetAllDocumentsByKey(keys):
    form, unid = doc.GetItemValue('Form')[0], doc.universalid
    v = evaluate("@DocumentUniqueId", doc)
    resp_col = doc.Responses
    print(f"Responses = {resp_col.count}")
    print(f"name = {form}, unid = {unid}")

    doc.ReplaceItemValue("testField1", "42")
    doc.ReplaceItemValue("testField2", 42)
    doc.ReplaceItemValue("testField3", 42.53)
    doc.ReplaceItemValue("testField4", time.time())
    doc.ReplaceItemValue("testField5", datetime.datetime.today())
    doc.ReplaceItemValue("testField6", datetime.date.fromisoformat("2020-03-23"))
    doc.ReplaceItemValue("testField7", datetime.datetime.now())
    doc.ReplaceItemValue("testField8", ["1", "2", "3"])
    doc.ReplaceItemValue("testField9", [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()])
    doc.ReplaceItemValue("testField10", datetime.time.fromisoformat("12:00"))

    value = doc.GetItemValue("testField1")
    value = doc.GetItemValue("testField2")
    value = doc.GetItemValue("testField3")
    value = doc.GetItemValue("testField4")
    value = doc.GetItemValue("testField5")
    value = doc.GetItemValue("testField6")
    value = doc.GetItemValue("testField7")
    value = doc.GetItemValue("testField8")
    value = doc.GetItemValue("testField9")
    value = doc.GetItemValue("testField10")

    value = doc.GetItemValue("testField1", True)
    value = doc.GetItemValue("testField2", True)
    value = doc.GetItemValue("testField3", True)
    value = doc.GetItemValue("testField4", True)
    value = doc.GetItemValue("testField5", True)
    value = doc.GetItemValue("testField6", True)
    value = doc.GetItemValue("testField7", True)
    value = doc.GetItemValue("testField8", True)
    value = doc.GetItemValue("testField9", True)
    value = doc.GetItemValue("testField10", True)

    values = doc.GetValues(["testField1", "testField7"], ["Size", "UniversalId", "NoteId"], ["@LowerCase(form)"])
    values = doc.GetValues(["testField1", "testField7"], ["Size", "UniversalId", "NoteId"], ["@LowerCase(form)", "@UpperCase(form)"], ["форма", "ФОРМА"], as_text=True)
    values = doc.GetValues("testField7", None, "@UpperCase(form)", "Форма", as_text=True)


    json = doc.toJSON(as_text=True)
    doc.Save(True, False)

print()

v = db.get_view('testForm')
keys = ["testform", "AGENT"]
for doc in v.GetAllDocumentsByKey("testform"):
    form, unid = doc.getitemvalue('Form')[0], doc.universalid
    f = doc.GetItemValue("form", True)

    print(f"name = {form}, unid = {unid}")


print(s.username)
print(s.ServerName)
print(s)