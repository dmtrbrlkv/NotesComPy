import os
from notescompy import init_session, open_database


s = init_session("python")
print(s.UserName)

db = open_database('PyLN', 'itcrowd.nsf')

acl = db.acl

for entry in acl:
    print(entry.to_json())
    print(entry.to_json(True))

# acl.AddRole("TEST")
# acl.Save()

# entry = acl.CreateACLEntry("Test")
# entry.UserType = ACL.UserType.ACLTYPE_PERSON
# entry.Level = ACL.ACLLevel.ACLLEVEL_EDITOR
# rights = ACL.ACLRights()
# rights.CanReplicateOrCopyDocuments = True
# rights.CanDeleteDocuments = True
# rights.IsPublicWriter = False
# entry.Rights = rights



# entry = acl.CreateACLEntry("Devs")
# entry.UserType = ACL.UserType.ACLTYPE_PERSON_GROUP
# entry.Level = ACL.ACLLevel.ACLLEVEL_DESIGNER
# entry.Roles = acl.Roles
# entry.Rights = ACL.ACLRights(CanReplicateOrCopyDocuments=True)
#
# acl.Save()


# acl.RemoveACLEntry("Test")
# acl.Save()

# acl.RenameRole("TEST", "newtest")
# acl.Save()


print(acl.to_json())
print(acl.to_json(True))