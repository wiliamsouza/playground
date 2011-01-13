import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

class UnitWrapper(QtCore.QObject):
    def __init__(self, unit):
        QtCore.QObject.__init__(self)
        self._unit = unit

    def _id(self):
        return str(self._unit.properties.Id)

    def _description(self):
        return str(self._unit.properties.Description)

    changed = QtCore.Signal()

    id = QtCore.Property(unicode, _id, notify=changed)
    description = QtCore.Property(unicode, _description, notify=changed)

class UnitListModel(QtCore.QAbstractListModel):
    COLUMNS = ('unit',)

    def __init__(self, unit):
        QtCore.QAbstractListModel.__init__(self)
        self._unit = unit
        self.setRoleNames(dict(enumerate(UnitListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._unit)

    def data(self, index, role):
        if index.isValid() and role == UnitListModel.COLUMNS.index('unit'):
            return self._unit[index.row()]
        return None

class UnitController(QtCore.QObject):
    @QtCore.Slot(QtCore.QObject)
    def unit_selected(self, unit_wrapper):
        print 'User clicked on:', unit_wrapper._unit.properties.Id

app = QtGui.QApplication(sys.argv)

m = QtGui.QMainWindow()

view = QtDeclarative.QDeclarativeView()
glw = QtGui.QWidget()
view.setViewport(glw)
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

from systemd.manager import Manager

manager = Manager()

units = []
for unit in manager.list_units():
    if not unit.properties.Id.endswith('.service'):
         continue
    units.append(UnitWrapper(unit))

unit_controller = UnitController()
unit_list_model = UnitListModel(units)

rc = view.rootContext()

rc.setContextProperty('unit_controller', unit_controller)
rc.setContextProperty('unit_list_model', unit_list_model)

view.setSource('UnitList.qml')

m.setCentralWidget(view)

m.show()

app.exec_()