import threading, socket, random
from time import sleep
from tkinter import *
from tkinter import ttk
import re


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
    def Quit(self):
        print('delete gui')
        self.root.destroy()

    def run(self):
        global chat
        global Msg
        print('gui started')
        #threading.Thread.__init__(self)
        print('gui 1')
        self.root = Tk()
        print('gui 2')
        self.root.title('The PyChat')
        self.root.geometry('400x620')
        print('gui got to here 0')
        self.mainframe = ttk.Frame(self.root, padding='3 3 3 3', width=400, height=620)
        self.mainframe.grid(sticky=(N, W, E, S))
        self.mainframe.pack(fill=BOTH, expand=1)
        self.sendframe = ttk.Frame(self.root, relief=RAISED, borderwidth=1)
        self.sendframe.pack(fill=BOTH, expand=0)
        print('gui got to here')
        chat = StringVar()
        Msg = StringVar()
        ttk.Label(self.mainframe, textvariable=chat, anchor='nw',text="Top Left").grid(sticky=(N, W, E, S))
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
                chattext = s.recv(1024).decode('utf-8')
                print(len(chattext))
                for i in range((len(chattext)//70)+1):
                    self.list.append((chattext[i*70:(i+1)*70]+'\n'))
                self.list = self.list[-37:len(self.list)]
                print(len(self.list))
                chattext = ''.join(str(x) for x in self.list)
                chat.set(chattext)
            except:
                sleep(0.1)


def SendMessage(*args):
    msg = Msg.get()
    if msg:
        text = '[{n}]: {m}'.format(n=Name, m=msg)
        if len(text) < 1024:
            print('sending: ' + text)
            s.send(text.encode('utf-8'))
            Msg.set('')
        else: print('message over limit, not sending')

def SetName(*args):
    global Name
    try:
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
            raise ConnectionRefusedError
    except:
        print('An error occurred in handshaking...restarting')
        Main()


def Main():
    NR1.start()


if __name__ == '__main__':

    print('Finding Servers')

    saddr = ('', 42120)

    socket.setdefaulttimeout(5) #5s timeout

    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    UDPSock.bind(saddr)
    data, addr = None, None
    while True:

        try:
            data, addr = UDPSock.recvfrom(1024)
        except:
            print('no server found this try, type \'o\' to enter own ip, or \'y\' to continue searching')
            dat = input()
            if dat == 'o':
                addr = input('ip of server: ')
                break
    
        if data:
            print('Found server {} at {}'.format(data.decode('utf-8'), addr))
            print('type \'y\' to use this server, \'o\' to type in your own address, or nothing to try again!')
            dat = input()

            if dat == 'y':
                break
            if dat == 'o':
                addr = input('ip: ')
                break
    UDPSock.close()
            
    
    socket.setdefaulttimeout(None)
    
    Name = ''
    chat = ''
    Msg = ''
    #host = "10.107.9."
    host = addr[0]
    port = 42120
    name = ''
    GM1 = GetMessage()
    GUI1 = GUI()
    NR1 = Namer()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    Main()

