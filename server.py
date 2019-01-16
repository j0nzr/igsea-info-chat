import socket
import threading
import random

"""
Starting with default Socket-Operations
"""

def byteorder():
    return sys.byteorder

def standard_encoding():
    return sys.getdefaultencoding()

def standardausgabe_encoding():
    return sys.stdout.encoding

def string2bytes(text):
    return bytes(text, "utf8")

def bytes2string(bytes):
    return str(bytes, "utf8")


"""
Handling new Connection to Server
"""
def new_connection():
    while True:
        client, client_address = server.accept()
        print(client_address, " hat sich verbunden.")
        #print("Client", client, "  ", type(client))
        client.send(string2bytes("Willkommen neuer! Sende uns zu aller erst deinen Namen!"))
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()


"""
Handling communication between server and single 
client + sending incomming messages to everyone

input:
client: socket Socket connection between server and client
"""
def handle_client(client):
    name = client.recv(1024)
    name = bytes2string(name)
    welcomeText = "Willkommen " + name + "!"
    client.send(string2bytes(welcomeText))
    msg = name + " ist dem chat beigetretten"
    sendToAll(msg)
    clients[client] = name

    while True:
        message = client.recv(1024)
        if message != string2bytes("{quit}"):
            sendToAll(message, name+":")
            
            """
            Some NSA-Eastereggs :D
            """
            rand = random.randint(0,50)
            if(rand == 1):
                sendToAll("Watch your Words. We're listening.", "NSA: ")
            elif(rand == 2):
                sendToAll("Aha. Intressting!", "NSA: ")
            elif(rand == 3):
                sendToAll("We're not here. Keep talking", "NSA: ")  
                
        else:
            client.send(string2bytes("{quit}"))
            client.close()
            del clients[client]
            sendToAll(string2bytes(name + " hat uns verlassen!"))
            break

"""
Sending a message to everyone in the chatroom

input:
msg: str or bytes  Message to send
prefix: str  Name before the message
"""
def sendToAll(msg, prefix=""):
        if(type(msg) == bytes):
                for sock in clients:
                        sock.send(string2bytes(prefix) + msg)
        else:
                for sock in clients:
                        sock.send(string2bytes(prefix + msg))

clients = {}    #object of all clients
addresses = {}  #object of all addresses

server_ip = '127.0.0.1'  
port = 14
addrTupl = (server_ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket with TC-Protocoll
server.bind(addrTupl) #bind open socket to ip and port of the server

if(__name__ == "__main__"):
        server.listen(5)
        print("Warten auf Verbindung durch client")
        accept = threading.Thread(target=new_connection) #thread for waiting and accepting new connections
        accept.start() #starting thread for new connections
        accept.join() #wait for thread to execute
        server.close()
