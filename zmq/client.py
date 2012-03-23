import sys

from PySide import QtCore
from PySide import QtGui

from controller import Client

if __name__ == '__main__':
    client = Client('127.0.0.1', 65534)
    client.start()
    app = QtGui.QApplication(sys.argv)
    client.send('Student connected')
    sys.exit(app.exec_())
