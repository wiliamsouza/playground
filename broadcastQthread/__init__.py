import time
import socket
import logging

from PySide import QtCore

from broadcastQthread.signals import teacherSignal

class BroadcastServer(QtCore.QThread):

    def __init__(self, ip, port, message, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message = message
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', 0))

    def run(self):
        print 'starting server'
        while True:
            print 'sending', self.message
            self.sock.sendto(self.message, (self.ip, self.port))
            time.sleep(1)

    def stop(self):
        pass


class BroadcastClient(QtCore.QThread):

    def __init__(self, port, datagram_size, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.port = port
        self.datagram_size = datagram_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind(('', self.port))

    def run(self):
        print 'starting client'
        while True:
            try:
                message, (ip, port) = self.sock.recvfrom(self.datagram_size)
                teacherSignal.discovered.emit(message, ip)
                print 'receiving', message
            except socket.timeout:
                print 'timeout'
            time.sleep(1)

    def stop(self):
        pass
