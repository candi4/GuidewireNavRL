import sys
import xmlrpc.client


# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# os.path.dirname(os.path.abspath(__file__)) + '/SimClient.py'
from scene import SOFA#, SaveImage

class Client():
    def __init__(self):
        self.port_rpc = None
    def connect(self, port_rpc):
        self.port_rpc = port_rpc
        # Register the instance to the manager
        self.server = xmlrpc.client.ServerProxy('http://localhost:' + port_rpc)
        print("Connected")
    def dataput(self, item):
        # Send data to the server.
        return self.server.clientput(item)
    def dataget(self):
        # Get data from the server.
        return self.server.serverget()


# This is run by runclient() in SimServer.
if __name__ == "__main__":
    print("Start SimClient.py")
    if len(sys.argv) != 2:
        print("SYNTAX: python client.py port_rpc")
        sys.exit(-1)
    port_rpc = sys.argv[1]

    client = Client()
    client.connect(port_rpc)

    # Initialize sofa
    sofa = SOFA()
    sofa.step(realtime=False)

    # Work as the order from the server.
    close = False
    while not close:
        # Get order from the server.
        order = client.dataget()
        # order = {'ordername': str(), # in str
        #          'info': dict()}     # in dict
        response = {'data': dict(),}   # in dict
        if order['ordername'] == 'close':
            close = True
        elif order['ordername'] == 'action':
            translation = order['info'].get('translation', 0)
            rotation    = order['info'].get('rotation',    0)
            sofa.action(translation=translation, rotation=rotation)
        elif order['ordername'] == 'step':
            realtime = order['info'].get('realtime', True)
            sofa.step(realtime=realtime)
        elif order['ordername'] == 'GetImage':
            image = sofa.GetImage()
            response['data'] = {'image': image}
        # Put response to the server.
        client.dataput(response)
    print("Close the simulation.")

