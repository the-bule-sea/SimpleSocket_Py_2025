import socket

s = socket.socket()
host = socket.gethostname()
print(" Server host is ", host)
port = 80
s.bind((host, port))
print(" Server is listening on port ", port)
s.listen(5)
conn ,addr = s.accept()
print(" Connected to ", addr)
while True:
    message = input(str('>> ')).encode()
    conn.send(message)
    print('Sent')
    incoming_message = conn.recv(1024)
    imcoming_message = incoming_message.decode()
    print('Client:', incoming_message)
