import selectors
import socket
from types import SimpleNamespace
from copy import copy
import jsonpickle
from LocalBlockchain import Blockchain


class rxServer:
    '''
    class that encapsulates the server that receives and responds to requests from other nodes.
    ...


    '''

    def __init__(self, blockchainRef: Blockchain, port=65020):
        self.selector = selectors.DefaultSelector()
        self.rxPort = port
        self.blockchain = blockchainRef

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

    def _createPreHeader(self, length: int, type):
        if isinstance(length, int):
            header = copy(str(length).encode('utf-8'))
            match type:
                case 'DATA':
                    header = b'DATA' + header
                case 'CMND':
                    header = b'CMND' + header
                case _:
                    raise ValueError(
                        'type not supported: use HEAD or CMND, tried:', type)

            while len(header) != 16:
                header = header + b' '
            print('Header set to 16 byte array, ', header)
            return header
        else:
            raise ValueError(
                "createHeader error - not type int", type(length))

    def _sendResponse(self, socket, response):
        # Send header first - always 16 bit array
        self._send(socket, self._createPreHeader(len(response)))

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

    def _handleUpdateRequest(self, data, key):
        if len(self.blockchain.blocks) > 0:
            newestHash = self.blockchain.blocks[-1].header.calcHash()
        else:
            newestHash = 'updateMePleaseNodeFriend'

        if data.decode() == newestHash:
            print('Responding with: header data')
            self._send(key, self._createPreHeader(
                length=200, type='CMND'))

        elif data == b'blockchainData':
            # TODO this needs to be dynamic so that the JSON strings are sent when asked for
            self._send(
                key, jsonpickle.encode(self.blockchain.blocks).encode('utf-8'))
            pass

        else:
            print('Responding with data to update blockchain.')
            self._send(key, self._createPreHeader(
                len(jsonpickle.encode(self.blockchain.blocks)), type='DATA'))

        pass

    def _respondRequest(self, key):
        _socket = key.fileobj  # TODO REMOVE

        _request = copy(key.data.rxb[0:16].rstrip())
        _data = copy(key.data.rxb[16:])

        print("Received request: %s, with data %s" % (_request, _data))

        # TODO create software responses
        # * request(hash) -> Block(hash)
        # * requestUpdate(merkleroot) -> Blockchain
        # * newBlock(block) -> Boolean

        match _request:
            case b'ForceQuitServer':
                print('quit')
                self._send(key, self._createPreHeader(
                    length=200, type='CMND'))
                quit()
            case b'TGB:newTrans:':
                print('Received transactions: %s' %
                      (jsonpickle.decode(_data.decode())))
                self._send(key, self._createPreHeader(length=200, type='CMND'))
                pass
            case b'TGB:PoW:':
                print('Recevied block: %s' %
                      (jsonpickle.decode(_data.decode())))

                # If block header nonce is correct
                # TODO dynamically check whether it is correct
                if True:
                    self._send(key, self._createPreHeader(
                        length=200, type='CMND'))

                # Else return error message
                else:
                    self._send(key, self._createPreHeader(
                        length=404, type='CMND'))
                pass
            case b'TGB:getNodes:':
                if _data == b'':
                    self._send(key, self._createPreHeader(
                        length=len(b'List of all the nodes in this node!'), type='DATA'))
                if _data == b'getData':
                    self._send(key, b'List of all the nodes in this node!')
            case b'TGB:update:':
                self._handleUpdateRequest(data=_data, key=key)

            case _:
                if key.data.rxb:
                    print('Responding with: ', b'rx %s ok' %
                          (key.data.rxb), 'to', key.data.addr)
                    sent = _socket.send(b'rx %s ok' % (key.data.rxb))
                    key.data.rxb = key.data.rxb[sent:]


if __name__ == '__main__':
    server = rxServer()
