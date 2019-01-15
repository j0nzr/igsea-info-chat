import socket
import threading
import tkinter

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
Handles recieved messages from server
"""
def recieve():
    while True:
        msg = client_socket.recv(1024)
        msg = bytes2string(msg)
        msg_list.insert(tkinter.END, msg)

"""
sends message to server

event: variable for tkinter, default is None
"""
def sendMessage(event=None):
    msg = my_msg.get()
    my_msg.set("") 
    client_socket.send(string2bytes(msg))
    if msg == "{quit}":
        client_socket.close()
        chat.quit()

"""
Handles closing the chat window

event: see sendMessage()
"""
def onClose(event=None):
    my_msg.set("{quit}")
    sendMessage()

chat = tkinter.Tk() #creating new Tkinter Window
chat.title("Chatroom")

messages_frame = tkinter.Frame(chat)  #creating view for recieved messages
my_msg = tkinter.StringVar()
my_msg.set("Dein Username...")
scrollbar = tkinter.Scrollbar(messages_frame) #making overflow possible

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(chat, textvariable=my_msg)
entry_field.bind("<Return>", sendMessage)
entry_field.pack()
send_button = tkinter.Button(chat, text="Senden", command=sendMessage)
send_button.pack()

chat.protocol("WM_DELETE_WINDOW", onClose)

server = '127.0.0.1'  #ip of the chat server
port = 14 #port for communication

addrTupl = (server, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(addrTupl)

receiving = threading.Thread(target=recieve)
receiving.start()
tkinter.mainloop() #starting tkinter frontend
