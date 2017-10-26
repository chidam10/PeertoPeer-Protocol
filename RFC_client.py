from socket import *
import socket
import os
import glob

PserverPort = 65400

f = open('Cookie.txt', 'w')
f.write('-1000')
f.close()                                   


listOfFiles = glob.glob('rfc8*.pdf')
i = (len(listOfFiles))
saveFile = open('RFC from peer.txt', 'w')
while i > 0:
    saveFile.write(listOfFiles[i - 1] + '\t' + socket.gethostbyname(socket.getfqdn()) + '\t' + str(PserverPort) + '\t'+'\n')
    i = i - 1
saveFile.close()

def RS_module():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    number = input('what do you want:\n Press 1 to register\n Press 2 to PQuery\n Press 3 to leave the connection\n Press 4 to return to previoues menu:')

    while number != 4:

        print('', number)
        if number == 1:
            print (number)
            clientSocket.connect(('192.168.1.7', 65423))
            messageType = 'Register'
            hostname = 'My machine'
            fj = open('Cookie.txt', 'r')
            cookie = fj.read(1024)
            fj.close()

            sentence = '' + messageType + ' P2P/DI-1.1 <cr> <lf>\nHost ' + hostname + ' <cr> <lf>\nPort ' + str(
                PserverPort) + ' <cr> <lf>\nCookie ' + str(cookie) + ' <cr> <lf>\n<cr> <lf>'

            print(sentence.encode('utf-8'))
            clientSocket.send(sentence.encode('ascii'))
            data = clientSocket.recv(2048)

            if data == 'Registered':
                print 'Client successfully registered'

            else :
                print 'Client already registered. Proceed to PQuery'


        elif number == 2:
            messageType = 'PQuery'
            hostname = 'My machine'
            fi = open('Cookie.txt', 'r')
            cookie = fi.read(1024)
            fi.close()
            sentence = '' + messageType + ' P2P/DI-1.1 <cr> <lf>\nHost ' + hostname + ' <cr> <lf>\nPort ' + str(
                PserverPort) + ' <cr> <lf>\nCookie ' + 'str(cookie)' + ' <cr> <lf>\n<cr> <lf>'

            print (sentence.encode('utf-8'))
            clientSocket.send(sentence.encode('ascii'))

            f = open('RS_peer_list.txt', 'wb')
            data = clientSocket.recv(2048)
            f.write(data)
            f.close()
            print 'Peer List downloaded'

            f = open('RS_peer_list.txt', 'r')
            i = f.readlines()
            j=len(i)
            print j

            for line in i:
                quad = line.split('\t')
                print socket.gethostbyname(socket.getfqdn())
                if quad[0] == socket.gethostbyname(socket.getfqdn()):
                    s = open('Cookie.txt', 'w')
                    s.write(quad[2])
                    s.close()
            f.close()
        elif number == 3:
            messageType = 'Leave'
            hostname = 'My machine'
            fi = open('Cookie.txt', 'r')
            cookie = fi.read(1024)
            fi.close()
            sentence = '' + messageType + ' P2P/DI-1.1 <cr> <lf>\nHost ' + hostname + ' <cr> <lf>\nPort ' + str(
                PserverPort) + ' <cr> <lf>\nCookie ' + str(cookie) + ' <cr> <lf>\n<cr> <lf>'

            print 'Exiting....................'
            print(sentence.encode('utf-8'))
            clientSocket.send(sentence.encode('ascii'))
            clientSocket.recv(1024)
            clientSocket.close()
            return
        number = input('what do you want:\n Press 1 to register\n Press 2 to PQuery\n Press 3 to leave the connection\n Press 4 to return to previoues menu:')


def Peer_module():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    while 1:

        sel = input('Press 1 to Query the RFC index of the peers\nPress 2 to download the RFC files\nPress 3 to exit: ')
        while sel != 3:
            if sel == 1:

                with open('RFC_peer_list.txt', 'r') as f:
                    i = f.readlines()
                    print i

                    for line in i :
                        if line != "\n":
                            print "line" + line
                            tup = line.split('\t')
                            peerName = tup[0]
                            print peerName
                            peerServer = tup[1]
                            print peerServer
                            if peerName != socket.gethostbyname(socket.getfqdn()):
                                RFC_index(peerName, peerServer)
                                print 'going to next line'
                        else:
                            return

            elif sel == 2:
                name = raw_input('Enter the name of file to be downloaded:\n')
                print name
                with open('RFC from peer.txt', 'r') as f:
                    print 'opened RFC from peer'
                    lines = f.readlines()
                    print lines
                    for line in lines:
                        print line[0:11]
                        if line[0:11]==name:
                            trip = line.split('\t')
                            print trip
                            if trip[1] != socket.gethostbyname(socket.getfqdn()):
                                RFC_download(name, trip[1], trip[2])
            sel = input('Press 1 to Query the RFC index of the peers\nPress 2 to download the RFC files\nPress 3 to exit: ')
        return


def RFC_index(peerName, peerServer):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print ('Establishing connection with peer:'+ peerName)
    clientSocket.connect((peerName, int(peerServer)))
    clientSocket.send("RFCindex")
    print 'RFCindex sent'
    with open('RFC2.txt', 'w') as f:
        data = clientSocket.recv(2048)
        f.write(data)
        f.close()
    with open('RFC2.txt', 'r') as fj:
        i = fj.readlines()
        print i
        fj.close()
    with open('RFC from peer.txt', 'w') as fi:
        for line in i:
            print line
            if line != '':
                tup = line.split('\n')
                print tup[0]
                fi.write(tup[0] + '\t' + peerName + '\t' + str(PserverPort) + '\t'+'\n')
        fi.close()

    clientSocket.close()


def RFC_download(name, Pname, Pport):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print ('Establishing connection with peer:' + Pname)
    clientSocket.connect((Pname, int(Pport)))
    print 'client connected'
    clientSocket.send("Download")
    print 'sent the download command'
    clientSocket.send(name)
    status = clientSocket.recv(1024)
    print status
    if status == "Available":
        data = clientSocket.recv(2048)
        fi = open(name, "wb")
        print data[0:20]
        while "gopikl" not in data:
            fi.write(data)
            print data[0:20]
            data = clientSocket.recv(2048)
        fi.write(data[:-6])
        fi.close()
        print 'RFC downloaded'
    else:
        print 'Requested file not available at the server'












if __name__ == '__main__':

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    while 1:
        selection = input('Press 1 to contact RS Server\n      2 to communicate with other peers:' )
        if selection == 1:
            RS_module()
        elif selection == 2:
            Peer_module()


    clientSocket.close()
