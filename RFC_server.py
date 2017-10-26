from socket import *
import socket
import os.path
import threading
import glob
from threading import Thread


PserverPort = 65400

PServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
PServer.bind(('', PserverPort))

PServer.listen(6)

print 'The peer server is ready to receive'
listOfFiles = glob.glob('*.pdf')
i = (len(listOfFiles))
saveFile = open('RFC index.txt', 'w')
while i > 0:
    saveFile.write(listOfFiles[i - 1] + '\n')
    i = i - 1
saveFile.close()





def handler(cs, addr):
    while 1:

        command = cs.recv(2048)
        if command == 'RFCindex':
            RFCindex(cs)
        if command == 'Download':
            upload(cs)



def RFCindex(c):

    with open('RFC files.txt', 'rb') as fi:
        data = fi.read(2048)
        print data
        c.send(data)
        fi.close()
def upload(c):
    name = c.recv(1024)
    listOfFiles = glob.glob('rfc8*.pdf')
    i = (len(listOfFiles))
    while i>0:
        if name == listOfFiles[i-1]:
            c.send("Available")
            with open(listOfFiles[i - 1], "rb") as f:
                data = f.read(2048)
                while data:
                    print data[0:20]
                    c.send(data)
                    data = f.read(2048)
                print 'RFC sent'
                #cs.send("gopikl")
                f.close()
        i = i-1
    print 'Files Transfer Complete'

    return

if __name__ == '__main__':

    while 1:
        cs, addr = PServer.accept()
        print ('The peer server accepted connection from :')

        thread = threading.Thread(target=handler, args=(cs, addr))
        thread.daemon = True
        thread.start()









