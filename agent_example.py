from notescompy import init_session, open_database
from notescompy.extended_collection import ExtendedCollection
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
view = db.get_view("Levels")

doc = view.get_first_document()

doc.replace_item_value("Level", "Beginer")
doc.save()

agent = db.get_agent("UpdatePerson")
agent.Run(doc)

doc.replace_item_value("Level", "Junior")
doc.save()

ext_col = ExtendedCollection()
ext_col.append(db.get_view("Levels"))

view = db.get_view("Languages")
ext_col.append(view)

for doc in ext_col:
    agent.run(doc)
