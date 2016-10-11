import socket
import threading
import time

def GetName(c):
    SendData(c, 'NameTime')
    name = RecvData(c, 1024)
    SendData(c, name)
    return name

def delClient(c):
        ThreadLock1.acquire()
        ThreadLock2.acquire()
        for i,b in enumerate(Clients):
            if Clients[i][1] == c:
                del Clients[i]
                print('dropped client: {}'.format(c))
                break
        c.close()
        ThreadLock1.release()
        ThreadLock2.release()
        

def SendData(c, data):
    try:
        c.send(data.encode('utf-8'))
    except ConnectionResetError:
        delClient(c)


def RecvData(c, buffer):
    print('c = {}'.format(c))
    print('Clients = {}'.format(Clients))
    try:
        data = c.recv(buffer).decode('utf-8')
        return data
    except (ConnectionResetError, OSError):
        delClient(c)



class GetConnections(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = ''
        self.c = ''
        self.addr = ''

    def run(self):
        while True:
            s.listen(1)
            self.c, self.addr = s.accept()
            self.name = GetName(self.c)
            Clients.append([False, self.c, self.name, {}])

class Listener(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        self.c = c['user']
        self.posted = True
        self.text = ''
    def run(self):
        while True:
            self.text = RecvData(self.c, 1024)
            if self.text:
                self.posted = False
                print('Data from {}: {}'.format(self.c, self.text))

            else:
                for i,b in enumerate(Clients):
                    if Clients[i][1] == self.c:
                        del Clients[i]
                        break
                self.c.close()
                print('removed client: {}'.format(self.c))
                break

class CreateListeners(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.c = {}
        self.kill_list = []

    def run(self):
        while True:
            try:
                ThreadLock1.acquire()
                ThreadLock2.acquire()
                for i,b in enumerate(Clients):
                    if Clients[i][0] == False:
                        Clients[i][0] = True
                        self.c['user'] = Clients[i][1]
                    else:
                        self.c = {}
                    if self.c != {}:
                        Listeners[i] = Listener(self.c)
                        Listeners[i].start()
            except RuntimeError:
                print('Dictionary changed. at CreateListeners')
                self.run()
                break
            finally:
                ThreadLock1.release()
                ThreadLock2.release()


class PostMessages(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        text = ''

    def run(self):
        while True:
            text = ''
            try:
                ThreadLock1.acquire()
                for i in Listeners:
                    if Listeners[i].posted == False:
                        text = Listeners[i].text
                        Listeners[i].posted = True
                for i,b in enumerate(Clients):
                    if text != '':
                        if len(text) < 1024:
                            SendData(Clients[i][1], text)
            except RuntimeError:
                print('Dictionary changed. at PostMessages')
                self.run()
            finally:
                ThreadLock1.release()

class sendBroadcast(threading.Thread):
    def __init__(self, ip, port, sname):
        threading.Thread.__init__(self)
        
        self.ip = ip
        self.port = port
        self.sname = sname
        
        self.sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sendSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def run(self):
        while True:
            self.sendSock.sendto(self.sname.encode('utf-8'), (self.ip, self.port))
            time.sleep(1)
    


def Main():
    kill_list = []
    GConns1 = GetConnections()
    CL1 = CreateListeners()
    PM1 = PostMessages()
    BR1 = sendBroadcast(brhost, port, serverName)
    GConns1.start()
    CL1.start()
    PM1.start()
    BR1.start()


if __name__ == '__main__':
    text = ''
    serverName = 'The Pychat server'
    Listeners = {}
    host = "0.0.0.0"
    brhost = "255.255.255.255"
    port = 42120
    Clients = []
    ThreadLock1 = threading.Lock()
    ThreadLock2 = threading.Lock()
    ThreadLock3 = threading.Lock()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    Main()


