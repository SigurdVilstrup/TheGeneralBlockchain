import selectors
import socket
from types import SimpleNamespace


class rxServer:
    '''
    class that encapsulates the server that receives and responds to requests from other nodes.
    ...


    '''

    def __init__(self, port=65020):
        self.selector = selectors.DefaultSelector()
        self.rxPort = port

        # Registers socket to open on TCP connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binds socket to host name socket
        self.socket.bind(
            (socket.gethostbyname(socket.gethostname()), self.rxPort))

        # Continueously listen to socket
        self.socket.listen()
        self.socket.setblocking(False)

        # Register socket in selector to read event
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self._openConnection()
                else:
                    self._handleConnection(mask=mask, key=key)

    def _openConnection(self):
        conn, addr = self.socket.accept()
        conn.setblocking(False)
        print('Data ready to be read')
        data = SimpleNamespace(addr=addr, rx=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(conn, events, data=data)

    def _handleConnection(self, mask, key):
        if mask & selectors.EVENT_READ:
            self._get_request(key=key)

        if mask & selectors.EVENT_WRITE:
            self._respond_to_request(key=key)
            pass

    def _get_request(self, key):
        _rxSocket = key.fileobj
        _data = key.data
        rxData = _rxSocket.recv(512)
        if rxData:
            _data.rx += rxData
        else:
            self.selector.unregister(_rxSocket)
            _rxSocket.close()

    def _respond_to_request(self, key):
        _msg = key.data.rx.decode()

        # TODO create software responses
        # * request(hash) -> Block(hash)
        # * requestUpdate(merkleroot) -> Blockchain
        # * newBlock(block) -> Boolean

        match _msg:
            case '1':
                print('quit', _msg)
                quit()  # TODO Remove
            case '2':
                print('her')
            case 'TGB:update':
                print('sender opdatering tilbage?')
            case _:
                print('All other scenarios:', _msg)

        pass


if __name__ == '__main__':
    rxServer()
