import socket, threading


def GetName(c):
    SendData(c, 'NameTime')
    name = RecvData(c, 1024)
    SendData(c, name)
    return name


def SendData(c, data):
    try:
        c.send(data.encode('utf-8'))
    except ConnectionResetError:
        ThreadLock1.acquire()
        ThreadLock2.acquire()
        for i in Clients:
            if Clients[i][1] == c:
                del Clients[i]
                break
        c.close()
        ThreadLock1.release()
        ThreadLock2.release()
        


def RecvData(c, buffer):
    print('c = {}'.format(c))
    print('Clients = {}'.format(Clients))
    try:
        data = c.recv(buffer).decode('utf-8')
        return data
    except (ConnectionResetError, OSError):
        pass



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
            Clients[self.name] = [False, self.c]


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
            else:
                for i in Clients:
                    if Clients[i][1] == self.c:
                        del Clients[i]
                        break
                self.c.close()
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
                for i in Clients:
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
            finally:
                ThreadLock1.release()


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
                for i in Clients:
                    if text != '':
                        SendData(Clients[i][1], text)
            except RuntimeError:
                print('Dictionary changed. at PostMessages')
                self.run()
            finally:
                ThreadLock1.release()


def Main():
    kill_list = []
    GConns1 = GetConnections()
    CL1 = CreateListeners()
    PM1 = PostMessages()
    GConns1.start()
    CL1.start()
    PM1.start()


if __name__ == '__main__':
    text = ''
    Listeners = {}
    host = "0.0.0.0"
    port = 5000
    Clients = {}
    ThreadLock1 = threading.Lock()
    ThreadLock2 = threading.Lock()
    ThreadLock3 = threading.Lock()
    s = socket.socket()
    s.bind((host, port))
    Main()

