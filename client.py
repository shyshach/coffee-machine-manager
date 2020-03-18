import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

msg = s.recv(1024)
print(msg.decode("utf-8"))
while True:
    s.send(bytes(str(input()), "utf-8"))
    msg = s.recv(1024).decode("utf-8")
    print(msg)
    if "It will be ready" in msg:
        break
print(s.recv(1024).decode("utf-8"))