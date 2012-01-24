import os
import time
import hashlib

import zmq

context = zmq.Context()
publisher = context.socket(zmq.PUB)
# Setting rate limit to 1Mbps
publisher.setsockopt(zmq.RATE, 1000)
publisher.bind('pgm://192.168.1.4:5000')

print 'Waiting for connections'
time.sleep(5)

file_path = '/home/wiliam/foo.pdf'
file_size = os.path.getsize(file_path)
f = open(file_path, 'rb')

md5 = hashlib.md5()

total = 0
while True:
    data = f.read(1436)
    md5.update(data)
    publisher.send(data)
    if not data:
        break
    total += 1436

print 'Total bytes sent:', total
print 'File size bytes:', file_size
print 'md5 checksum:', md5.hexdigest()
f.close()
