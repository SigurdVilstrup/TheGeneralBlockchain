from sys import argv
from context import TGB


if __name__ == '__main__':
    print('Running communication smoketest.')

    if len(argv) == 1:
        print('please input local address for testing the communication as an argument\nEx. %s 111.111.11.11' % (
            argv[0]))
        quit()

    if len(argv) == 2:
        _testNodes = [argv[1]]

        _testBC = TGB.Blockchain(_testNodes)
        _testNetwork = TGB.Network(_testBC)
        _testNetwork.smokeTestRxTxLocal()
