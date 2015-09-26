import threading, socket, random
from time import sleep
from tkinter import *
from tkinter import ttk


class Namer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        sleep(0.1)

    def Quit(self):
        self.namer.destroy()

    def run(self):
        global name
        self.namer = Tk()
        self.namer.title('The PyChat')

        self.nameframe = ttk.Frame(self.namer, padding='3 3 3 3')
        self.nameframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.nameframe.columnconfigure(0, weight=1)
        self.nameframe.rowconfigure(0, weight=1)

        name = StringVar()

        ttk.Button(self.nameframe, text="Confirm name:", command=SetName).grid(column=1, row=1, sticky=(N, W, E, S))
        Name_entry = ttk.Entry(self.nameframe, width=7, textvariable=name).grid(column=2, row=1, sticky=(N, W, E, S))

        for child in self.nameframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.namer.bind('<Return>', SetName)

        self.namer.mainloop()


class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        sleep(0.1)

    def Quit(self):
        self.root.destroy()

    def run(self):
        global chat
        global Msg
        threading.Thread.__init__(self)
        self.root = Tk()
        self.root.title('The PyChat')
        self.root.geometry('400x620')
        
        self.mainframe = ttk.Frame(self.root, padding='3 3 3 3')
        self.mainframe.grid(sticky=(N, W, E, S))
        self.mainframe.pack(fill=BOTH, expand=1)
        self.sendframe = ttk.Frame(self.root, relief=RAISED, borderwidth=1)
        self.sendframe.pack(fill=BOTH, expand=0)

        chat = StringVar()
        Msg = StringVar()
        ttk.Label(self.mainframe, textvariable=chat, wraplength=380, anchor='nw',text="Top Left").grid(sticky=(N, W, E, S))
        Msg_entry = ttk.Entry(self.sendframe, width=20, textvariable=Msg).grid(column=0, row=0, sticky=(W, E, S))
        ttk.Button(self.sendframe, text="Send Message:", command=SendMessage).grid(column=1, row=0, sticky=(W, S))
        

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.root.bind('<Return>', SendMessage)

        self.root.mainloop()


class NamingError(Exception):
    def __init__(self, name, check):
        self.name = name
        self.check = check

    def __str__(self):
        return repr(self.name), repr(self.check)


class GetMessage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.text = ''
        self.list = []

    def run(self):
        while True:
            sleep(0.1)
            try:
                self.text = s.recv(1024).decode('utf-8')
                for i in range((len(self.text)//80)+1):
                    self.list.append((self.text[i*80:(i+1)*80]+'\n'))
                self.list = self.list[-37:len(self.list)]
                self.text = ''
                self.text = self.text.join(str(x) for x in self.list)
            except:
                sleep(0.1)
            chat.set(self.text)


def SendMessage(*args):
    msg = Msg.get()
    if msg:
        text = Name + ': ' + msg
        print('sending: ' + text)
        s.send(text.encode('utf-8'))
        Msg.set('')

def SetName(*args):
    global Name
    s.connect((host, port))
    HndSkMsg = s.recv(1024).decode('utf-8')
    Name = name.get()
    if not Name:
        Name = 'NoName {}'.format(random.randint(0,9999999))
    if HndSkMsg == 'NameTime':
        s.send(Name.encode('utf-8'))
        NR1.Quit()
        check = s.recv(1024).decode('utf-8')
        if Name == check:
            GUI1.start()
            GM1.start()
            s.send(('{} has joined the server'.format(Name)).encode('utf-8'))
        else:
            try:
                raise NamingError(name, check)
            except NamingError as e:
                print(
                    'Naming Error: First value is what was sent to server, Second is what came back. The two must match.\nNames: ' + repr(
                        e.name) + ' & ' + repr(e.check))
                sleep(5)
                print('restarting')
                Main()
        
    else:
        print('An error occurred in handshaking...restarting')
        Main()


def Main():
    NR1.start()


if __name__ == '__main__':
    Name = ''
    chat = ''
    Msg = ''
    #host = "10.107.9.67"
    host = "127.0.0.1"
    port = 5000
    name = ''
    GM1 = GetMessage()
    GUI1 = GUI()
    NR1 = Namer()
    s = socket.socket()
    Main()
