from socket import *
from threading import Thread
import threading
import os
import thread
import time
serverPort = 65423
cook_field = 1
para = 0

#********************************************************************************************************#

class Node:                                                     #Class to address details pertaining to a peeer
    def __init__(self, hname, addr, ttl=0, flag=0, cookie=0):
        self.hname = hname
        self.addr = addr
        self.next = None
        self.cookie = 0
        self.ttl = 0
        self.flag = 0

    def getnext(self):
        return self.next

    def setnext(self, newdata):
        self.next = newdata

    def get_hname(self):
        return self.hname

    def get_addr(self):
        return self.addr

    def get_cookie(self):
        return self.cookie

    def get_ttl(self):
        return self.ttl

    def get_flag(self):
        return self.flag

    def set_hname(self, hname):
        self.hname = hname

    def set_addr(self, addr):
        self.addr = addr

    def set_cookie(self):
        global cook_field
        self.cookie = cook_field
        print self.cookie
        cook_field = cook_field + 1

    def set_ttl(self, data):
        self.ttl = data


    def set_flag(self, data):
        self.flag = data


class LinkedList:                                   #To create a linked list of the peers that are connected
    def __init__(self):
        self.head = None
        self.para = 0

    def add(self, hname, addr):                     #To add a peer to the linked list

        if self.head is None:
            newnode = Node(hname, addr)
            newnode.set_flag(1)
            newnode.set_cookie()
            newnode.set_ttl(7200)
            c = newnode.get_cookie()
            thread1 = threading.Thread(target=self.timer, args=(hname, addr))
            thread1.daemon = True
            thread1.start()
            self.head = newnode

            print self.head
            #return newnode.get_cookie()
        else:
            newnode = Node(hname, addr)
            newnode.setnext(self.head)
            newnode.set_flag(1)
            newnode.set_cookie()
            newnode.set_ttl(7200)
            thread1 = threading.Thread(target=self.timer, args=(hname, addr))
            thread1.daemon = True
            thread1.start()
            self.head = newnode



    def search(self, hname, addr):                              #To check whether a client has already been registered
        temp = self.head
        while temp != None:
            if ((temp.hname == hname) and (temp.addr == addr)):
                print 'The host is already registered'
                return hname
            else:
                temp = temp.getnext()
        print 'The client is not registered.Need to registered'
        return 0

    def peer_list(self):                                    #To generate peer list
        temp = self.head
        count = 0
        while temp != None:
            print temp.get_ttl()
            if temp.get_ttl() != 0:
                if count == 0:
                    saveFile = open('peer_list.txt', 'w')
                    text = "%s\t%s\t%d\t%s\n" % (temp.get_hname(), temp.get_addr(), temp.get_cookie(), temp.get_ttl())
                    saveFile.write(text)
                    saveFile.close()
                else:
                    saveFile = open('peer_list.txt', 'a')
                    text = "%s\t%s\t%d\t%s\n" % (temp.get_hname(), temp.get_addr(), temp.get_cookie(), temp.get_ttl())
                    saveFile.write(text)
                    saveFile.close()
                count = count + 1
                temp = temp.getnext()
            else:
                temp = temp.getnext()

    def timer(self, hname, addr):                       #To implement TTl so that a peer can be marked inactive
        temp = Node(hname, addr)
        sec = 0
        while sec != 7200:
            time.sleep(5)
            sec = sec + 5
            number = 7200-sec
            temp.set_ttl(number)
        temp.set_ttl(0)
        temp.set_flag(0)




    def inactive(self, hname, addr):                    #To maunally mark a peer inactive
        Node(hname, addr).set_flag(0)
        print 'The client has been marked inactive and closing the connection'


def client_process(connectionsocket, addr) :            #Thread that handles the connection (connection socket)
    print connectionsocket
    while 1:
        cs = addr[0]
        cport = addr[1]
        sentence = connectionsocket.recv(1024)
        s = sentence.decode('utf-8')
        print s
        method = s[s.index(''):s.index(' P2P/DI-1.1 <cr> <lf>\nHost')]
        port = s[s.index('Port') + 5:s.index(' <cr> <lf>\nCookie')]
        port = int(port)


    # The incoming request details are taken and searched in the nodes. if no match, then the peer has to be registered
        if method == 'Register':
            r = l.search(cs, port)
            if r == 0:
                l.add(cs, port)
                connectionsocket.send("Registered")
            else :
                print 'client is already registered. can directly proceed to pquery'
                connectionsocket.send("Already Registered")

        elif method == 'PQuery':
            l.peer_list()

            with open('peer_list.txt', 'r') as f:
                i = f.readlines()
                f.close()
            with open('For peer.txt', 'w') as fi:
                count = 0
                for line in i:
                    quad = line.split('\t')
                    if quad[0]!= cs:
                        fi.write(line)
                        count = count +1
                if count == 0:
                    fi.write('None')
                fi.close()

            with open('For peer.txt', 'rb') as f:
                send_file = f.read(2048)
                connectionsocket.send(send_file)
                f.close()
        elif method == 'Leave' :
            f = open("peer_list.txt", "r")
            lines = f.readlines()
            f.close()
            f = open("peer_list.txt", 'w')
            for line in lines:
                trip = line.split('\t')
                if trip[0] != cs and "\n":
                    f.write(line)
            f.close()
            connectionsocket.send("bye")
            connectionsocket.close()



if __name__=='__main__':
    serverPort = 65423
    RSserver = socket(AF_INET,SOCK_STREAM)
    RSserver.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    RSserver.bind(('', serverPort))
    RSserver.listen(6)                                  #The welcome socket on which the server listens on
    l = LinkedList()
    print 'The Server is ready to receive'

    while 1:
        cs, addr = RSserver.accept()
        print 'connection accepted from: ', addr
        print 'address', addr[0]
        print 'Socket:', cs

        thread = threading.Thread(target=client_process, args=(cs, addr))
        thread.daemon = True
        thread.start()
