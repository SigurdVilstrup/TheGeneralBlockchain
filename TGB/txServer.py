from copy import copy
import selectors
import socket
from types import SimpleNamespace
from typing import List

import jsonpickle
from .LocalBlockchain import Blockchain
import datetime


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
        print('Starting txServer with nodeList %s, and port %s...' %
              (nodeList, port))
        self.nodeList = nodeList
        self.txPort = port

        self.selector = selectors.DefaultSelector()

    def sendMsg(self, host, msg, msgLen, preheader=False):
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

    def forceUpdate(self):
        for node in self.nodeList:
            # TODO - newestHash should dynamically be the newest hash in the local blockchain
            _type, _len = self.sendMsg(
                node, 'TGB:update:'.ljust(16)+'aLaterHash', 16, True)
            print('type found:', _type, 'Next len:', _len)

            if _type == 'CMND' and _len == 200:
                print("Blockchain is up to date")
                return

            if _type == 'DATA':
                print("Getting blockchain from updated node")
                _value = self.sendMsg(
                    node, 'TGB:update:'.ljust(16)+'blockchainData', _len)

                # _value that is received is the blockchain as a Json String
                print(_value)
                pass
        pass

    def getBlockchain(self, blockchainReference: Blockchain):
        # TODO integrate later - how is it different to forceUpdate? Maybe only meant to be called when initialized? To skip update request.
        pass

    def getNodes(self, blockchainReference: Blockchain):
        # TODO request all nodes from node(s)
        for node in self.nodeList:
            _type, _len = self.sendMsg(
                node, 'TGB:getNodes:'.ljust(16), 16, True)
            print('type found:', _type, 'Next len:', _len)
            if _type == 'DATA':
                _value = self.sendMsg(
                    node, 'TGB:getNodes:'.ljust(16)+'getData', _len)
                print(_value)
                # _value received is the list of nodes as a Json string
                pass
        pass

    def broadcastNewTransactions(self, transactions: List[Blockchain.Block.Body.Transaction]):
        # TODO broadcast a new transaction to the whole network
        for node in self.nodeList:
            _type, _len = self.sendMsg(
                node, 'TGB:newTrans:'.ljust(16)+jsonpickle.encode(transactions), 16, True)
            print('type found:', _type, 'Next len:', _len)
            if _type == 'CMND' and _len == 200:
                print('node:', node, 'has received new transaction')
                return
            pass
        pass

    def broadcastPoW(self, block: Blockchain.Block):
        # TODO broadcast Proof of Work to network after receival of the new transaction(s)
        for node in self.nodeList:
            _type, _len = self.sendMsg(
                node, 'TGB:PoW:'.ljust(16)+jsonpickle.encode(block), 16, True)

            if _type == 'CMND' and _len == 200:
                print('node:', node, 'has accepted proof of work')
                return

            if _type == 'CMND' and _len == 404:
                print('node:', node, 'has denied proof of work')
                return
        pass


if __name__ == '__main__':
    testTransactions = [Blockchain.Block.Body.Transaction(
        epochTimestamp=datetime.datetime.now().timestamp(), data='hejsa'),
        Blockchain.Block.Body.Transaction(
        epochTimestamp=datetime.datetime.now().timestamp(), data='hejsa'),
        Blockchain.Block.Body.Transaction(
        epochTimestamp=datetime.datetime.now().timestamp(), data='hejsa'),
        Blockchain.Block.Body.Transaction(
        epochTimestamp=datetime.datetime.now().timestamp(), data='hejsa')]

    testBlock = Blockchain.Block(
        timestamp=datetime.datetime.now(),
        transactions=[Blockchain.Block.Body.Transaction(
            epochTimestamp=datetime.datetime.now().timestamp(), data='data')],
        previousHash="")

    testBC = Blockchain()
    nodelist = ['192.168.50.37']

    test = txServer(nodelist)

    print('\n\n\nStarting tests!...........................................................................')

    print("\n\nTesting forceUpdate().....................................................................\n")
    test.forceUpdate()

    print("\n\nTesting getNodes()........................................................................\n")
    test.getNodes(testBC)

    print("\n\nTesting broadcastNewTransaction().........................................................\n")
    test.broadcastNewTransactions(testTransactions)

    print("\n\nTesting broadcastPoW()....................................................................\n")
    test.broadcastPoW(testBlock)

    print('\n\n\nAll tests successfully caried out!......................................................\n')
