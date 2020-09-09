import sys
from datetime import datetime
import socket

remoteServer = raw_input("Please enter a host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)
print("scanning ...", remoteServerIP)
t1 = datetime.now()
try:
	for port in range(1, 500):
		print("Checking ", port)
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.settimeout(0.1)
		result = sock.connect_ex((remoteServerIP, port))
		if result == 0:
			print("Port		{:d}: Open".format(port))
	sock.close()

except KeyboardInterrupt:
	print("You pressed ctrl+c")
	sys.exit()

except socket.gaierror:
	print('Hostname could not be resolved to IP. Exiting')
	sys.exit()

except socket.error:
	print("couldn't connect to server")
	sys.exit()

t2 = datetime.now()
total = t2 - t1
print("scanning compelte in:", total)
