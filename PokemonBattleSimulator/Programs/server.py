# Chat Room Connection - Client-To-Client
import threading
import socket
host = "172.20.10.9"
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
FORMAT = "utf-8"

def broadcast(message) :
    if message != "b''" :
        print(message)
        for client in clients :
            client.send(message)

def handle_client(client) :
    while True :
        try :
            message = client.recv(1024)
            #print(message)
            broadcast(message)
        except :
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            #broadcast(f"!playerleft:{alias}".encode(FORMAT))
            msg = f"!left:{alias}"
            broadcast(msg.encode(FORMAT))
            #print(msg)
            aliases.remove(alias)
            break

# Main function to receive the clients connection
def receive() :
    while True :
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f"Connection established with {str(address)}")
        client.send("alias?".encode(FORMAT))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f"The alias of this client is {alias}".encode(FORMAT))
        broadcast(f"{alias} has connected to the chat room".encode(FORMAT))
        broadcast(f"!players:{aliases}".encode(FORMAT))
        #print(aliases)
        client.recv(1024)
        client.send("You are now connected!".encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__" :
    receive()
