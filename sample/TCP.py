import selectors
import socket
import threading
import types


class txThread:
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
        sendMsgs(msgs : String) -> None
            sends message (serialized block) to rest of blockchain

    '''

    def __init__(self, host, port):
        self.txHost = host
        self.txPort = port

        self.selector = selectors.DefaultSelector()

    def sendMsgs(self, msgs):
        '''
        sends message (serialized block) to rest of blockchain
        ...
        Parameters:
        ----------
        msgs : String
            messages (serialized blocks) to send to other nodes in the network
        '''
        self._start_connection(host=self.txHost, port=self.txPort,
                               num_conns=2, msgs=msgs, selector=self.selector)

        while True:
            events = self.selector.select(timeout=1)
            if events:
                for key, mask in events:
                    self._service_connection(
                        key=key, mask=mask, sel=self.selector)
            if not self.selector.get_map():
                break

    def _start_connection(self, num_conns, msgs):
        server_addr = (self.txHost, self.txPort)

        for i in range(0, num_conns):
            connid = i + 1
            print('starting connection', connid, 'to', server_addr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(connid=connid,
                                         msg_total=sum(len(m)
                                                       for m in msgs),
                                         recv_total=0,
                                         messages=list(msgs),
                                         outb=b'')
            self.selector.register(sock, events, data=data)

    def _service_connection(key, mask, sel):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                print("received:", repr(recv_data),
                      'from connection', data.connid)
                data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print('closing connection:', data.connid)
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)
            if data.outb:
                print('sending', repr(data.outb),
                      'to connection', data.connid)
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]





if __name__ == '__main__':
    rxThread = rxThread(port=33333)
