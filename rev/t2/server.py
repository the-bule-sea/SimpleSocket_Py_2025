import socket

def server():
    host = str(input("请输入连接的IP地址"))
    port = int(input("请输入连接的端口号"))
    server_socket = socket.socket()
    # bind函数用来绑定地址和端口
    server_socket.bind((host, port))
    # listen函数用来监听连接
    server_socket.listen(5)
    print("服务器已启动，等待连接...")
    conn, address = server_socket.accept()
    print("已连接到客户端：", address)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("收到消息：", data.decode())
        conn.send(data)
    conn.close()

if __name__ == '__main__':
    server()