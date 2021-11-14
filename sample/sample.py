import datetime
from LocalBlockchain import Blockchain
from network import Network


def runMenu(blockchain):
    while True:
        _input = input()

        match _input:
            case 'q':
                quit()

            case 'h' | 'help':
                print('''Help menu ######################################\r

h           : Help menu
q           : Quit blockchain
print       : Print all blocks in blockchain
addBlock    : Add new block to blockchain

################################################''')

            case 'print':
                for b in blockchain.blocks:
                    print('Block', blockchain.blocks.index(b), '\n')
                    b.printAll()

            case 'addBlock':
                _transactions = []
                _more = 'Y'
                while True:
                    print('Input transaction data')
                    _data = input()
                    _timestamp = datetime.datetime.now()

                    _transactions.append(
                        Blockchain.Block.Body.Transaction(_timestamp, _data))

                    print('Add more transactions to block? (Y/n)')
                    _more = input()
                    if _more == 'Y' or _more == '':
                        pass
                    else:
                        break

                blockchain.addBlock(timestamp=_timestamp,
                                    transactions=_transactions)


if __name__ == '__main__':
    _localBC = Blockchain()

    nodes = []

    _network = Network(_localBC, nodes)

    for i in range(6):
        _localBC.addBlock(timestamp=datetime.datetime.now(), transactions=[Blockchain.Block.Body.Transaction(
            epochTimestamp=datetime.datetime.now().timestamp(), data='data point no. '+str(i)), ])

    runMenu(_localBC)