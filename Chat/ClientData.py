import socket, threading, pickle, os
from tkinter import *
from tkinter import ttk
from time import sleep
import importlib

rsa_loader = importlib.find_loader('rsa')
found_rsa = rsa_loader is not None
if found_rsa == False:
    os.system('C:\Python34\Scripts\easy_install rsa')

from Crypto.Cipher import AES
import rsa

class Client:
    def __init__(self, host='127.0.0.1', port=5000, name=None):
        self.s = socket.socket()
        self.server = (host, port)
        if name == None:
            self.namer1 = Namer(self)
            self.namer1.start()
        else:
            self.Name = name
        self.GUI1 = GUI(self)
        self.GM1 = GetMessage(self)
        
    def start(self):
        self.s.connect(self.server)
        self.cPubicKey, self.cPrivateKey = rsa.newkeys(1024)
        self.s.send(pickle.dumps(self.cPublicKey))
        self.sPublicKey = pickle.loads(self.s.revc(1024))

        self.TestMsgc = rsa.encrypt(self.Name.encode('utf-8'), self.sPublicKey)
        self.TestMsgcS = rsa.sign(self.TestMsgc, self.cPrivateKey)
        self.s.send(self.TestMsgc)
        self.s.send(TestMsgcS)
        if self.s.recv(1024).decode('utf-8') == 'Failed':
            self.s.close()

        self.TestMsgs = self.s.recv(1024)
        if rsa.verify(self.TestMsgs, self.sPublicKey) :
            self.s.close()
            self.start() #If athentication fails the client will for now restart.
        else:
            if rsa.verify(self.TestMsgs, self.sPublicKey):
                self.s.send('Passed'.encode('utf-8'))
                self.GUI1.start()
                self.GM1.start()
            else:
                self.s.send('Failed'.encode('utf-8'))
                self.s.close()
                self.start() #If athentication fails the client will for now restart.
        
class Namer(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)

    def Quit(self):
        self.root.destroy()

    def run(self):
        self.root = Tk()
        self.root.title('The safe python chat')

        self.mainframe = ttk.Frame(self.root, padding='3 3 3 3')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.name = StringVar()

        ttk.Button(self.mainframe, text='Confirm name:', command=self.Setname).grid(column=1, row=1, sticky=(N, W, E, S))
        Name_entry = ttk.Entry(self.mainframe, width=12, textVariable=self.name).grid(column=2, row=1, sticky=(N, W, E, S))

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.root.bind('<Return>', Setname)

        self.root.mainloop()

    def SetName(*args):
        self.Name = name.get()
        
class GetMessage(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.text = ''

    def run(self):
        while True:
            try:
                self.text += s.recv(1024).decode('utf-8') + '\n')
            except:
                sleep(0.1)
            finally:
                self.chat.set(self.text)

class GUI(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
    
    def Quit(self):
        self.root.destroy()
        
    def run(self):
        self.root = Tk()
        self.root.title('The safe python chat')

        self.mainframe = ttk.Frame(self.root, padding='3 3 3 3')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.chat = StringVar()
        self.Msg = StringVar()

        ttk.Label(self.mainframe, textvariable=chat).grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.button(self.mainframe, text='QUIT', command=self.Quit).grid(column=2, row=1, Sticky=(N, W, E))

        ttk.button(self.mainframe, text='Send Message:', command=self.SendMessage).grid(column=1, row=2, sticky=(N, W, E, S))
        self.Msg_entry = ttk.Entry(self.mainframe, width=20, textvariable=Msg).grid(column=2, row=2, stick=(W, E, S))

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.root.bind('<Return>', self.SendMessage)

        self.root.mainloop()

    def SendMessage():
        toSend = self.Msg.get()
        Space = if toSend == ' '*len(toSend): True else: False
        if toSend != '' and Space == False:
            self.s.send((self.Name+': '+toSend).encode('utf-8'))
            self.Msg.set('')

if __name__ == '__main__':
    testClient = Client(host='127.0.0.1', port=5000, name='Yui')
