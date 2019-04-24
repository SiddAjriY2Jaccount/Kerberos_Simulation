import math
import string
import random
import time
import sys

alphabet = list(string.ascii_uppercase)
numbers = list('123456789')

sessionkeys = {'Kca': 3, 'Kct': 4, 'Kts': 5}

def decrypt(text,s):
    result=""
    #s represents shift order, s=3 for Caesar cipher
    for x in text:
        if x in alphabet:
            result += chr((ord(x) - s - 65) % 26 + 65)
        elif x in numbers:
            result += str((int(x) - s)%10)
        else:
            result += x
    return result


#function to generate ciphertext
def encrypt(text,s):
    result=""
    #s represents shift order, s=3 for Caesar cipher
    for x in text:
        if x in alphabet:
            result += chr((ord(x) + s-65) % 26 + 65)
        elif x in numbers:
            result += str((int(x) + s)%10)
        else:
            result += x
    return result


class Client:
    def __init__(self,id,psswd):
        self.id = id
        self.password= psswd

    def initiate(self, kdc):
        global sessionkeys
        print("INITITATING Kerberos...")
        ix = encrypt(self.password,sessionkeys['Kca'])
        print(ix)
        enc_password = ix
        self.tgt= str(kdc.authenticate(self.id, enc_password))
        if self.tgt == 'None':
            time.sleep(2)
            print("Incorrect Password - Auth. Failed")
            sys.exit()
        print("\n TGT is ", self.tgt)

    def requestTicket(self, kdc, server):
        global seesionkeys
        print("REQUESTING TGS for Ticket...")
        self.nonce1 = random.randint(1,9)
        toenc = self.tgt + str(self.id) + str(self.nonce1)
        iy = encrypt(toenc, sessionkeys['Kct'])
        print(iy)
        enc_tgt = iy
        self.Kcs_enc_Kct, self.Kcs_enc_Kts, self.tempstr1, self.tempstr2 = kdc.grantTicket(enc_tgt, self.id, self.nonce1)
        print("GOT Kcs\n")
        print(self.Kcs_enc_Kct, self.Kcs_enc_Kts)
        array1 = (self.tempstr1).split("|")
        self.Kcs = int(decrypt(self.Kcs_enc_Kct, sessionkeys['Kct']))
        sessionkeys['Kcs'] = self.Kcs
        print(sessionkeys)
        print("At Client:")
        print(self.Kcs)
        self.nonce2 = random.randint(1,9)
        server.authServerKcs(self.Kcs_enc_Kts, self.tempstr2)

    def checking(self, server):
        if(server.fnonce2 == self.nonce2 + 1):
            print("***Nonce verified***\n")
            time.sleep(2)
        if(self.Kcs == server.Kcs):
            print("Kcs")
            print(self.Kcs)
            print("!!!! Kcs shared secretly, integrity maintained !!!!")





class KeyDistCenter:
    def __init__(self,id):
        self.id = id
        self.infobase = {1:'ALPHA', 2:'BETA',3: 'CENTURY',4: 'DELTA',5: 'EPSILON'}
        self.server_id = random.choice(list(self.infobase.keys()))

    def authenticate(self,id,etext1):
        global sessionkeys
        print(id)
        print(etext1)
        if(id in self.infobase):
            password = decrypt(etext1,sessionkeys['Kca'])
            #print("@@@ ",password, "\n MMMM ",self.infobase[id])
            if self.infobase[id] == password: #pass password parameter correctly in Client object, must match infobase
                #generate 16-bit alphanumeric TGT
                self.TGT = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                #TGT = "Sidd"
                print(self.TGT)
                return str(self.TGT)
        else:
            print("\n---ID invalid, Auth. failed---")
            sys.exit()


    def grantTicket(self,enc_tgt,id,nonce1):
        global sessionkeys
        print(id)
        print(enc_tgt)
        fnonce1 = nonce1 + 1 #nonce updation used in verification at client side for integrity checking
        #generate session key Kcs
        ###
        Kcs = random.randint(1,9)
        print("Kcs <<<---Secret, just for verification check here-------->>>>>>>> \n", Kcs)
        ###
        print("Server ID ----- ",self.server_id)
        tempstr1 = '|'.join([str(Kcs),str(id),str(fnonce1)])
        tempstr2 = '|'.join([str(Kcs),str(self.server_id),str(id)])
        #Kcs_enc_Kct_extra = str(encrypt(Kcs, sessionkeys['Kct']))
        Kcs_enc_Kct = encrypt(str(Kcs), sessionkeys['Kct'])
        Kcs_enc_Kts = encrypt(str(Kcs), sessionkeys['Kts'])
        return Kcs_enc_Kct, Kcs_enc_Kts, tempstr1, tempstr2



class Server:

    def __init__(self, id):
        self.id = id
    def authServerKcs(self, Kcs_enc_Kts, tempstr2):
        array2 = (tempstr2).split("|")
        print("Array at server---------")
        print(array2)
        self.Kcs = int(decrypt(Kcs_enc_Kts, sessionkeys['Kts']))
        self.id = int(array2[1])
        print("Server ID ---- ", self.id)

    def finalauthClientKcs(self, client):
        self.fnonce2 = client.nonce2 + 1




###
#Creation of objects and calling methods
###
'''
i1 = 3
s1 = 3
enc_i1 = encrypt(str(i1),s1)
print(enc_i1)
dec_i1 = decrypt(enc_i1, s1)
print(dec_i1)
i1_1 = int(dec_i1)
print(i1 == i1_1)
'''

print("Public session keys:")
print(sessionkeys)

time.sleep(2)

#Passing IDs and Auth. password to the classes where Server and Client must have IDs in the KDC's infobase
p1 = KeyDistCenter(22)
p3 = Server(0)
p2 = Client(11, 'ALPHA')

time.sleep(2)

p2.initiate(p1) #Autheticates with Auth Server of KDC its password. In return, gets TGT

time.sleep(2)

p2.requestTicket(p1,p3) #Request made for the Ticket. KDC grants and sends Kcs, which is forwarded to Server, encrypted by Kts

time.sleep(2)

p3.finalauthClientKcs(p2) #Server gets Kcs and sends f(Nonce2) to complete the verification

time.sleep(2)

p2.checking(p3) #Checking to verify if Kcs shared and if Nonce integrity maintained

time.sleep(2)

print("Final Dictionary of session keys:")
print(sessionkeys)
