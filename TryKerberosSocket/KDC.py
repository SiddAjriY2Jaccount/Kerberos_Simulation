import math
import string
import random
import socket

portinfobase = {12345:"KDC", 32344:"Client", 22343:"Server"}
sessionkeys = {'Kca': 3, 'Kct': 4, 'Kts': 5}
alphabet = list(string.ascii_uppercase)
                                         

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
   # establish a connection
   clientsocket,addr = serversocket.accept()

   print("Got a connection from %s" % str(addr))

   msg = 'Thank you for connecting'+ "\r\n"
   clientsocket.send(msg.encode('ascii'))
   clientsocket.close()
