from . import handle, utils, iterdoc
import enum

class ACLLevel(enum.IntEnum):
    ACLLEVEL_NOACCESS = 0
    ACLLEVEL_DEPOSITOR = 1
    ACLLEVEL_READER = 2
    ACLLEVEL_AUTHOR = 3
    ACLLEVEL_EDITOR = 4
    ACLLEVEL_DESIGNER = 5
    ACLLEVEL_MANAGER = 6

    def __str__(self):
        if self == ACLLevel.ACLLEVEL_NOACCESS:
            return "No access"
        if self == ACLLevel.ACLLEVEL_DEPOSITOR:
            return "Depositor"
        if self == ACLLevel.ACLLEVEL_READER:
            return "Reader"
        if self == ACLLevel.ACLLEVEL_AUTHOR:
            return "Author"
        if self == ACLLevel.ACLLEVEL_EDITOR:
            return "Editor"
        if self == ACLLevel.ACLLEVEL_DESIGNER:
            return "Designer"
        if self == ACLLevel.ACLLEVEL_MANAGER:
            return "Manager"


class UserType(enum.IntEnum):
    ACLTYPE_UNSPECIFIED = 0
    ACLTYPE_PERSON = 1
    ACLTYPE_SERVER =2
    ACLTYPE_MIXED_GROUP = 3
    ACLTYPE_PERSON_GROUP = 4
    ACLTYPE_SERVER_GROUP = 5

    def __str__(self):
        if self == UserType.ACLTYPE_UNSPECIFIED:
            return "Unspecified"
        if self == UserType.ACLTYPE_PERSON:
            return "Person"
        if self == UserType.ACLTYPE_SERVER:
            return "Server"
        if self == UserType.ACLTYPE_MIXED_GROUP:
            return "Mixed group"
        if self == UserType.ACLTYPE_PERSON_GROUP:
            return "Person group"
        if self == UserType.ACLTYPE_SERVER_GROUP:
            return "Server group"

class ACLRights():
    def __init__(self, CanCreateDocuments=False, CanCreateLSOrJavaAgent=False, CanCreatePersonalAgent=False, CanCreatePersonalFolder=False,
                 CanCreateSharedFolder=False, CanDeleteDocuments=False, CanReplicateOrCopyDocuments=False, IsPublicReader=False, IsPublicWriter=False):
        self.CanCreateDocuments = CanCreateDocuments
        self.CanCreateLSOrJavaAgent = CanCreateLSOrJavaAgent
        self.CanCreatePersonalAgent = CanCreatePersonalAgent
        self.CanCreatePersonalFolder = CanCreatePersonalFolder
        self.CanCreateSharedFolder = CanCreateSharedFolder
        self.CanDeleteDocuments = CanDeleteDocuments
        self.CanReplicateOrCopyDocuments = CanReplicateOrCopyDocuments
        self.IsPublicReader = IsPublicReader
        self.IsPublicWriter = IsPublicWriter

    @property
    def CanCreateDocuments(self):
        return self._CanCreateDocuments
    @CanCreateDocuments.setter
    def CanCreateDocuments(self, value):
        self._CanCreateDocuments = value

    @property
    def CanCreateLSOrJavaAgent(self):
        return self._CanCreateLSOrJavaAgent
    @CanCreateLSOrJavaAgent.setter
    def CanCreateLSOrJavaAgent(self, value):
        self._CanCreateLSOrJavaAgent = value

    @property
    def CanCreatePersonalAgent(self):
        return self._CanCreatePersonalAgent
    @CanCreatePersonalAgent.setter
    def CanCreatePersonalAgent(self, value):
        self._CanCreatePersonalAgent = value

    @property
    def CanCreatePersonalFolder(self):
        return self._CanCreatePersonalFolder
    @CanCreatePersonalFolder.setter
    def CanCreatePersonalFolder(self, value):
        self._CanCreatePersonalFolder = value

    @property
    def CanCreateSharedFolder(self):
        return self._CanCreateSharedFolder
    @CanCreateSharedFolder.setter
    def CanCreateSharedFolder(self, value):
        self._CanCreateSharedFolder = value

    @property
    def CanDeleteDocuments(self):
        return self._CanDeleteDocuments
    @CanDeleteDocuments.setter
    def CanDeleteDocuments(self, value):
        self._CanDeleteDocuments = value

    @property
    def CanReplicateOrCopyDocuments(self):
        return self._CanReplicateOrCopyDocuments
    @CanReplicateOrCopyDocuments.setter
    def CanReplicateOrCopyDocuments(self, value):
        self._CanReplicateOrCopyDocuments = value

    @property
    def IsPublicReader(self):
        return self._IsPublicReader
    @IsPublicReader.setter
    def IsPublicReader(self, value):
        self._IsPublicReader = value

    @property
    def IsPublicWriter(self):
        return self._IsPublicWriter
    @IsPublicWriter.setter
    def IsPublicWriter(self, value):
        self._IsPublicWriter = value

    def __str__(self):
        res = []

        if self.CanCreateDocuments:
            res.append("Create documents")
        if self.CanCreateLSOrJavaAgent:
            res.append("Create LotusScript/Java agents")
        if self.CanCreatePersonalAgent:
            res.append("Create private agents")
        if self.CanCreatePersonalFolder:
            res.append("Create personal folders/views")
        if self.CanCreateSharedFolder:
            res.append("Create shares folders/views")
        if self.CanDeleteDocuments:
            res.append("Delete documents")
        if self.CanReplicateOrCopyDocuments:
            res.append("Replicate or copy documents")
        if self.IsPublicReader:
            res.append("Read public documents")
        if self.IsPublicWriter:
            res.append("Write public documents")

        return ", ".join(res)


