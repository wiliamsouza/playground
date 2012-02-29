import time
import logging
import multiprocessing

from broadcast import BroadcastServer

if __name__ == '__main__':
    time.sleep(2)
    multiprocessing.log_to_stderr(logging.DEBUG)
    message = 'bcastserver'
    datagram_size = len(message)
    server = BroadcastServer('255.255.255.255', 65535, message)
    server.start()
    time.sleep(6)
    server.stop()
    server.join()

