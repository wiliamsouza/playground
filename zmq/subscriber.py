import zmq

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect('pgm://192.168.1.4:5000')
subscriber.setsockopt(zmq.SUBSCRIBE, '')

file_path = '/home/wiliam/foo_downloaded.pdf'
f = open(file_path, 'wb')

while True:
    data = subscriber.recv()
    f.write(data)
    if not data:
        break

f.close()
