import socket

def client_connect(ip : str, port : int) :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))


print(socket.gethostname())
#msg = s.recv(1024)
#print(msg.decode("utf-8"))
