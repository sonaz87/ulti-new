from tkinter import *
from client import *
from server import *
from threading import Thread

def main():

    root = Tk(className = "Ulti")

    # server_ip = '83.160.108.8'
    # port = 5555


    server_thread = Thread(target = server)
    server_thread.setDaemon(True)

    def serverClick(label):
        label.config(text = 'Szerver fut', fg= '#0f0')
        server_thread.start()

    def clientCkick(nameBox, IpBox):
        name = nameBox.get()
        ip = IpBox.get()
        client_thread = Thread(target=client, args=(name, ip))
        client_thread.setDaemon(True)
        client_thread.start()


    def quit():
        # client_thread.join()
        server_thread.join()
        root.destroy()
        pygame.QUIT
        sys.exit()

    nameBox = Entry(root, width = 10, )
    IPBox = Entry(root, width= 15, )
    nameLabel = Label(root, text = "Név: ")
    IPLabel = Label(root, text= "Szerver IP: ")
    # myLabel = Label(root, text = 'Ulti')
    myLabel2 = Label(root, text= 'Nem fut a szerver', fg= '#f00', font = 'bold')
    myButton = Button(root, text= "Kliens indítása", command = lambda: clientCkick(nameBox, IPBox))
    myButton2 = Button(root, text= 'Szerver indítása', command = lambda: serverClick(myLabel2))
    myButton3 = Button(root, text='Kilépés', command = quit)


    # myLabel.grid(column = 0, row= 0)
    myLabel2.grid(column = 0, row = 1)

    nameLabel.grid(column = 0, row = 2)
    nameBox.grid(column = 1, row = 2)
    IPLabel.grid(column = 0, row = 3)
    IPBox.grid(column = 1, row = 3)

    myButton.grid(column = 0, row = 4)
    myButton2.grid(column = 0, row = 5)
    myButton3.grid(column = 0, row = 6)


    root.mainloop()


if __name__== "__main__":
    main()