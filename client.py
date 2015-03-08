import socket
import pickle
import time
from message import Message

class MessageClient:
    """ A client to send messages and measure RTT of messages. """
    def __init__(self, server_address, **options):
        """ Initializes the socket and client parameters.
        Constructor accepts a server address and options (timeout=int, port=int, probe_number=int) """
        # Initialize the client parameters
        self.server_address = server_address
        self.timeout = options['timeout'] if options.get('timeout') else 2
        self.port = options['port'] if options.get('port') else 31337
        self.probe_number = options['probe_number'] if options.get('probe_number') else 10
        # Initialize the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)

    def __del__(self):
        self.sock.close

    def wait_for_acknowledgement(self, sequence_number):
        """ Waits for the acknowledgement message of appropriate sequence number.
        Accepts an integer sequence number and returns whether message was acknowledged in time and RTT for message."""
        start_time = time.time()  # start timer
        try:
            data, addr = self.sock.recvfrom(1024)  # listen for ack from server
            received_sequence_number = data.decode("utf-8")
            if int(received_sequence_number) == sequence_number:
                return True, (time.time() - start_time)  # return true and RTT
        except Exception:
            print("Request timed out/incoming message corrupt")  # If try failed, either timeout or garbage received
            return False, (time.time() - start_time)

    def send_message(self, message):
        """ Sends a message to the server.  Accepts a message object and returns RTT of message. """
        while not message.acknowledged:
            self.sock.sendto(pickle.dumps(message), (self.server_address, self.port))  # send message
            message.acknowledged, RTT = self.wait_for_acknowledgement(message.sequence_number)  # wait for ack
        return RTT  # once message is acknowledged, return RTT of message

    def create_and_send_message(self, sequence_number):
        """ Accepts a sequence number integer and returns RTT for message sent."""
        message = Message(sequence_number)  # create a message object with appropriate sequence number
        RTT = self.send_message(message)  # send message
        print("Packet", sequence_number, "RTT:", RTT, "seconds")
        return RTT

    def measure_RTT(self):
        """ Creates and sends a sequence of messages and returns the average RTTs of those messages. """
        # send a sequence of messages and measure RTTs for each
        print("\nMeasuring Average RTT to", self.server_address)
        RTT_Array = [self.create_and_send_message(sequence_number) for sequence_number in range(0, self.probe_number)]
        average_RTT = sum(RTT_Array)/len(RTT_Array)  # calculate average RTT
        print("\nAverage RTT between local and", self.server_address, ":", average_RTT, "\n")
        return average_RTT