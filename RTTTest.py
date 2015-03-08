from client import MessageClient

class Server():
    """ Class for a server running message server script """
    def __init__(self, hostname):
        self.hostname = hostname

    def test_RTT(self):
        """ Measures average RTT for 10 messages """
        client = MessageClient(self.hostname)
        self.RTT = client.measure_RTT()
        return self.RTT

# Servers to test RTT to
server_hostnames = ['planet1.pnl.nitech.ac.jp',
                    'planetlab2.arizona-gigapop.net']

# Measure RTTs
RTTS = [Server(hostname).test_RTT() for hostname in server_hostnames]

# Print RTT to each server
print("\nAverage RTTs:")
for server, RTT in zip(server_hostnames, RTTS):
    print(server, RTT)