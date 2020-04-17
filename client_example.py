from notescompy import init_session, open_database, session, extended_collection, log

def update_person(doc):
    logdb = open_database('PyLN', 'dblog.nsf')
    l = log.notes_log(logdb, "Python log", log.LogLevel.INFO)

    unid = doc.get_item_value0("unid")

    l.info(f"Актуализация для справочника {unid}")
    db = doc.parent_database
    col = extended_collection.ExtendedCollection()

    if doc.get_item_value0("Form") == "Language":
        view = db.get_view("srchPersonsByLanguage")
        field_name = "Languages"
        field_unid_name = "LanguagesUNID"
        new_value = doc.get_item_value0("Name")
    elif doc.get_item_value0("Form") == "Level":
        view = db.get_view("srchPersonsByLevel")
        field_name = "Level"
        field_unid_name = "LevelUNID"
        new_value = doc.get_item_value0("Level")
    else:
        return

    for person_doc in view.get_all_documents_by_key(unid):
        field_value = []

        for field_v, field_unid in person_doc.get_values_t(field_name, field_unid_name):
            if field_unid == unid:
                field_value.append(new_value)
            else:
                field_value.append(field_v)

        if field_value != person_doc.get_item_value(field_name):
            person_doc.replace_item_value(field_name, field_value)
            col.append(person_doc)

    col.save()

    l.info(f"Изменено {col.count} документов")


s = init_session(session_type=session.SessionType.NotesNotesSession)
unid = s.notes_property.GetEnvironmentString("LN_UNID")
path = s.notes_property.GetEnvironmentString("LN_FILEPATH")
server = s.notes_property.GetEnvironmentString("LN_SERVER")

db = open_database(server, path)
doc = db.get_document_by_unid(unid)

update_person(doc)

input("Готово")