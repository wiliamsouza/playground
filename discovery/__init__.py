"""
Multicast DNS service discovery server and client.
"""

import time
import socket

import multiprocessing

from Zeroconf import Zeroconf, ServiceInfo


class DiscoveryServer(object):
    def __init__(self, name='DiscoveryServer'):
        self.zeroconf = Zeroconf()
        self.description = {'version': '0.1', 'auth': 'none'}
        self.service_info = ServiceInfo(
                '_http._tcp.local.',
                'waa._http._tcp.local.',
                socket.inet_aton('127.0.0.1'),
                1234,
                0,
                0,
                self.description)

    def run(self):
        self.zeroconf.registerService(self.service_info)

    def stop(self):
        self.zeroconf.close()


class DiscoveryClient(multiprocessing.Process):
    def __init__(self, name='DiscoveryClient'):
        super(DiscoveryClient, self).__init__(name=name)
        self.event = multiprocessing.Event()
        self.zeroconf = Zeroconf()

    def run(self):
        self.event.set()
        while self.event.is_set():
            service = self.zeroconf.getServiceInfo(
                    '_http._tcp.local.',
                    'waa._http._tcp.local.')
            print service
            time.sleep(1)

    def stop(self):
        self.event.clear()
        self.zeroconf.close()
        self.terminate()
