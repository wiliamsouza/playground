import zmq

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect('epgm://192.168.1.2;239.192.0.1:5000')
subscriber.setsockopt(zmq.SUBSCRIBE, '')

file_path = 'C:\\Users\\waa\\Desktop\\Firefox Setup 10.0.1.exe'
with open(file_path, 'wb') as f:
    while True:
        if data := subscriber.recv():
            f.write(data)

        else:
            break
