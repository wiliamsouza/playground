import logging

import multiprocessing

from pydispatch import dispatcher

from broadcast import BroadcastClient
from broadcast.signals import teacher_discovered

def handle_teacher_discovery_event(sender):
    print 'New teacher available'
    print 'Signal sent by ', sender

dispatcher.connect(handle_teacher_discovery_event, signal=teacher_discovered, sender=dispatcher.Any)

if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.INFO)
    message = 'bcastserver'
    datagram_size = len(message)
    client = BroadcastClient(65535, datagram_size)
    client.start()
    client.join()
