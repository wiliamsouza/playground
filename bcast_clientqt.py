import sys

from broadcastQthread import BroadcastClient
from broadcastQthread.signals import teacherSignal

from PySide import QtCore
from PySide import QtGui


@QtCore.Slot(str, str)
def handle_teacher_discovery_event(message, ip):
    print 'New teacher available', message, ip


if __name__ == '__main__':
    teacherSignal.discovered.connect(handle_teacher_discovery_event)
    message = 'bcastserver'
    datagram_size = len(message)
    client = BroadcastClient(65535, datagram_size)
    client.start()
    app = QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())
