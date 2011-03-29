import dbus
from PySide import QtCore

# This is local copy from what is returned by a dbus interface
GROUPS = [
    dbus.Dictionary({
        dbus.String(u'groupName'): dbus.String(u'wiliam', variant_level=1),
        dbus.String(u'gid'): dbus.Int64(1000L, variant_level=1),
        dbus.String(u'members'): dbus.Array([dbus.String(u'wiliam')],
        signature=dbus.Signature('s'), variant_level=1)},
        signature=dbus.Signature('sv')),
    dbus.Dictionary(
        {dbus.String(u'groupName'): dbus.String(u'paula', variant_level=1),
         dbus.String(u'gid'): dbus.Int64(500L, variant_level=1),
         dbus.String(u'members'): dbus.Array([dbus.String(u'paula')],
         signature=dbus.Signature('s'), variant_level=1)},
         signature=dbus.Signature('sv')) 
        ]

class GroupListModel(QtCore.QAbstractListModel):
    COLUMNS = ('group',)
    def __init__(self, groups):
        QtCore.QAbstractListModel.__init__(self)
        self.__groups = groups
        self.setRoleNames(dict(enumerate(GroupListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__groups)

    def data(self, index, role):
        if index.isValid() and role == GroupListModel.COLUMNS.index('group'):
            return self.__groups[index.row()]
        return None

class Group(QtCore.QObject):

    def __init__(self, groupDetails):
        QtCore.QObject.__init__(self)
        self.__groupDetails = groupDetails

    def __getGid(self):
        return str(self.__groupDetails['gid'])

    def __getGroupName(self):
        return str(self.__groupDetails['groupName'])

    def __getMembers(self):
        return self.__groupDetails['members']

    @classmethod
    def populate(cls):
        groups = []
        for group in GROUPS:
            groups.append(cls(group))
        return groups

    changed = QtCore.Signal()
    gid = QtCore.Property(unicode, __getGid, notify=changed)
    groupname = QtCore.Property(unicode, __getGroupName, notify=changed)
    members = QtCore.Property(list, __getMembers, notify=changed)