class ACLEntry(handle.NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)

    @property
    def Name(self):
        return self.handle.Name

    @Name.setter
    def Name(self, value):
        self.handle.Name = value


    @property
    def Roles(self):
        return self.handle.Roles

    @Roles.setter
    def Roles(self, roles):
        if roles is None:
            for role in self.Roles:
                self.handle.DisableRole(role)
            return

        if isinstance(roles, str):
            roles = [roles]

        for role in self.Roles:
            self.handle.DisableRole(role)
        
        for role in roles:
            self.handle.EnableRole(role)


    @property
    def UserType(self):
        return UserType(self.handle.UserType)
    @UserType.setter
    def UserType(self, value):
        if isinstance(value, UserType):
            self.handle.UserType = value.value
        else:
            self.handle.UserType = value

    @property
    def Level(self):
        return ACLLevel(self.handle.Level)
    @Level.setter
    def Level(self, value):
        if isinstance(value, ACLLevel):
            self.handle.Level = value.value
        else:
            self.handle.Level = value

    @property
    def Rights(self):
        rights = ACLRights()
        if self.handle.CanCreateDocuments:
            rights.CanCreateDocuments = True

        if self.handle.CanCreateLSOrJavaAgent:
            rights.CanCreateLSOrJavaAgent = True

        if self.handle.CanCreatePersonalAgent:
            rights.CanCreatePersonalAgent = True

        if self.handle.CanCreatePersonalFolder:
            rights.CanCreatePersonalFolder = True

        if self.handle.CanCreateSharedFolder:
            rights.CanCreateSharedFolder = True

        if self.handle.CanDeleteDocuments:
            rights.CanDeleteDocuments = True

        if self.handle.CanReplicateOrCopyDocuments:
            rights.CanReplicateOrCopyDocuments = True

        if self.handle.IsPublicReader:
            rights.IsPublicReader = True

        if self.handle.IsPublicWriter:
            rights.IsPublicWriter = True

        return rights

    @Rights.setter
    def Rights(self, rights):
        if rights is None:
            rights = ACLRights()

        self.handle.CanCreateDocuments = rights.CanCreateDocuments
        self.handle.CanCreateLSOrJavaAgent = rights.CanCreateLSOrJavaAgent
        self.handle.CanCreatePersonalAgent = rights.CanCreatePersonalAgent
        self.handle.CanCreatePersonalFolder = rights.CanCreatePersonalFolder
        self.handle.CanCreateSharedFolder = rights.CanCreateSharedFolder
        self.handle.CanDeleteDocuments = rights.CanDeleteDocuments
        self.handle.CanReplicateOrCopyDocuments = rights.CanReplicateOrCopyDocuments
        self.handle.IsPublicReader = rights.IsPublicReader
        self.handle.IsPublicWriter = rights.IsPublicWriter

    def __str__(self):
        res = []

        res.append(f"Name: {self.Name}")
        res.append(f"User type: {str(self.UserType)}")
        res.append(f"Level: {str(self.Level)}")
        if self.Roles:
            res.append(f"Roles: ({', '.join(self.Roles)})")
        else:
            res.append(f"Roles: -")
        res.append(f"Rights: ({self.Rights})")

        return ", ".join(res)


    def get_values(self, asStr):
        values = {
            "Name": self.Name,
            "UserType": str(self.UserType) if asStr else self.UserType,
            "Level": str(self.Level) if asStr else self.Level,
            "Roles": self.Roles
        }
        return values

    def to_json(self, asStr=False, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, asStr=False, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        utils.save_to_json(values, fp, default, sort_keys, indent)


class ACL(handle.NotesHandle, iterdoc.IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        iterdoc.IterDocMixin.__init__(self, "GetFirstEntry:get_first_entry", "GetNextEntry:get_next_entry", ACLEntry)


    @property
    def Roles(self):
        return self.handle.Roles

    def AddRole(self, name):
        self.handle.AddRole(name)

    def DeleteRole(self, name):
        self.handle.DeleteRole(name)

    def RenameRole(self, old_name, new_name):
        self.handle.RenameRole(old_name, new_name)

    def CreateACLEntry(self, name, level=ACLLevel.ACLLEVEL_NOACCESS, user_type=UserType.ACLTYPE_PERSON, roles=None, rights=None):

        if isinstance(level, ACLLevel):
            entry_handle = self.handle.CreateACLEntry(name, level.value)
        else:
            entry_handle = self.handle.CreateACLEntry(name, level)

        entry = ACLEntry(entry_handle)

        if isinstance(user_type, UserType):
            entry.UserType = user_type.value
        else:
            entry.UserType = user_type

        entry.Roles = roles
        entry.Rights = rights

        return entry


    def RemoveACLEntry(self, name):
        self.handle.RemoveACLEntry(name)


    def Save(self):
        self.handle.Save()


    def get_values(self, asStr=False):
        values = {
            entry.Name: entry.get_values(asStr) for entry in self
        }
        return values

    def to_json(self, asStr=False, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, asStr=False, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        utils.save_to_json(values, fp, default, sort_keys, indent)
