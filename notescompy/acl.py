from . import handle, utils, iterdoc
import enum

class ACLLevel(enum.IntEnum):
    NOACCESS = 0
    DEPOSITOR = 1
    READER = 2
    AUTHOR = 3
    EDITOR = 4
    DESIGNER = 5
    MANAGER = 6

    def __str__(self):
        if self == ACLLevel.NOACCESS:
            return "No access"
        if self == ACLLevel.DEPOSITOR:
            return "Depositor"
        if self == ACLLevel.READER:
            return "Reader"
        if self == ACLLevel.AUTHOR:
            return "Author"
        if self == ACLLevel.EDITOR:
            return "Editor"
        if self == ACLLevel.DESIGNER:
            return "Designer"
        if self == ACLLevel.MANAGER:
            return "Manager"


class UserType(enum.IntEnum):
    UNSPECIFIED = 0
    PERSON = 1
    SERVER =2
    MIXED_GROUP = 3
    PERSON_GROUP = 4
    SERVER_GROUP = 5

    def __str__(self):
        if self == UserType.UNSPECIFIED:
            return "Unspecified"
        if self == UserType.PERSON:
            return "Person"
        if self == UserType.SERVER:
            return "Server"
        if self == UserType.MIXED_GROUP:
            return "Mixed group"
        if self == UserType.PERSON_GROUP:
            return "Person group"
        if self == UserType.SERVER_GROUP:
            return "Server group"

class ACLRights():
    def __init__(self, can_create_documents=False, can_create_ls_or_java_agent=False, can_create_personal_agent=False, can_create_personal_folder=False,
                 can_create_shared_folder=False, can_delete_documents=False, can_replicate_or_copy_documents=False, is_public_reader=False, is_public_writer=False):
        self.can_create_documents = can_create_documents
        self.can_create_ls_or_java_agent = can_create_ls_or_java_agent
        self.can_create_personal_agent = can_create_personal_agent
        self.can_create_personal_folder = can_create_personal_folder
        self.can_create_shared_folder = can_create_shared_folder
        self.can_delete_documents = can_delete_documents
        self.can_replicate_or_copy_documents = can_replicate_or_copy_documents
        self.is_public_reader = is_public_reader
        self.is_public_writer = is_public_writer

    @property
    def can_create_documents(self):
        return self._can_create_documents
    @can_create_documents.setter
    def can_create_documents(self, value):
        self._can_create_documents = value

    @property
    def can_create_ls_or_java_agent(self):
        return self._can_create_ls_or_java_agent
    @can_create_ls_or_java_agent.setter
    def can_create_ls_or_java_agent(self, value):
        self._can_create_ls_or_java_agent = value

    @property
    def can_create_personal_agent(self):
        return self._can_create_personal_agent
    @can_create_personal_agent.setter
    def can_create_personal_agent(self, value):
        self._can_create_personal_agent = value

    @property
    def can_create_personal_folder(self):
        return self._can_create_personal_folder
    @can_create_personal_folder.setter
    def can_create_personal_folder(self, value):
        self._can_create_personal_folder = value

    @property
    def can_create_shared_folder(self):
        return self._can_create_shared_folder
    @can_create_shared_folder.setter
    def can_create_shared_folder(self, value):
        self._can_create_shared_folder = value

    @property
    def can_delete_documents(self):
        return self._can_delete_documents
    @can_delete_documents.setter
    def can_delete_documents(self, value):
        self._can_delete_documents = value

    @property
    def can_replicate_or_copy_documents(self):
        return self._can_replicate_or_copy_documents
    @can_replicate_or_copy_documents.setter
    def can_replicate_or_copy_documents(self, value):
        self._can_replicate_or_copy_documents = value

    @property
    def is_public_reader(self):
        return self._is_public_reader
    @is_public_reader.setter
    def is_public_reader(self, value):
        self._is_public_reader = value

    @property
    def is_public_writer(self):
        return self._is_public_writer
    @is_public_writer.setter
    def is_public_writer(self, value):
        self._is_public_writer = value

    def __str__(self):
        res = []

        if self.can_create_documents:
            res.append("Create documents")
        if self.can_create_ls_or_java_agent:
            res.append("Create LotusScript/Java agents")
        if self.can_create_personal_agent:
            res.append("Create private agents")
        if self.can_create_personal_folder:
            res.append("Create personal folders/views")
        if self.can_create_shared_folder:
            res.append("Create shares folders/views")
        if self.can_delete_documents:
            res.append("Delete documents")
        if self.can_replicate_or_copy_documents:
            res.append("Replicate or copy documents")
        if self.is_public_reader:
            res.append("Read public documents")
        if self.is_public_writer:
            res.append("Write public documents")

        return str(res)


