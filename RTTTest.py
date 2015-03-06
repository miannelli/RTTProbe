class Server():
    def __init__(self, hostname, port=31337):
        self.hostname = hostname
        self.port = port

    def test_RTT(self):
        import client
        client.port = self.port
        client.server_address = self.hostname
        self.RTT = client.start()
        return self.RTT

servers = []

RTTS = [[server.hostname, server.test_RTT] for server in servers]
