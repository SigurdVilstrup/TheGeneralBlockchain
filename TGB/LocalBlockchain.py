import datetime
from typing import List, NamedTuple
import hashlib
import jsonpickle
import json

from jsonpickle.unpickler import decode


# Dataclass for the blockchain
class Blockchain:
    '''
    A class that represenents a blockchain.
    ...
    Attributes:
    ----------
    blocks : Block[]
        a list of all blocks in the blockchain
    ...
    Methods:
    -------
    deserializeBlock(string=None) -> Block
        deserializes block from json string input
    '''

    def __init__(self, nodeList):
        '''
        Parameters:
        ----------
        self : self
            Initializes blockchain with a genesis block.
        '''
        self.blocks = []
        self.nodeList = nodeList

    def updateBlockchainFromJSON(self, jsonString: str):
        # object_type = str(type([Blockchain.Block]))
        # json_dict = json.loads(jsonString)
        # json_dict.update({"py/object": object_type})

        print('Decoded into: %s' % jsonpickle.decode(jsonString))

    def createBlock(self, header, body):
        # Should run through PoW and return block when PoW is found correctly.
        # This should be done in a seperate thread probably. (Not a proority, set difficulty to easy)
        return self.Block(timestamp=header.timestamp, transactions=body.transactions)

    def getNodeList(self):
        return self.nodeList

    class Block:
        '''
        A class that represents a single block in a blockchain.

        ...

        Attributes:
        ----------
        body : Body
            body of the block
        header : Header
            header of the block

        ...
        '''

        def __init__(self, timestamp, transactions, previousHash):
            '''
            Parameter:
            ---------
            timestamp : Timestamp
                timestamp of the creation of the block
            transactions : Transaction[]
                list of the transactions contained in the block
            previousHash : String
                hash of the previous block in the blockchain

            '''
            self.body = self.Body(transactions=transactions)
            self.header = self.Header(
                version='0.1',
                bodySize=len(jsonpickle.encode(self.body)),
                timestampEpoch=timestamp.timestamp(),
                merkleroot=self._calcMerkleRoot(transactions),
                preHash=previousHash,
            )

        class Body(NamedTuple):
            '''
            Class that represents body of a block in the blockchain
            ...
            Attributes:
            ----------
            transactions : Transaction[]
                list of transactions in body
            '''
            transactions: List

            class Transaction(NamedTuple):
                '''
                Class that represents a transaction
                ...
                Attributes:
                ----------
                    epochTimestamp : Integer
                        epoch timestamp of when the transaction took place
                    data : String
                        data in the form of a string - very loose definition since it's meant to be an educational blockchain
                '''
                epochTimestamp: int
                data: str

        class Header(NamedTuple):
            '''
            Class that represents the header in a block of the blockchain
            ...
            Attributes:
            ----------
            bodySize : Integer
                size of the serialized body - to make sure to receive all data when requesting it
            timestampEpoch : Integer
                timestamp of the block
            merkleroot : String
                merkleroot of all the transactions
            version : String
                version of the blockchain i.e.: v0.23
            preHash : String
                hash of the previous block in the blockchain
            '''
            bodySize: int
            timestampEpoch: int
            merkleroot: str
            version: str
            preHash: str

            def calcHash(self):
                '''
                Calculates hash of the current block in the blockchain.
                returns hash as a string object of double lenght as per hashlib's hexdigest().
                '''
                h = hashlib.sha256()

                h.update(str(self.bodySize).encode('utf-8'))
                h.update(str(self.timestampEpoch).encode('utf-8'))
                h.update(self.merkleroot.encode('utf-8'))
                h.update(self.version.encode('utf-8'))
                h.update(self.preHash.encode('utf-8'))

                return h.hexdigest()

        def _calcMerkleRoot(self, transactions: List):
            print('Starting Merkle Root Calculation...')

            # List of all hashes
            allHashes = []

            # Fill list of all hashes
            for t in transactions:
                allHashes.append(hashlib.sha256(
                    jsonpickle.encode(t).encode('utf-8')).hexdigest())

            # Always even number of hashes total
            if (len(allHashes) % 2 != 0):
                allHashes.append(allHashes[-1])

            curHashes = allHashes

            print('hashes being rooted:', len(curHashes))

            # While there is more than one hash keep hashing them together to get root
            while len(curHashes) != 1:
                prevHashes = curHashes[:]
                curHashes.clear()

                # Concatenate e.g., 0+1, 2+3, 4+5, 6+6, etc...
                for i in range(round(len(prevHashes)/2)):
                    temp = hashlib.sha256()
                    temp.update(prevHashes[i*2].encode('utf-8'))
                    temp.update(prevHashes[i*2+1].encode('utf-8'))
                    curHashes.append(temp.hexdigest())

            # the last and single hash must be the merkleroot of the blockchain
            print('Merkle Root calculation finished', curHashes[0])
            return curHashes[0]

        def printHeader(self):
            '''
            prints header data for the block of self
            '''
            print(
                """Body size:      %s,
Timestamp:      %s,
Merkle root:    %s,
Version:        %s,
Previous Hash:  %s
Hash:           %s
            """
                % (
                    self.header.bodySize,
                    datetime.datetime.fromtimestamp(
                        self.header.timestampEpoch),
                    self.header.merkleroot,
                    self.header.version,
                    self.header.preHash,
                    self.header.calcHash(),
                )
            )

        def printBody(self):
            '''
            prints body data for the block of self
            '''
            for t in self.body.transactions:
                print(t)
            print('\n')

        def printAll(self):
            '''
            prints all (header and body) data for the block of self
            '''
            print("Header:")
            self.printHeader()
            print("Body:")
            self.printBody()

    def addBlock(self, block: Block):
        '''
        Adds block to the blockchain
        ...
        Parameters:
        ----------
        timestamp : Timestamp
        transactions : Transaction[]
        '''
        self.blocks.append(block)