class ACLEntry(handle.NotesHandle):
    def __init__(self, handle):
        super().__init__(handle)

    @property
    def name(self):
        return self.handle.Name

    @name.setter
    def name(self, value):
        self.handle.Name = value
    Name = name

    @property
    def roles(self):
        return list(self.handle.Roles)

    @roles.setter
    def roles(self, roles):
        if roles is None:
            for role in self.roles:
                self.handle.DisableRole(role)
            return

        if isinstance(roles, str):
            roles = [roles]

        for role in self.roles:
            self.handle.DisableRole(role)
        
        for role in roles:
            self.handle.EnableRole(role)
    Roles = roles

    @property
    def user_type(self):
        return UserType(self.handle.UserType)
    @user_type.setter
    def user_type(self, value):
        if isinstance(value, UserType):
            self.handle.UserType = value.value
        else:
            self.handle.UserType = value
    UserType = user_type

    @property
    def level(self):
        return ACLLevel(self.handle.Level)
    @level.setter
    def level(self, value):
        if isinstance(value, ACLLevel):
            self.handle.Level = value.value
        else:
            self.handle.Level = value
    Level = level

    @property
    def rights(self):
        rights = ACLRights()
        if self.handle.CanCreateDocuments:
            rights.can_create_documents = True

        if self.handle.CanCreateLSOrJavaAgent:
            rights.can_create_ls_or_java_agent = True

        if self.handle.CanCreatePersonalAgent:
            rights.can_create_personal_agent = True

        if self.handle.CanCreatePersonalFolder:
            rights.can_create_personal_folder = True

        if self.handle.CanCreateSharedFolder:
            rights.can_create_shared_folder = True

        if self.handle.CanDeleteDocuments:
            rights.can_delete_documents = True

        if self.handle.CanReplicateOrCopyDocuments:
            rights.can_replicate_or_copy_documents = True

        if self.handle.IsPublicReader:
            rights.is_public_reader = True

        if self.handle.IsPublicWriter:
            rights.is_public_writer = True

        return rights

    @rights.setter
    def rights(self, rights):
        if rights is None:
            rights = ACLRights()

        self.handle.CanCreateDocuments = rights.can_create_documents
        self.handle.CanCreateLSOrJavaAgent = rights.can_create_ls_or_java_agent
        self.handle.CanCreatePersonalAgent = rights.can_create_personal_agent
        self.handle.CanCreatePersonalFolder = rights.can_create_personal_folder
        self.handle.CanCreateSharedFolder = rights.can_create_shared_folder
        self.handle.CanDeleteDocuments = rights.can_delete_documents
        self.handle.CanReplicateOrCopyDocuments = rights.can_replicate_or_copy_documents
        self.handle.IsPublicReader = rights.is_public_reader
        self.handle.IsPublicWriter = rights.is_public_writer

    def __str__(self):
        res = []

        res.append(f"Name: {self.name}")
        res.append(f"User type: {str(self.user_type)}")
        res.append(f"Level: {str(self.level)}")
        if self.roles:
            res.append(f"Roles: ({', '.join(self.roles)})")
        else:
            res.append(f"Roles: -")
        res.append(f"Rights: ({self.rights})")

        return ", ".join(res)

    def get_values(self, asStr):
        values = {
            "Name": self.name,
            "UserType": str(self.user_type) if asStr else self.user_type,
            "Level": str(self.level) if asStr else self.level,
            "Roles": self.roles,
            "Rights": self.rights,
        }
        return values

    def to_json(self, asStr=True, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, asStr=True, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        utils.save_to_json(values, fp, default, sort_keys, indent)


class ACL(handle.NotesHandle, iterdoc.IterDocMixin):
    def __init__(self, handle):
        super().__init__(handle)
        iterdoc.IterDocMixin.__init__(self, "GetFirstEntry:get_first_entry", "GetNextEntry:get_next_entry", ACLEntry)


    @property
    def roles(self):
        return self.handle.Roles
    Roles = roles

    def add_role(self, name):
        self.handle.AddRole(name)
    AddRole =add_role

    def delete_role(self, name):
        self.handle.DeleteRole(name)
    DeleteRole = delete_role

    def rename_role(self, old_name, new_name):
        self.handle.RenameRole(old_name, new_name)
    RenameRole = rename_role

    def create_acl_entry(self, name, level=ACLLevel.NOACCESS, user_type=UserType.PERSON, roles=None, rights=None):
        if isinstance(level, ACLLevel):
            entry_handle = self.handle.CreateACLEntry(name, level.value)
        else:
            entry_handle = self.handle.CreateACLEntry(name, level)

        entry = ACLEntry(entry_handle)

        if isinstance(user_type, UserType):
            entry.user_type = user_type.value
        else:
            entry.user_type = user_type

        entry.roles = roles
        entry.rights = rights

        return entry
    CreateACLEntry = create_acl_entry

    def remove_acl_entry(self, name):
        self.handle.RemoveACLEntry(name)
    RemoveACLEntry = remove_acl_entry

    def get_entry(self, name):
        entry_handle = self.handle.GetEntry(name)
        return ACLEntry(entry_handle)

    def save(self):
        self.handle.Save()
    Save = save

    def get_values(self, asStr=True):
        values = {
            entry.name: entry.get_values(asStr) for entry in self
        }
        return values

    def to_json(self, asStr=True, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, asStr=True, default=str, sort_keys=True, indent=4):
        values = self.get_values(asStr)
        utils.save_to_json(values, fp, default, sort_keys, indent)
