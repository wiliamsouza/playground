import time
import socket
import logging

import multiprocessing
from multiprocessing import Process

class BroadcastServer(Process):

    def __init__(self, ip, port, name='BroadcastServer'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.message = 'bcastserv'
        self._running = True
        self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(('', 0))

    def run(self):
        self.logger.info('PID: %d' % multiprocessing.current_process().pid)
        while self._running:
            self.logger.debug('Running: %s' % self._running)
            self.logger.info('Sending: %s' % self.message)
            self._sock.sendto(self.message, (self._ip, self._port))
            time.sleep(1)

    def halt(self):
        self.logger.info('Server will halt.')
        self._running = False


class BroadcastClient(Process):

    def __init__(self, port, name='BroadcastClient'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self._running = True
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(('', self._port))

    def run(self):
        self.logger.info('PID: %d' % multiprocessing.current_process().pid)
        while self._running:
            message, (ip, port) = self._sock.recvfrom(30)
            self.logger.info('Received: %s from: %s' % (message, ip))
            time.sleep(1)

    def halt(self):
        self.logger.info('Client will halt.')
        self._running = False


if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    server = BroadcastServer('255.255.255.255', 65535)
    client = BroadcastClient(65535)
    server.start()
    client.start()
    time.sleep(6)
    server.halt()
    client.halt()
    server.join()
    client.join()
