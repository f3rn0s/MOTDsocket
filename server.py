'''
A simple getter server, client connects and can issue text commands to recieve files.
'''
import socket
import sys
import time
import os
import datetime
from thread import *
from urllib2 import urlopen

HOST = ''   # Symbolic name meaning all available interfaces
while 1:
	try:
		PORT = int(raw_input("Port: ")) # Arbitrary non-privileged port
		if PORT <= 65535:	
			break
		else:
			print("Enter a valid port please (1-65535)")
	except KeyboardInterrupt:
		print('\n')
		quit()
	except:
		print("Enter a valid port please (1-65535)")

def makedir(foldername):
	if not os.path.exists(foldername):
		os.makedirs(foldername)


#Creates directories
makedir('logs')
makedir('private')
makedir('public')

#Creates log file with time
now = datetime.datetime.now()
TIME = now.strftime('%Y-%m-%d-%H:%M')
LOGFILE = "logs/log-" + TIME + ".txt"

#Attempts to create all sockets
try:
	my_ip = urlopen('http://ip.42.pl/raw').read()
	ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ss.connect(('google.com', 0))
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
	print("No interent connection")	
	exit()

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

#Gives information about serveri
print('Socket now listening on port: ' + str(PORT))
print('Public IP Address: ' + str(my_ip))
print('Private IP Address: ' + str(ss.getsockname()[0]))

#Some useful functions
def clearscreen(conn):
	conn.send('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	conn.send('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

def ignore():
	ignore = 'ignore'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	
	#stores relevant information about connection
	user = addr[0]
	port = str(addr[1])

	#Welcomes user to the server
	conn.send('#Welcome to the server, type /motd to get started\n')
        conn.send('#Type quit to leave the server at any time\n')
	
	#Places user in a loop until disconnect
	while True:
		try:
			data = str(conn.recv(1024))
		except:
			conn.send('Input to large')
		
		#User Commands
		
		if data.lower() == '/clear\n':
			clearscreen(conn)
		elif data.lower() == '/motd\n':
			conn.send('\n')
			try:
				f = open('motd.info', 'r')
				for line in f:
					conn.send(line)
				f.close()
			except:
				conn.send('server is missing a motd.info file\n')
		elif data.lower() == "/login\n":
			conn.send('Any sniffing of this network traffic will show your password in clear text\n')
			conn.send('\nPassword: ')
			try:
				passworddata = str(conn.recv(1024))
			except:
				conn.send('Get out!')
				break
			if passworddata == 'password\n':
				clearscreen(conn)
				conn.send('Goodjob, you can now access authorised only files\n')
				conn.send('Make sure to type quit before leaving!')
				while 1:
					securedata = str(conn.recv(1024))
					if securedata.lower() == "quit\n" or securedata.lower() == "/quit\n":
						break
					else:
						try:
							f = open("private/" + (securedata.lower()).rstrip() + ".txt", 'r')
							for line in f:
								conn.send(line)
							f.close()
						except:
							conn.send("File does not exist\n")
			else:
				clearscreen(conn)
				conn.send('Incorrect\n')
				with open(LOGFILE, "a") as myfile: 
					myfile.write('Failed login attempt by: ' + user + ':' + port + '\n')
				print('Failed login attempt by: ' + user + ':' + port)
                elif data.lower() == "quit\n" or data.lower() == "/quit\n":
                        conn.close()
                        print('User ' + user + ':' + port + ' disconnected')
                        break
                elif data.lower() == "client\n" or data.lower() == "/client\n":
                	try:
                		f = open("client.py", 'r')
                		for line in f:
                			conn.send(line)
                		f.close
                	except:
                		conn.send("Server is missing a client")
		#Solution for opening files
		else:
			try:
				f = open("public/" + (data.lower()).rstrip() + ".txt", 'r')
				for line in f:
					conn.send(line)
				f.close()
			except:
				ignore()

try:
	while 1: 
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
		print('User ' + addr[0] + ':' + str(addr[1]) + ' connected')
		with open(LOGFILE, "a") as myfile:
			myfile.write(str(addr[0]) + '\n')     
		start_new_thread(clientthread ,(conn,))

except KeyboardInterrupt:
	print('\nLog written to ' + str(LOGFILE))
	print('Have a nice day')
except:
	ignore()

s.close()
