import time
import socket
import logging

import multiprocessing
from multiprocessing import Process, Event

from broadcast.signals import teacher_discovered

class BroadcastServer(Process):

    def __init__(self, ip, port, message, name='BroadcastServer'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.message = message
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', 0))

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)
        while self.event.is_set():
            self.logger.debug('Sending: %s' % self.message)
            self.sock.sendto(self.message, (self.ip, self.port))
            time.sleep(1)

    def stop(self):
        self.logger.debug('Server will halt.')
        self.event.clear()
        self.terminate()


class BroadcastClient(Process):

    def __init__(self, port, datagram_size, name='BroadcastClient'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.port = port
        self.datagram_size = datagram_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind(('', self.port))

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)
        while self.event.is_set():
            try:
                message, (ip, port) = self.sock.recvfrom(self.datagram_size)
                teacher_discovered.send(sender=self)
                self.logger.debug('Received: %s from: %s' % (message, ip))
            except socket.timeout:
                self.logger.debug('%s timeout' % multiprocessing.current_process().name)
            time.sleep(1)

    def stop(self):
        self.logger.debug('Client will halt.')
        self.event.clear()
        self.sock.close()
        self.terminate()
