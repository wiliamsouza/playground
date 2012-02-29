from PySide import QtCore

class TeacherSignal(QtCore.QObject):
    discovered = QtCore.Signal(str, str)

teacherSignal = TeacherSignal()
