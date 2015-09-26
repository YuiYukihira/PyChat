import socket, threading

# Define GetName function.
def GetName(c):
    SendData(c, 'NameTime')
    name = RecvData(c, 1024)
    SendData(c, name)
    return name

# Define SendData function.
def SendData(c, data):
    try:
        # Try and send some data.
        c.send(data.encode('utf-8'))
    except ConnectionResetError:
        # If the connection was reset, remove the client from the list of connected clients.
        ThreadLock1.aquire()
        ThreadLock2.aquire()
        for i in Clients:
            if Clients[i][1] == c:
                del Clients[i]
                break
        c.close()
        ThreadLock1.release()
        ThreadLock2.release()

# Define RecvData function.
def RecvData(c, buffer):
    print('c = {}'.format(c))
    print('Clients = {}'.format(Clients))
    try:
        # Try and recive some data.
        data = c.recv(buffer).decode('utf-8')
        return data
    except (ConnectionResetError, OSError):
        # If that fails, emove the client from the list of connected clients.
        ThreadLock1.acquire()
        ThreadLock2.acquire()
        for i in Clients:
            if Clients[i][1] == c:
                del Clients[i]
                break
        c.close()
        ThreadLock1.release()
        ThreadLock2.release()

# Define GetConnections class
class GetConnections(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = ''
        self.c = ''
        self.addr = ''

    def run(self):
        while True:
            # Find client, Get thier name, add to list of connected clients.
            s.listen(1)
            self.c, self.addr = s.accept()
            self.name = GetName(self.c)
            Clients[self.name] = [False, self.c]

# Define Listener class.
class Listener(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        self.c = c['user']
        self.name = c
        self.posted = True
        self.text = ''
        
    def run(self):
        while True:
            # Recieve message.
            self.text = RecvData(self.c, 1024)
            if self.text:
                # If message exists set posted to False.
                self.posted = False
            else: self.posted = False;self.text = 'user has left the server';break
            # Otherwise set posted to False and text to 'user has left the server'.

# Define CreateLsteners class
class CreateListeners(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.c = {}
        self.kill_list = []

    def run(self):
        while True:
            try:
                # Does the client has a listener? yes: check the next client. no: create one.
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
                print('Dictionary changed.')
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
                ThreadLock2.acquire()
                for i in Listeners:
                    # Does listener i have a new message? yes: send message to new all clients. no: go onto the next listener.
                    if Listeners[i].posted == False:
                        text = Listeners[i].text
                        Listeners[i].posted = True
                for i in Clients:
                    if text != '':
                        SendData(Clients[i][1], text)
            except RuntimeError:
                print('Dictionary changed.')
                self.run()
            finally:
                ThreadLock2.release()

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
