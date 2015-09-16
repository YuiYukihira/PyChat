import socket, threading, rsa, pickle
from Crypto.Cipher import AES

class Getconnections(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, *args)
        self.name = ''
        self.c = ''
        self. addr = ''

    def run(self):
        while True:
            self.s.listen(1)
            self.c, self.addr = s.accept()
            self.name = self.c.recv(1024).decode('utf-8')
            self.Clients[self.name] = [False, self.c]
class Listen


__author__ = 'Yui'
