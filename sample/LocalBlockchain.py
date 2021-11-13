import datetime
from typing import List, NamedTuple
import hashlib
import jsonpickle


class Blockchain:
    def __init__(self):
        self.blocks = [
            self.Block(timestamp=datetime.datetime.now(),
                       transactions=[self.Block.Body.Transaction(
                           epochTimestamp=datetime.datetime.now().timestamp, data='Genesis!')],
                       previousHash='00000000000000')
        ]

    class Block:
        def __init__(self, timestamp, transactions, previousHash):
            self.body = self.Body(transactions=transactions)
            self.header = self.Header(
                version='0.1',
                bodySize=len(jsonpickle.encode(self.body)),
                timestampEpoch=timestamp.timestamp(),
                merkleroot=self._calcMerkleRoot(transactions),
                preHash=previousHash,
            )

        class Body(NamedTuple):
            transactions: List

            class Transaction(NamedTuple):
                epochTimestamp: int
                data: str

        class Header(NamedTuple):
            bodySize: int
            timestampEpoch: int
            merkleroot: str
            version: str
            preHash: str

            def calcHash(self):
                h = hashlib.sha256()

                h.update(str(self.bodySize).encode('utf-8'))
                h.update(str(self.timestampEpoch).encode('utf-8'))
                h.update(self.merkleroot.encode('utf-8'))
                h.update(self.version.encode('utf-8'))
                h.update(self.preHash.encode('utf-8'))

                return h.hexdigest()

        def _calcMerkleRoot(self, transactions):
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
            for t in self.body.transactions:
                print(t)
            print('\n')

        def printAll(self):
            print("Header:")
            self.printHeader()
            print("Body:")
            self.printBody()

    def addBlock(self, timestamp, transactions):
        self.blocks.append(self.Block(timestamp=timestamp, transactions=transactions,
                                      previousHash=self.blocks[-1].header.calcHash()))
