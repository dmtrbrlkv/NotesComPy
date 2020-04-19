from notescompy import init_session, open_database
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
doc = db.get_document_by_unid("9A899214038E229843258541003BFFDB")

print(doc.get_item_value("Form"))
print(doc.GetItemValue("Level"))
print(doc.get_item_value("Level")[0])
print(doc.get_item_value0("Level"))

lang_doc = db.create_document()
lang_doc.replace_item_value("Form", "Language")
lang_doc.replace_item_value("Name", "Go")
lang_doc.replace_item_value("Description", "Go is an open source programming language that makes it easy to build simple, reliable, and efficient software")
lang_doc.compute_with_form()
# lang_doc.save()

values = lang_doc.get_values(["Form", "Name"], "Universalid", "@created", "Дата создания")
print(values)
values = lang_doc.get_values(["Form", "Name"], "Universalid", "@created", "Дата создания", no_list=True)
print(values)