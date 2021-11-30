import threading
from typing import List
from sample.LocalBlockchain import Blockchain
from sample.rxServer import rxServer


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

    def __init__(self, blockchain: Blockchain, nodeList: List, port=65020):
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
        self.blockchain = Blockchain
        self.nodeIps = nodeList
        self.port = port

        # Starts new thread that continuesly is able to receive updates to the blockchain
        self.rxThread = threading.Thread(
            target=rxServer, args=(self.port))

    def addNode():
        pass
        # TODO create method

    def updateNetwork():
        pass
        # TODO create method
