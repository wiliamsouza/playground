import time
import socket
import logging

import multiprocessing
from multiprocessing import Process, Event

class BroadcastServer(Process):

    def __init__(self, ip, port, name='BroadcastServer'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.message = 'bcastserv'
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', 0))

    def run(self):
        self.event.set()
        self.logger.info('PID: %d' % multiprocessing.current_process().pid)
        while self.event.is_set():
            self.logger.info('Sending: %s' % self.message)
            self.sock.sendto(self.message, (self.ip, self.port))
            time.sleep(1)

    def stop(self):
        self.logger.info('Server will halt.')
        self.event.clear()
        self.terminate()


class BroadcastClient(Process):

    def __init__(self, port, name='BroadcastClient'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))

    def run(self):
        self.event.set()
        self.logger.info('PID: %d' % multiprocessing.current_process().pid)
        while self.event.is_set():
            message, (ip, port) = self.sock.recvfrom(30)
            self.logger.info('Received: %s from: %s' % (message, ip))
            time.sleep(1)

    def stop(self):
        self.logger.info('Client will halt.')
        self.event.clear()
        self.terminate()


if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    server = BroadcastServer('255.255.255.255', 65535)
    client = BroadcastClient(65535)
    server.start()
    client.start()

    time.sleep(6)

    server.stop()
    client.stop()
    server.join()
    client.join()
