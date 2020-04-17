from notescompy import init_session, open_database
from notescompy.extended_collection import ExtendedCollection
s = init_session("python")

ext_col = ExtendedCollection()

db = open_database('PyLN', 'itcrowd.nsf')
for doc in db.get_view("Levels"):
    ext_col.append(doc)

view = db.get_view("Languages")
ext_col.append(view)

other_col = ExtendedCollection(db.get_view("Persons"))
ext_col.append(other_col)

for doc in ext_col:
    print(doc.get_item_value0("Form"))

ext_col.remove(db.get_view("Persons"))

for doc in ext_col:
    print(doc.get_item_value0("Form"))

print(ext_col.get_values())