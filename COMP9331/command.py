# Written by Fengting YANG for COMP9331 Assignment
# zID: z5089358
# python version: 3.6.4
# This program is to send command to peers
# Usage: <peerNumber> <command>[quit|request] <filename>

import socket

LOCALHOST = '127.0.0.1'


def sendCommand():
    while True:
        command = input(
            '[Format: <peer> <command>[quit|request] <filename>(Ignore this para when command is quit)].\npls input a command: ')
        peer, commandType = command.split()[0:2]
        if commandType == 'quit':
            commandArgs = ''
        elif commandType == 'request':
            commandArgs = command.split()[2]
        else:
            print('Wrong command ...')
            continue
        try:
            print(f'{commandType},{commandArgs}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((LOCALHOST, 50000 + int(peer)))
            sock.send(f'command,{commandType},{commandArgs}'.encode())
        except Exception:
            raise
            continue
        finally:
            sock.close()


if __name__ == '__main__':
    sendCommand()
