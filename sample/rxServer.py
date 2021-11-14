import selectors
import socket
from types import SimpleNamespace
from copy import copy


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

    def _send(self, key, message):
        _socket = key.fileobj
        _socket.send(message)
        key.data.rxb = b''

    def _createHeader(self, headerIn):
        if isinstance(headerIn, int):
            header = copy(str(headerIn).encode('utf-8'))
            header = b'HEAD' + header
            while len(header) != 16:
                header = header + b' '
            print('Header set to 16 byte array, ', header)
            return header
        else:
            raise ValueError(
                "createHeader error - not type int", type(headerIn))

    def _sendResponse(self, socket, response):
        # Send header first - always 16 bit array
        self._send(socket, self._createHeader(len(response)))

        # Send body after
        self._send(socket, response)
        pass

    def _openConnection(self):
        conn, addr = self.socket.accept()
        conn.setblocking(False)

        data = SimpleNamespace(addr=addr, rxb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        self.selector.register(conn, events, data=data)

    def _handleConnection(self, mask, key):
        if mask & selectors.EVENT_READ:
            self._readRequest(key=key)

        if mask & selectors.EVENT_WRITE:
            self._respondRequest(key=key)

    def _readRequest(self, key):
        _socket = key.fileobj
        data = key.data

        rxData = _socket.recv(1024)
        if rxData:
            data.rxb += rxData
        else:
            print('connection closed to: ', data.addr)
            self.selector.unregister(_socket)
            _socket.close()

    def _respondRequest(self, key):
        _socket = key.fileobj  # TODO REMOVE

        _request = copy(key.data.rxb)

        # TODO create software responses
        # * request(hash) -> Block(hash)
        # * requestUpdate(merkleroot) -> Blockchain
        # * newBlock(block) -> Boolean

        match _request:
            case b'1':
                print('quit')
                quit()  # TODO Remove
            case b'2':
                print('her')
            case b'TGB:update':
                print('Responding with: header data')
                self._send(key, self._createHeader(32))

            case _:
                if key.data.rxb:
                    print('Responding with: ', b'rx %s ok' %
                          (key.data.rxb), 'to', key.data.addr)
                    sent = _socket.send(b'rx %s ok' % (key.data.rxb))
                    key.data.rxb = key.data.rxb[sent:]


if __name__ == '__main__':
    server = rxServer()
