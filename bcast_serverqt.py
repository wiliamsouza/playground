import sys
import time

from broadcastQthread import BroadcastServer

from PySide.QtGui import QApplication

if __name__ == '__main__':
    time.sleep(2)
    message = 'bcastserver'
    datagram_size = len(message)
    server = BroadcastServer('255.255.255.255', 65535, message)
    server.start()
    app = QApplication(sys.argv)
    sys.exit(app.exec_())

