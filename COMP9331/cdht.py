# Written by Fengting YANG for COMP9331 Assignment
# zID: z5089358
# python version: 3.6.4
# method killThread is copied from stackoverflow
# it is the only way i can find to really kill a thread in python...
# This program does not accept any inputs
# To send a command to this program, please use command.py (also run in python 3.6.4)



import ctypes
import sys
import threading
import socket
import time

LOCALHOST = '127.0.0.1'


class CDHT():
    def __init__(self, currentPeer, succ1, succ2):

        self.currentPeer = currentPeer
        self.succ1 = succ1
        self.succ2 = succ2
        self.pred1 = -1
        self.pred2 = -1

        self.threadPing = threading.Thread(target=self.ping)
        self.threadTCP = threading.Thread(target=self.TCP)

        self.threadPing.start()
        self.threadTCP.start()

    def peer2port(self, peer):
        if peer == 'Dead':
            return 60000
        return 50000 + int(peer)

    def ping(self):
        global deadPeer
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)  # set time out
        sock.bind((LOCALHOST, self.peer2port(self.currentPeer)))

        lastPingTime = 0
        seq = 0
        succ1Ack = 0
        succ2Ack = 0
        succ1Dead = False
        succ2Dead = False

        while True:
            if time.time() - lastPingTime > 2.0:  # set ping interval（ping frequency)
                if self.succ1 != 'Dead':
                    self.sendPingMessage(seq, self.currentPeer, LOCALHOST, self.peer2port(self.succ1), 'request')
                if self.succ2 != 'Dead':
                    self.sendPingMessage(seq, self.currentPeer, LOCALHOST, self.peer2port(self.succ2), 'request')

                lastPingTime = time.time()
                seq += 1

            if succ1Dead and self.succ1 != 'Dead':
                succ1Ack = seq
                succ1Dead = False
            if succ2Dead and self.succ2 != 'Dead':
                succ2Ack = seq
                succ2Dead = False

            if self.succ1 != 'Dead' and seq - succ1Ack >= 5:  # set how many missed ack can decide a dead peer
                print(f'Peer {self.succ1} is no longer alive.')
                deadPeer = self.succ1
                self.succ1 = 'Dead'
                succ1Dead = True
                self.sendTCPMessage('prompt', self.currentPeer, LOCALHOST, self.peer2port(self.succ2), 'querySucc',
                                    succ1=0, succ2=0)
            if self.succ2 != 'Dead' and seq - succ2Ack >= 5:  # set how many missed ack can decide a dead peer
                print(f'Peer {self.succ2} is no longer alive.')
                deadPeer = self.succ2
                self.succ2 = 'Dead'
                succ2Dead = True
                self.sendTCPMessage('prompt', self.currentPeer, LOCALHOST, self.peer2port(self.succ1), 'querySucc',
                                    succ1=0, succ2=0)

            try:
                message, addr = sock.recvfrom(1024)
                sender, seqRecv, messageType = message.decode().split(',')

                if messageType == 'request':
                    print(f'A ping request message was received from Peer {sender}.')
                    if all([self.pred1 != -1, self.pred2 != -1, sender != self.pred1, sender != self.pred2]):
                        self.pred1 = -1
                        self.pred2 = -1
                    if self.pred1 == -1:
                        self.pred1 = sender
                    elif self.pred2 == -1:
                        self.pred2 = sender if sender != self.pred1 else -1

                    self.sendPingMessage(seqRecv, self.currentPeer, LOCALHOST, self.peer2port(sender), 'response')

                else:
                    if int(sender) == self.succ1:
                        succ1Ack = int(seqRecv)
                    elif int(sender) == self.succ2:
                        succ2Ack = int(seqRecv)
                    print(f'A ping response message was received from Peer {sender}.')
            except Exception:
                continue

    def TCP(self):
        global deadPeer
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.settimeout(1.0)
        sock.bind((LOCALHOST, self.peer2port(self.currentPeer)))
        sock.listen(1)

        while True:
            try:
                connectionSocket, addr = sock.accept()
                while True:
                    message = connectionSocket.recv(1024)
                    if not message:
                        break
                    sender = message.decode().split(',')[2]
                    message = message.decode()

                    if message.split(',')[0] == 'prompt':
                        if message.split(',')[1] == 'quit':
                            newSucc1, newSucc2 = message.split(',')[3:5]

                            if int(sender) == self.succ1:
                                self.succ1, self.succ2 = int(newSucc1), int(newSucc2)
                            elif int(sender) == self.succ2:
                                self.succ1, self.succ2 = self.succ1, int(newSucc1)

                            print(f'Peer {sender} will depart from the network.')
                            print(f'My first successor is now peer {self.succ1}.')
                            print(f'My second successor is now peer {self.succ2}.')
                        elif message.split(',')[1] == 'querySucc':
                            self.sendTCPMessage('prompt', self.currentPeer, LOCALHOST, self.peer2port(sender),
                                                'querySuccResponse',
                                                succ1=self.succ1, succ2=self.succ2)
                        elif message.split(',')[1] == 'querySuccResponse':
                            newSucc1, newSucc2 = message.split(',')[3:5]
                            if self.succ1 == 'Dead':
                                self.succ1, self.succ2 = int(self.succ2), int(newSucc1)
                            elif self.succ2 == 'Dead':
                                if newSucc1 == str(deadPeer) or newSucc1 == 'Dead':
                                    self.succ2 = int(newSucc2)
                                else :
                                    self.succ2 =int(newSucc1)
                            if self.succ1 == 'Dead' or self.succ2 == 'Dead':
                                continue
                            print(f'My first successor is now peer {self.succ1}.')
                            print(f'My second successor is now peer {self.succ2}.')
                    elif message.split(',')[0] == 'file':
                        if message.split(',')[1] == 'Next':
                            self.sendTCPMessage('file', self.currentPeer, LOCALHOST,
                                                self.peer2port(message.split(",")[4]), 'Here',
                                                fileName=message.split(',')[3], originalPeer=message.split(',')[4])
                            print(f'File {message.split(",")[3]} is here.')
                            print(f'A response message, destined for peer {message.split(",")[4]}, has been sent.')
                        elif message.split(',')[1] == 'Here':
                            print(
                                f'Received a response message from peer {sender}, which has the file {message.split(",")[3]}.')
                        elif message.split(',')[1] == 'Unknown':
                            fileP = self.filePosition(message.split(",")[3], self.currentPeer, self.succ1)
                            if fileP == 'Here':
                                sendTCPMessage('file', self.currentPeer, LOCALHOST,
                                               self.peer2port(message.split(',')[4]), fileP,
                                               fileName=message.split(',')[3], originalPeer=message.split(',')[4])

                                print(f'File {message.split(",")[3]} is here.')
                                continue
                            elif fileP == 'Next':
                                self.sendTCPMessage('file', self.currentPeer, LOCALHOST, self.peer2port(self.succ1),
                                                    fileP,
                                                    fileName=message.split(',')[3], originalPeer=message.split(',')[4])

                                print(f'File {message.split(",")[3]} is not stored here.')
                                print(f'File request message has been forwarded to my successor.')
                            elif not fileP:
                                self.sendTCPMessage('file', self.currentPeer, LOCALHOST, self.peer2port(self.succ1),
                                                    'Unknown',
                                                    fileName=message.split(',')[3], originalPeer=message.split(',')[4])

                                print(f'File {message.split(",")[3]} is not stored here.')
                                print(f'File request message has been forwarded to my successor.')
                    elif message.split(',')[0] == 'command':
                        if message.split(',')[1] == 'quit':
                            print(f'Peer {self.currentPeer} will depart from the network.')
                            self.sendTCPMessage('prompt', self.currentPeer, LOCALHOST, self.peer2port(self.pred1),
                                                'quit',
                                                succ1=self.succ1, succ2=self.succ2)
                            self.sendTCPMessage('prompt', self.currentPeer, LOCALHOST, self.peer2port(self.pred2),
                                                'quit',
                                                succ1=self.succ1, succ2=self.succ2)
                            self.killThread(self.threadPing)
                            self.killThread(self.threadTCP)
                            time.sleep(1)
                        elif message.split(',')[1] == 'request':
                            try:
                                fileNameString = message.split(',')[2]
                                fileName = int(message.split(',')[2])
                                if any([fileName < 0, fileName > 9999, len(message.split(',')[2]) != 4]):
                                    raise ValueError('Wrong file...')
                            except ValueError:
                                print('Wrong file...')
                                continue
                            fileP = self.filePosition(fileName, self.currentPeer, self.succ1)
                            if fileP == 'Here':
                                print(f'File {fileNameString} is here.')
                                continue
                            elif fileP == 'Next':
                                self.sendTCPMessage('file', self.currentPeer, LOCALHOST, self.peer2port(self.succ1),
                                                    fileP,
                                                    fileName=fileNameString,
                                                    originalPeer=self.currentPeer)
                            elif not fileP:
                                self.sendTCPMessage('file', int(sender), LOCALHOST, self.peer2port(self.succ1),
                                                    'Unknown',
                                                    fileName=fileNameString, originalPeer=self.currentPeer)
                            print(f'File {fileNameString} is not stored here.')
                            print('File request message has been forwarded to my successor.')

                connectionSocket.close()
            except Exception:
                raise
                continue

    # This method is the only useful way which is really kill a thread in python.
    # Copy from stackoverflow.
    # Don't know why other method like 'sys.exit()' looks like to kill a method but it is actually still running...
    def killThread(self, thread):
        if not thread.isAlive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def sendPingMessage(self, seq, source, IP, port, status):
        message = f'{source},{seq},{status}'
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1.0)
            sock.sendto(bytes(message, encoding='utf-8'), (IP, port))
        except Exception:
            pass

    def sendTCPMessage(self, messageType, source, IP, port, status, succ1=None, succ2=None, fileName=None,
                       originalPeer=None):
        if messageType == 'prompt':
            message = f'prompt,{status},{source},{succ1},{succ2}'
        elif messageType == 'file':
            message = f'file,{status},{source},{fileName},{originalPeer}'

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, port))
            sock.send(message.encode())
        except Exception:
            pass
        finally:
            sock.close()

    def filePosition(self, fileName, myPeer, succ1):
        fileHash = int(fileName) % 256
        if fileHash == myPeer:
            return 'Here'
        if succ1 < myPeer:
            if myPeer < fileHash <= 255 or 0 <= fileHash <= succ1:
                return 'Next'
        if myPeer < fileHash <= succ1:
            return 'Next'
        return False


if __name__ == '__main__':
    instance = CDHT(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
