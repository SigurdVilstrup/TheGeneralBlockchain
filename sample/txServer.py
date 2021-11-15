from copy import copy
import selectors
import socket
from types import SimpleNamespace

from LocalBlockchain import Blockchain


class txServer:
    '''
    class that encapculates the transmit (tx) thread
    ...
    Attributes:
    ----------
        txHost : String
        txPort : Integer
    ...
    Methods:
    -------
        sendMsg(msgs : String) -> None
            sends message (serialized block / request) to rest of blockchain
    '''

    def __init__(self, nodeList, port=65020):
        self.nodeList = nodeList
        self.txPort = port

        self.selector = selectors.DefaultSelector()

    def sendMsg(self, host, msg, msgLen, preheader):
        '''
        sends message (serialized block) to rest of blockchain
        ...
        Parameters:
        ----------
        host : String
            host that the message should be send to 'ip address'
        msg : String
            message (serialized blocks / request) to send to other nodes in the network
        '''

        # TODO needs to be able to receive header first - get length and afterwards receiver data/body

        self._startConnection(
            host=host,
            data=SimpleNamespace(recv_total=0,
                                 message=msg,
                                 outb=b''))

        while True:
            events = self.selector.select(timeout=1)
            if events:
                for key, mask in events:
                    # Get value
                    value = self._handleTxRx(key=key, mask=mask, rxLen=msgLen)

            if not self.selector.get_map():
                if preheader:
                    _type, _len = self._getLenFromPreHeader(value)
                    print('type found:', _type, 'Next len:', _len)
                    return _type, _len
                else:
                    return value

    def _getLenFromPreHeader(self, value):
        '''
        get length of either Header or body from preheader
        return (type:str, len:int)
        type can be: 'HEAD' or 'CMND'
        '''
        print(value)
        returnValue = copy(value[4:])
        type = copy(value[0:4])

        while returnValue[-1] == 32:
            returnValue = returnValue[0:-1]

        return (type.decode(), int(returnValue))

    def _startConnection(self, host, data):
        '''
        Starts connection to host with predefined port
        ...
        Parameters:
        ----------
        host : String
            ip address of host to connect to
        '''

        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setblocking(False)
        _socket.connect_ex((host, self.txPort))

        self.selector.register(_socket, selectors.EVENT_READ | selectors.EVENT_WRITE,
                               data=data)
        print('Connection to %s has been started' % (host))

    def _handleTxRx(self, key, mask, rxLen):
        _socket = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            rxData = _socket.recv(1024)
            if rxData:
                data.recv_total += len(rxData)
            if data.recv_total == rxLen:
                print('Received: %s, closing connection to Node' % rxData)
                self.selector.unregister(_socket)
                _socket.close()
                return rxData

        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.message:
                data.outb = data.message.encode('utf-8')
                data.message = ''
            if data.outb:
                print('sending', repr(data.outb), 'to connection')
                sent = _socket.send(data.outb)
                data.outb = data.outb[sent:]

    def getUpdate(self, host):
        # Get preheader
        _type, _len = self.sendMsg(host, 'TGB:update', 16, True)

        if _type == 'CMND':
            update = self.sendMsg(host, 'TGB:update:nxt', _len, False)

        print(update.decode())


if __name__ == '__main__':
    # For testing
    test = txServer(nodeList=['192.168.50.37', '0.0.0.0'])
    test.getUpdate(host='192.168.50.37')