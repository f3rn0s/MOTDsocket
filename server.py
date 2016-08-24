'''
A simple getter server, client connects and recieves a MOTD, then they leave
'''
import socket
import sys
import time
from thread import *
from urllib2 import urlopen

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 31337 # Arbitrary non-privileged port
my_ip = urlopen('http://ip.42.pl/raw').read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.connect(('google.com', 0))

print('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print('Socket now listening on port: ' + str(PORT))
print('Public IP Address: ' + str(my_ip))
print('Private IP Address: ' + str(ss.getsockname()[0]))

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	#conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

	f = open('motd.txt', 'r')
	for line in f:
		conn.send(line)
	f.close()
	conn.close()

while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('User ' + addr[0] + ':' + str(addr[1]) + ' Grabbed information')
    with open("ip.txt", "a") as myfile:
    	myfile.write(str(addr[0]) + '\n')     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()