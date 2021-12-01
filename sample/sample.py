import datetime
from TGB import Blockchain
from TGB import Network


# TODO To be created later


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

    nodeList = ['192.168.50.37']

    _network = Network(_localBC, nodeList)

    runMenu(_localBC)
