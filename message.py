class Message:
    """Message class to send between client and server"""
    def __init__(self, sequence_number):
        self.sequence_number = sequence_number