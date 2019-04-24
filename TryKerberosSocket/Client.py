import math
import string
import random
import socket

portinfobase = {12345:"KDC", 32344:"Client", 22343:"Server"}
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #default protocol TCP
port = 12345
s.bind(('', port))
print("Socket binded to ",str(port),str(portinfobase[port]))
'''
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# connection to hostname on the port.
s.connect((host, port))

# Receive no more than 1024 bytes
msg = s.recv(1024)

s.close()
print (msg.decode('ascii'))

'''
sessionkeys = {'Kca': 3, 'Kct': 4, 'Kts': 5}
alphabet = list(string.ascii_uppercase)





def decrypt(text,s):
    result=""
    #s represents shift order, s=3 for Caesar cipher
    for x in text:
        if x in alphabet:
            result += chr((ord(x) - s - 65) % 26 + 65)
        else:
            result += x
    return result


#function to generate ciphertext
def encrypt(text,s):
    result=""
    #s represents shift order, s=3 for Caesar cipher
    for x in text:
        if x in alphabet:
            result += chr((ord(x) + s - 65) % 26 + 65)
        else:
            result += x
    return result









'''
