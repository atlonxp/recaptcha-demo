
# coding: utf-8
#!/usr/bin/python

import socket
import sys
import subprocess
import time

#constants
server_address = ('localhost', 6666) #server address
#mesage format definition
#X[E]
endMark = '[E]'

def msgMapping(msg):
#message as input
#mapping messages to differnt functions
#based on the first 3 characters
    mapper = {
        'R': predict,
        'T': msgEcho,  #testing
    }
    return mapper.get(msg[:1], noDefinition)

#function definitions
def predict(connection, msg):

    print('received request. Start predicting...', file = sys.stderr)
    # Call yolo to find the street sign
    subprocess.call('yolo-street-sign.exe')
    sendMsg = b"D[E]"
    connection.sendall(sendMsg)


def msgEcho(connection, msg):
#send the message back for testing
#connected socket and message are inputs
    print('echo back to the client', file = sys.stderr)
    connection.sendall(b'Please wait for 5 seconds\n')
    time.sleep(5)
    connection.sendall(b'Another 5 seconds\n')
    time.sleep(5)
    connection.sendall(msg[3:] + '\n')

def noDefinition(connection, msg):
#msg not defined; server will send the error message back to client
    print('wrong format. notify the client', file = sys.stderr)
    wrongMsg = b"Wrong format![E]"
    connection.sendall(wrongMsg)


# In[3]:

#create an NET, STREAMing(TCP/IP) socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tells the kernel to reuse a local socket in TIME_WAIT state
#serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

#server address

#bind the socket to a host and a port
print('Starting up on %s port %s' % server_address, file = sys.stderr)
serversocket.bind(server_address)

#Listen for incoming connections
serversocket.listen(1)

# start laoding the weights and configures for prediction


while True:
    # Wait for a connection
    print ('waiting for a connection', file = sys.stderr)
    connection, client_address = serversocket.accept()
    msg = ""
    #connection happens
    try:
        print('connection from %s:%s' % client_address, file = sys.stderr)
        msg += connection.recv(4096).decode()
        if msg.endswith(endMark):
            func = msgMapping(msg)
            func(connection, msg)
            print("'Received '%s'" % msg, file = sys.stderr)
    finally:
        #clean up the connection
        connection.close()




