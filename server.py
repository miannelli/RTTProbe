import socket
import pickle
# import random  # used to simulate packet loss and transmission delay
# import time  # used to simulate transmission delay

address = "127.0.0.1"
port = 31337
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_acknowledgement(client, sequence_number):
    """ Sends acknowledment to client.  Accepts integer sequence number, no return value. """
    addr, port = client
    sock.sendto(bytes(str(sequence_number), 'utf-8'), (addr, port))

def listen():
    """ Listens for messages from clients. """
    print('Listening on port', port)
    while True:
        data, client = sock.recvfrom(1024)  # Receive message from client
        try:
            message = pickle.loads(data)  # unpack message
            print("received message", message.sequence_number)
            # time.sleep(random.random())  # used to simulate transmission delay
            # if random.random() > 0.5:  # used to simulate packet loss
            send_acknowledgement(client, message.sequence_number)  # send ack for message sequence number
        except:
            print("Incoming Message Corrupt")  # if garbage received

def start():
    """ Starts the server. """
    server_state = False
    try:
        sock.bind((address, port))
        server_state = True
    except:
        print("Failed to start server")  # Server may fail to start if port in use
    if server_state:
        listen()

start()