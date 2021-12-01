import datetime
import threading
from typing import List

import jsonpickle
from LocalBlockchain import Blockchain
from txServer import txServer
from rxServer import rxServer


class Network:
    '''
    class that encapsulates the network that enables communication between the nodes of the blockchain
    ...
    Attributes:
    ----------
    blockchain : Blockchain
        blockchain that the network uses to verify and send serialized block back and forth
    nodeList : String[]
        list of all the ip addresses to nodes in the network
    port : Integer
        port that the TCP communication is open on, on all nodes
    ...
    Methods:
    -------
    addNode(ip: String) -> Boolean
        adds node's ip address to network - return True on success
    updateNetwork() -> String[]
        sends latest merkleroot along with size of blockchain - enables other nodes to get updated
        returns list of all ip's of the nodes that needed to be updated
    '''

    def __init__(self, blockchain: Blockchain, port=65020):
        '''
        Initializes blockchain network to enable communication between nodes on the network
        ...
        Arguments:
        ---------
        blockchain : Blockchain
            blockchain that the network uses to verify and send serialized block back and forth
        nodeList : String[]
            list of all the ip addresses to nodes in the network
        port : Integer
            port that the TCP communication is open on, on all nodes. If not set = 65020
        ...
        '''
        self.blockchain = blockchain
        self.nodeIps = blockchain.getNodeList()
        self.port = port

        # Starts new thread that continuesly is able to receive updates to the blockchain
        print('Starting rxThread on port: %s' % self.port)
        self.rxThread = threading.Thread(
            target=rxServer, args=[self.blockchain, self.port])
        self.rxThread.start()

    def addNode():

        pass
        # TODO create method

    def update(self):
        '''Requests an update to the blockchain from the connected network'''

        # Create txServer
        tx = txServer(
            nodeList=self.nodeIps, blockchainRef=self.blockchain, port=self.port)

        tx.forceUpdate()

        pass
        # TODO create method

    def smokeTestRxTxLocal(self):
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

        testBC = self.blockchain
        nodelist = self.nodeIps

        test = txServer(nodelist)

        print('\n\nStarting tests!.............................................................................')

        print("\n\nTesting forceUpdate().....................................................................\n")
        test.forceUpdate()

        print("\n\nTesting getNodes()........................................................................\n")
        test.getNodes(testBC)

        print("\n\nTesting broadcastNewTransaction().........................................................\n")
        test.broadcastNewTransactions(testTransactions)

        print("\n\nTesting broadcastPoW()....................................................................\n")
        test.broadcastPoW(testBlock)

        print('\n\n\nAll tests successfully caried out!......................................................\n')
        print('Quit command was send to host...')
        test.sendMsg(host='192.168.50.37', msg='ForceQuitServer',
                     msgLen=len('ForceQuitServer'), preheader=False)
        quit()


if __name__ == '__main__':
    testBC = Blockchain(nodeList=['192.168.50.37'])

    testBlocks = [Blockchain.Block(timestamp=datetime.datetime.now(), transactions=[Blockchain.Block.Body.Transaction(
        epochTimestamp=datetime.datetime.now().timestamp(), data='hejsa')], previousHash='0')]

    testBC.updateBlockchainFromJSON(jsonpickle.encode(testBlocks))

    _network = Network(blockchain=testBC)

    _network.update()
