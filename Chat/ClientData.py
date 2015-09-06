import socket, threading, rsa
from Crypto.Cipher import AES
from tkinter import *, ttk
from time import sleep


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
        Msg_entry = ttk.Entry(self.mainframe, width=20, textvariable=Msg).grid(column=2, row=2, stick=(W, E, S))

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.root.bind('<Return>', self.SendMessage)

    def SendMessage():
        toSend = self.Msg.get()
        Space = if toSend == ' '*len(toSend): True else: False
        if toSend != '' and Space == False:
            self.s.send((self.Name+': '+toSend).encode('utf-8'))
            self.Msg.set('')
