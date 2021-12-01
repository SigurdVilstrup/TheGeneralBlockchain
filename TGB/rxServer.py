import selectors
import socket
import time
from types import SimpleNamespace
from copy import copy
import jsonpickle
from LocalBlockchain import Blockchain
import random


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
            self._respondRequest(_key=key)

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
            # 'updateMePleaseNodeFriend' is the official newestHash of a TGB blockchain that contains no blocks.
            newestHash = 'updateMePleaseNodeFriend'

        if data.decode() == newestHash:
            print('Responding with: header data')
            self._send(key, self._createPreHeader(
                length=200, type='CMND'))

        elif data == b'blockchainData':
            self._send(
                key, jsonpickle.encode(self.blockchain.blocks).encode('utf-8'))
            pass

        else:
            print('Responding with data to update blockchain.')
            self._send(key, self._createPreHeader(
                len(jsonpickle.encode(self.blockchain.blocks)), type='DATA'))

    def _handleNodeRequest(self, data, key):
        nodeList = jsonpickle.encode(self.blockchain.nodeList)

        # If there is no data, send back preheader with length
        if data == b'':
            self._send(
                key,
                message=self._createPreHeader(length=len(nodeList.encode()), type='DATA'))

        # If data is == getData, a specific request being send from network, send all the data back
        if data == b'getData':
            self._send(
                key,
                message=nodeList.encode())

    def _handleNewTransaction(self, data, key):
        # TODO should this be a seperate thread?
        print('Received transactions: %s' %
              (jsonpickle.decode(data.decode())))

        self._send(key, self._createPreHeader(
            length=200, type='CMND'))

        tempBlock = self.blockchain.createBlock(
            header=Blockchain.Block.Header(),
            body=Blockchain.Block.Body())
        # TODO actually start the process of creating the PoW, whether it be simulated or not.
        # Simulate PoW for now - timer in random interval.
        # msSleepTime = random.randint(50, 2000)
        # time.sleep(msSleepTime/1000)

    def _respondRequest(self, _key):
        _socket = _key.fileobj

        _request = copy(_key.data.rxb[0:16].rstrip())
        _data = copy(_key.data.rxb[16:])

        print("Received request: %s, with data %s" % (_request, _data))

        match _request:
            case b'ForceQuitServer':
                print('quit')
                self._send(_key, self._createPreHeader(
                    length=200, type='CMND'))
                quit()
            case b'TGB:newTrans:':
                self._handleNewTransaction(data=_data, key=_key)

            case b'TGB:PoW:':
                self._handlePoWRequest(data=_data, key=_key)
                print('Recevied block: %s' %
                      (jsonpickle.decode(_data.decode())))

                # If block header nonce is correct
                # TODO dynamically check whether it is correct
                if True:
                    self._send(_key, self._createPreHeader(
                        length=200, type='CMND'))

                # Else return error message
                else:
                    self._send(key, self._createPreHeader(
                        length=400, type='CMND'))
                pass
            case b'TGB:getNodes:':
                self._handleNodeRequest(data=_data, key=_key)

            case b'TGB:update:':
                self._handleUpdateRequest(data=_data, key=_key)

            case _:
                if _key.data.rxb:
                    print('Responding with: ', b'rx %s ok' %
                          (_key.data.rxb), 'to', _key.data.addr)
                    sent = _socket.send(b'rx %s ok' % (_key.data.rxb))
                    _key.data.rxb = _key.data.rxb[sent:]


if __name__ == '__main__':
    server = rxServer()
