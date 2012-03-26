import time

from discovery import DiscoveryServer

d = DiscoveryServer()
d.run()
time.sleep(50)
d.stop()
