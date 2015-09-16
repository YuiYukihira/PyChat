import threading, socket
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
        self.nameframe.rowconfigure(0,  weight=1)

        name = StringVar()

        ttk.Button(self.nameframe, text="Confirm name:", command=SetName).grid(column=1, row=1, sticky=(N,W,E, S))
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

        self.mainframe = ttk.Frame(self.root, padding='3 3 3 3')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        chat = StringVar()
        Msg = StringVar()

        ttk.Label(self.mainframe, textvariable=chat).grid(column=1, row=1, sticky=(N, W, E, S))

        ttk.Button(self.mainframe, text="Send Message:", command=SendMessage).grid(column=1, row=2, sticky=(W, E, S))
        Msg_entry = ttk.Entry(self.mainframe, width=20, textvariable=Msg).grid(column=2, row=2, sticky=(W, E, S))

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

    def run(self):
        while True:
            sleep(0.1)
            try:
                self.text += s.recv(1024).decode('utf-8') + '\n'
            except:
                sleep(0.1)
            chat.set(self.text)

def SendMessage(*args):
        text = Name + ': ' + Msg.get()
        print('sending: ' + text)
        s.send(text.encode('utf-8'))
        Msg.set('')

def SetName(*args):
    s.connect((host, port))
    HndSkMsg = s.recv(1024).decode('utf-8')
    Name = name.get()
    if HndSkMsg == 'NameTime':
        s.send(Name.encode('utf-8'))
        NR1.Quit()
        check = s.recv(1024).decode('utf-8')
        if Name == check:
            GUI1.start()
            GM1.start()
        else:
            try:
                raise NamingError(name, check)
            except NamingError as e:
                print('Naming Error: First value is what was sent to server, Second is what came back. The two must match.\nNames: ' + repr(e.name) + ' & ' + repr(e.check))
                sleep(5)
                print('restarting')
                Main()
    else:
        print('An error occured in handshaking...restarting')
        Main()

 
                   
def Main():
    NR1.start()

if __name__ == '__main__':
    Name = ''
    chat = ''
    Msg = ''
    host = "192.168.1.66"
    port = 5000
    name = ''
    GM1 = GetMessage()
    GUI1 = GUI()
    NR1 = Namer()
    s = socket.socket()
    Main()
