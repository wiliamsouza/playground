import logging

import multiprocessing

from broadcast import BroadcastClient
from broadcast.signals import teacher_discovered

def handle_teacher_discovery_event(signal, sender):
    print 'New teacher available'
    print 'Signal sent by ', sender

teacher_discovered.connect(handle_teacher_discovery_event)

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.INFO)
    message = 'bcastserver'
    datagram_size = len(message)
    client = BroadcastClient(65535, datagram_size)
    client.start()
    client.join()
