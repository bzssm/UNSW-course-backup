import ctypes
import sys
import threading
import socket
import time

LOCALHOST = '127.0.0.1'


def ping():
    global currentPeer, succ1, succ2, pred1, pred2, deadPeer
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    sock.bind((LOCALHOST, peer2port(currentPeer)))

    lastPingTime = 0
    seq = 0
    succ1Ack = 0
    succ2Ack = 0
    succ1Dead = False
    succ2Dead = False

    while True:
        if time.time() - lastPingTime > 1.0:
            if succ1 != 'Dead':
                sendPingMessage(seq, currentPeer, LOCALHOST, peer2port(succ1), 'request')
            if succ2 != 'Dead':
                sendPingMessage(seq, currentPeer, LOCALHOST, peer2port(succ2), 'request')
            lastPingTime = time.time()
            seq += 1

        if succ1Dead and succ1 != 'Dead':
            succ1Ack = seq
            succ1Dead = False
        if succ2Dead and succ2 != 'Dead':
            succ2Ack = seq
            succ2Dead = False

        if succ1 != 'Dead' and seq - succ1Ack >= 8:  # set how many missed ack can decide a dead peer
            print(f'Peer {succ1} is no longer alive.')
            succ1 = 'Dead'
            deadPeer = succ1
            succ1Dead = True
            sendTCPMessage('prompt', currentPeer, LOCALHOST, peer2port(succ2), 'querySucc', succ1=0, succ2=0)
        if succ2 != 'Dead' and seq - succ2Ack >= 8:  # set how many missed ack can decide a dead peer
            print(f'Peer {succ2} is no longer alive.')
            succ2 = 'Dead'
            deadPeer = succ2
            succ2Dead = True
            sendTCPMessage('prompt', currentPeer, LOCALHOST, peer2port(succ1), 'querySucc', succ1=0, succ2=0)

        try:
            message, addr = sock.recvfrom(1024)
            sender, seqRecv, messageType = message.decode().split(',')

            if messageType == 'request':
                print(f'A ping request message was received from Peer {sender}.')
                if all([pred1 != -1, pred2 != -1, sender != pred1, sender != pred2]):
                    pred1 = -1
                    pred2 = -1
                if pred1 == -1:
                    pred1 = sender
                elif pred2 == -1:
                    pred2 = sender if sender != pred1 else -1

                sendPingMessage(seqRecv, currentPeer, LOCALHOST, peer2port(sender), 'response')

            else:
                if int(sender) == succ1:
                    succ1Ack = int(seqRecv)
                elif int(sender) == succ2:
                    succ2Ack = int(seqRecv)
                print(f'A ping response message was received from Peer {sender}.')
        except Exception:
            continue


def TCP():
    global currentPeer, succ1, succ2, pred1, pred2, deadPeer, threadTCP, threadPing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.settimeout(1.0)
    sock.bind((LOCALHOST, peer2port(currentPeer)))
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
                        succ1, succ2 = int(newSucc1), int(newSucc2) if int(sender) == succ1 else int(sender), int(
                            newSucc1)
                        print(f'Peer {sender} will depart from the network.')
                        print(f'My first successor is now peer {succ1}.')
                        print(f'My second successor is now peer {succ2}.')
                    elif message.split(',')[1] == 'querySucc':
                        sendTCPMessage('prompt', currentPeer, LOCALHOST, peer2port(sender), 'querySuccResponse',
                                       succ1=succ1, succ2=succ2)
                    elif message.split(',')[1] == 'querySuccResponse':
                        newSucc1, newSucc2 = message.split(',')[3:5]
                        if succ1 == 'Dead':
                            succ1, succ2 = int(succ2), int(newSucc1)
                        elif succ2 == 'Dead':
                            succ2 = int(newSucc2) if newSucc1 == str(deadPeer) or newSucc1 == 'Dead' else int(newSucc1)
                        print('succ1 = ', succ1, 'succ2 = ', succ2)
                    print(f'My first successor is now peer {succ1}.')
                    print(f'My second successor is now peer {succ2}.')
                elif message.split(',')[0] == 'file':
                    if message.split(',')[1] == 'Next':
                        sendTCPMessage('file', currentPeer, LOCALHOST, peer2port(sender), 'Here',
                                       fileName=message.split(',')[3], originalPeer=message.split(',')[4])
                        print(f'File {message.split(",")[3]} is here.')
                        print(f'A response message, destined for peer {message.split(",")[4]}, has been sent.')
                    elif message.split(',')[1] == 'Here':
                        print(
                            f'Received a response message from peer {sender}, which has the file {message.split(",")[3]}.')
                    elif message.split(',')[1] == 'Unknown':
                        fileP = filePosition(message.split(",")[3], currentPeer, succ1)
                        if fileP == 'Here':
                            sendTCPMessage('file', currentPeer, LOCALHOST, peer2port(succ1), fileP,
                                           fileName=message.split(',')[3], originalPeer=message.split(',')[4])

                            print(f'File {message.split(",")[3]} is here.')
                            continue
                        elif fileP == 'Next':
                            sendTCPMessage('file', currentPeer, LOCALHOST, peer2port(succ1), fileP,
                                           fileName=message.split(',')[3], originalPeer=message.split(',')[4])

                            print(f'File {message.split(",")[3]} is not stored here.')
                            print(f'File request message has been forwarded to my successor.')
                        elif not fileP:
                            sendTCPMessage('file', currentPeer, LOCALHOST, peer2port(succ1), 'Unknown',
                                           fileName=message.split(',')[3], originalPeer=message.split(',')[4])

                            print(f'File {message.split(",")[3]} is not stored here.')
                            print(f'File request message has been forwarded to my successor.')
                elif message.split(',')[0] == 'command':
                    if message.split(',')[1] == 'quit':
                        print(f'This is Peer {currentPeer}. Leaving from the CDHT...')
                        terminate_thread(threadPing)
                        terminate_thread(threadTCP)
                        time.sleep(1)
                    elif message.split(',')[1] == 'request':
                        fileName = int(message.split(',')[2])
                        fileP = filePosition(fileName, currentPeer, succ1)
                        if fileP == 'Here':
                            print(f'File {fileName} is here.')
                            continue
                        elif fileP == 'Next':
                            sendTCPMessage('file', currentPeer, LOCALHOST, peer2port(succ1), fileP, fileName=fileName,
                                           originalPeer=currentPeer)
                        elif not fileP:
                            sendTCPMessage('file', int(sender), LOCALHOST, peer2port(succ1), 'Unknown',
                                           fileName=fileName, originalPeer=currentPeer)
                        print(f'File {fileName} is not stored here.')
                        print('File request message has been forwarded to mu successor.')

            connectionSocket.close()
        except Exception:
            raise
            continue


