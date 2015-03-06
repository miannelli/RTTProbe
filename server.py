import socket
import pickle
# import random  # used to simulate packet loss and transmission delay
# import time  # used to simulate transmission delay

address = "127.0.0.1"
port = 31337
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_acknowledgement(client, sequence_number):
    addr, port = client
    sock.sendto(bytes(str(sequence_number), 'utf-8'), (addr, port))

def listen():
    print('Listening on port', port)
    while True:
        data, client = sock.recvfrom(1024)
        try:
            message = pickle.loads(data)
            print("received message", message.sequence_number)
            # time.sleep(random.random())  # used to simulate transmission delay
            # if random.random() > 0.5:  # used to simulate packet loss
            send_acknowledgement(client, message.sequence_number)
        except:
            print("Incoming Message Corrupt")
            print(data)
            m = pickle.loads(data)
            print(m.sequence_number)

def start():
    server_state = False
    try:
        sock.bind((address, port))
        server_state = True
    except:
        print("Failed to start server")
    if server_state:
        listen()

start()