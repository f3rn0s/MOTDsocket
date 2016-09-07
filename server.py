'''
A simple getter server, client connects and can issue text commands to recieve
files.
'''
import socket
import sys
import time
import os
import datetime
from thread import *
from urllib2 import urlopen

now = datetime.datetime.now()

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 31337 # Arbitrary non-privileged port
TIME = now.strftime('%Y-%m-%d-%H:%M')

LOGFILE = "log-" + TIME + ".txt"

try:
	my_ip = urlopen('http://ip.42.pl/raw').read()
	ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ss.connect(('google.com', 0))
except:
	print("No interent connection")	
	exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
#print('Public IP Address: ' + str(my_ip))
print('Private IP Address: ' + str(ss.getsockname()[0]))


def clearscreen(conn):
	conn.send('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	
	user = addr[0]
	port = str(addr[1])

	conn.send('Welcome to the server, type /motd to get started\n')
        conn.send('Type quit to leave the server at any time\n')
	while True:
		try:
			data = str(conn.recv(1024))
		except:
			conn.send('Input to large')
		
		#User Commands
		
		if data.lower() == '/clear\n':
			clearscreen(conn)
		if data.lower() == '/motd\n':
			conn.send('\n')
			f = open('motd.txt', 'r')
			for line in f:
				conn.send(line)
			f.close()
		if data.lower() == "/login\n":
			conn.send('Any sniffing of this network traffic will show your password in clear text\n')
			conn.send('\nPassword: ')
			try:
				passworddata = str(conn.recv(1024))
			except:
				conn.send('Get out!')
				break
			if passworddata == 'password\n':
				clearscreen(conn)
				conn.send('Goodjob\n')
			else:
				clearscreen(conn)
				conn.send('Incorrect\n')
				with open(LOGFILE, "a") as myfile: 
					myfile.write('Failed login attempt by: ' + user + ':' + port + '\n')
				print('Failed login attempt by: ' + user + ':' + port)
		
		#Temporary solution for opening files
		if data.lower() == "info\n":
			conn.send('\n')
			f = open('info.txt', 'r')
			for line in f:
				conn.send(line)
			f.close()
		if data.lower() == "cyberpatriot\n":
			conn.send('\n')
			f = open('cyberpatriot.txt', 'r')
			for line in f:
				conn.send(line)
			f.close()
		if data.lower() == "quit\n":
			conn.close()
			print('User ' + user + ':' + port + ' disconnected')
			break
while 1: 
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	print('User ' + addr[0] + ':' + str(addr[1]) + ' connected')
	with open(LOGFILE, "a") as myfile:
		myfile.write(str(addr[0]) + '\n')     
	start_new_thread(clientthread ,(conn,))
s.close()