def peer2port(peer):
    if peer == 'Dead':
        return 60000
    return 50000 + int(peer)


def terminate_thread(thread):
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


def sendPingMessage(seq, source, IP, port, status):
    message = f'{source},{seq},{status}'
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        sock.sendto(bytes(message, encoding='utf-8'), (IP, port))
    except Exception:
        pass


def sendTCPMessage(messageType, source, IP, port, status, succ1=None, succ2=None, fileName=None, originalPeer=None):
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


# def sendPromptMessage(source, succ1, succ2, IP, port, status):
#     message = f'prompt,{status},{source},{succ1},{succ2}'
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.connect((IP,port))
#         sock.send(message.encode())
#     except Exception:
#         pass
#     finally:
#         sock.close()


def filePosition(fileName, myPeer, succ1):
    fileHash = int(fileName) % 256
    if fileHash == myPeer:
        return 'Here'
    if succ1 < myPeer:
        if myPeer < fileHash <= 255 or 0 <= fileHash <= succ1:
            return 'Next'
    if myPeer < fileHash <= succ1:
        return 'Next'
    return False


# def sendFileMessage(fileName, source, IP, port, status):
#     message = f'file,{status},{source},{fileName}'
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.connect((IP,port))
#         sock.send(message.encode())
#     except Exception:
#         pass
#     finally:
#         sock.close()


def init():
    global currentPeer, succ1, succ2, pred1, pred2, threadTCP, threadPing
    currentPeer = int(sys.argv[1])
    succ1 = int(sys.argv[2])
    succ2 = int(sys.argv[3])
    pred1 = -1
    pred2 = -1

    threadPing = threading.Thread(target=ping)

    threadTCP = threading.Thread(target=TCP)

    threadPing.start()

    threadTCP.start()

    # while True:
    #     command = input('Please input command: ')
    #
    #     if command == 'quit':
    #         sendPromptMessage(currentPeer, succ1, succ2, LOCALHOST, peer2port(pred1), 'quit')
    #         sendPromptMessage(currentPeer, succ1, succ2, LOCALHOST, peer2port(pred2), 'quit')
    #
    #         # Ways to kill a thread?? Or just leave...
    #         sys.exit()
    #         # killThread(threadPing)
    #         # killThread(threadTCP)
    #
    #         print(f'This is Peer {currentPeer}. Leaving from the CDHT...')
    #         time.sleep(1)
    #         break
    #     elif command.startswith('request'):
    #         try:
    #             print(int(command.split(' ')[1]))
    #             fileName = int(command.split(' ')[1])
    #
    #
    #             if any([fileName < 0, fileName > 9999, len(command.split()[1]) != 4]):
    #                 raise ValueError
    #         except Exception:
    #             print('Wrong file ...')
    #             continue
    #
    #         fileP = filePosition(fileName, currentPeer, succ1)
    #         if fileP == 'Here':
    #             print(f'File {fileName} is here.')
    #             continue
    #         elif fileP == 'Next':
    #             sendFileMessage(fileName, currentPeer, LOCALHOST, peer2port(succ1), fileP)
    #         elif not fileP:
    #             sendFileMessage(fileName, currentPeer, LOCALHOST, peer2port(succ1), 'Unknown')
    #         print(f'File {fileName} is not stored here.')
    #         print('File request message has been forwarded to mu successor.')
    #     else:
    #         print('Wrong command...')


if __name__ == '__main__':
    init()
