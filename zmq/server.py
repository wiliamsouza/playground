import sys

from PySide import QtCore
from PySide import QtGui

from controller import Server

if __name__ == '__main__':
    server = Server('127.0.0.1', 65534)
    server.start()
    app = QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())
