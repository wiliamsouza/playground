from PySide import QtCore, QtGui, QtDeclarative

from models import Group, GroupListModel

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    groupListModel = GroupListModel(Group.populate())
    context = view.rootContext()
    context.setContextProperty('groupListModel', groupListModel)
    view.setSource('groups.qml')
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.setWindowTitle('Groups')
    view.show()
    app.exec_()