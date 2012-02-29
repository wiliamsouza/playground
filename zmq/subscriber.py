import zmq

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect('epgm://192.168.1.2;239.192.0.1:5000')
subscriber.setsockopt(zmq.SUBSCRIBE, '')

file_path = 'C:\\Users\\waa\\Desktop\\Firefox Setup 10.0.1.exe'
f = open(file_path, 'wb')

while True:
    data = subscriber.recv()
    if not data:
        break

    f.write(data)

f.close()
