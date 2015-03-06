import socket
import pickle
import time
from message import Message

probe_number = 10
timeout = 2

client_address = "127.0.0.1"
server_address = "192.168.1.8"

port = 31337

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((client_address, port))
sock.settimeout(timeout)

def wait_for_acknowledgement(sequence_number):
    start_time = time.time()
    try:
        data, addr = sock.recvfrom(1024)
        received_sequence_number = data.decode("utf-8")
        if int(received_sequence_number) == sequence_number:
            return True, (time.time() - start_time)
    except Exception:
        print("Request timed out")
        return False, (time.time() - start_time)


def send_message():
    message_acknowledged = False
    RTT = 0
    while not message_acknowledged:
        sock.sendto(pickle.dumps(message), (server_address, port))
        message_acknowledged, RTT = wait_for_acknowledgement(message.sequence_number)
    return RTT

RTT_Array = []

for sequence_number in range(0, probe_number):
    message = Message(sequence_number)
    RTT = send_message()
    print("Packet", sequence_number, "RTT:", RTT, "seconds")
    RTT_Array.append(RTT)

average_RTT = sum(RTT_Array)/len(RTT_Array)
print("\nAverage RTT between local and", server_address, ":", average_RTT)

