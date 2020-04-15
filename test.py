from notescompy import session, database, document, view, custom_collection
from notescompy.utils import evaluate
import time, datetime
import os

def update_person(doc):
    unid = doc.GetItemValue0("unid")
    db = doc.ParentDatabase
    cc = custom_collection.CustomCollection(True)

    if doc.GetItemValue0("Form") == "Language":
        view = db.get_view("srchPersonsByLanguage")
        field_name = "Languages"
        field_unid_name = "LanguagesUNID"
        new_value = doc.GetItemValue0("Name")
    elif doc.GetItemValue0("Form") == "Level":
        view = db.get_view("srchPersonsByLevel")
        field_name = "Level"
        field_unid_name = "LevelUNID"
        new_value = doc.GetItemValue0("Level")
    else:
        return

    for person_doc in view.GetAllDocumentsByKey(unid):
        field_value = []

        for field_v, field_unid in person_doc.GetValuesT([field_name, field_unid_name]):
            if field_unid == unid:
                field_value.append(new_value)
            else:
                field_value.append(field_v)

        if field_value != person_doc.GetItemValue(field_name):
            person_doc.ReplaceItemValue(field_name, field_value)
            cc.append(person_doc)

    cc.save()

    return cc.to_json("UNID")

s = session.Session(os.environ.get("LN_PASS"))
print(s.UserName)
print(s.notes_property.isonserver)

db = session.open_database('PyLN', 'itcrowd.nsf')
print(db)

# db = session.open_database('PyLN', 'itcrowd.nsf', 'Python', 'python')
# print(db)

all_docs = db.AllDocuments
for doc in all_docs:
    form, unid = doc.GetItemValue('Form')[0], doc.UniversalID
    print(f"name = {form}, unid = {unid}")

v = db.get_view('Persons')
doc = v.get_first_document()
while doc:
    name = doc.GetItemValue('FullName')[0]
    print(f"name = {name}")
    doc = v.get_next_document()


for doc in v:
    name = doc.GetItemValue('FullName')[0]
    print(f"name = {name}")


json = v.to_json()

v = db.get_view('Persons\\By level')

json = v.to_json()

autoupdate = v.AutoUpdate
v.AutoUpdate = False

v.notes_property.AutoUpdate = True
autoupdate = v.AutoUpdate

keys = ["Senior"]
for doc in v.GetAllDocumentsByKey(keys):
    json = doc.to_json(sep=", ")

print()

json = v.GetAllDocumentsByKey(keys).to_json(no_list=True)

col = v.GetAllDocumentsByKey(keys)
json = col.to_json()
print(json)

json = col.to_json(formulas=v, formulas_names=v)
print(json)

print(s.username)
print(s.notes_property.ServerName)
print(s)

doc = db.get_document_by_unid("3F1B416909DE674043258541003445AA")
doc.ReplaceItemValue("Name", "Python")
doc.Save()

agent = db.get_agent("UpdatePerson")
status = agent.Run(doc)

doc.ReplaceItemValue("Name", "Python2")
doc.Save()
# print(update_person(doc))


url = doc.notes_property.NotesUrl
f_save = doc.notes_property.Save
f_save(True, False)

doc.save_to_json("doc.json")
col.save_to_json("col.json")
v = db.get_view("Persons\\By language")
v.save_to_json("view.json")

col = db.search("@contains(FullName; 'John')")
col.save_to_json("col_search.json", formulas=v, formulas_names=v)


cc = custom_collection.CustomCollection()

cc.append(v)
cc.append(col)
cc.append(doc)

for doc in cc:
    print(doc.GetValuesT(["Form", "UNID"]))

cc.append(db.create_document())
cc.stamp_all("test1", "ok")
# cc.save()


cc = custom_collection.CustomCollection(True)

cc.append(v)
cc.append(col)
cc.append(doc)

for doc in cc:
    print(doc.GetValuesT(["Form", "UNID"]))


cc.save_to_json("custom.json", ["Form", "UNID"])


cc = custom_collection.CustomCollection()
cc.append(db.create_document())
cc.append(db.create_document())
cc.save()