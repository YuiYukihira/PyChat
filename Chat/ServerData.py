import socket, threading, rsa, pickle
from Crypto.Cipher import AES

class Getconnections(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, *args=(self))
        self.name = ''
        self.c = ''
        self. addr = ''

    def run(self):
        while True:
            self.s.listen(1)
            self.c, self.addr = s.accept()
            self.name = self.GetName(self.c)
            self.Clients[self.name] = [False, self.c]

    def GetName(self):
        self.cPublicKey = pickle.loads(self.c.recv(1024))
        self.c.send(pickle.dumps(self.sPublicKey))

        self.TestMsgc = self.c.recv(1024)
        if not rsa.verify(self.TestMsgc, self.cPublicKey):
            self.c.send('Failed'.encode('utf-8'))
            self.c.close()
        else:
            self.name = 
