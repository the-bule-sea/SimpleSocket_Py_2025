import socket


s = socket.socket()
host = input(str('输入host'))
port = 8080
address = (host, port)
s.connect(address) # 传入元组
print('socket connected to ' + host)
while True:
    incoming_message = s.recv(1024).decode('utf-8')
    print("server:" + incoming_message)
    message = input(str('client:')).encode('utf-8')
    s.send(message)
