import os
import time
import hashlib

import zmq

context = zmq.Context()
publisher = context.socket(zmq.PUB)
# Setting rate limit to 1Mbps
#publisher.setsockopt(zmq.RATE, 1000)
publisher.bind('epgm://192.168.1.2;239.192.0.1:5000')

import os
time.sleep(5)

file_path = 'C:\Users\waa\Downloads\Firefox Setup 10.0.1.exe'
file_size = os.path.getsize(file_path)
with open(file_path, 'rb') as f:
    md5 = hashlib.md5()

    total = 0
    while True:
        data = f.read(1436)
        md5.update(data)
        publisher.send(data)
        total += 1436
        if not data:
            break

    import os
    import
    import
