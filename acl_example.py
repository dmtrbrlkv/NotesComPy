from notescompy import init_session, open_database
from notescompy.acl import UserType, ACLRights, ACLLevel


s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
acl = db.acl

print(acl.roles)
acl.AddRole("TEST")
acl.Save()

for entry in acl:
    print(entry)

entry = acl.create_acl_entry("Test")
entry.user_type = UserType.PERSON
entry.level = ACLLevel.EDITOR
rights = ACLRights()
rights.can_replicate_or_copy_documents = True
rights.can_delete_documents = True
entry.rights = rights
acl.save()

entry = acl.CreateACLEntry("Devs")
entry.user_type = UserType.PERSON_GROUP
entry.level = ACLLevel.DESIGNER
entry.roles = acl.roles
entry.rights = ACLRights(can_create_ls_or_java_agent=True, can_replicate_or_copy_documents=True)
acl.save()

acl.remove_acl_entry("Test")
acl.rename_role("TEST", "BOSS")
entry = acl.get_entry("Python/PyLN")
roles = entry.roles
roles.append("BOSS")
entry.roles = roles
acl.save()