import socket

def udp_server(host='127.0.0.1', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))  # 绑定本地地址和端口
    print(f"UDP Server listening on {host}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)  # 接收数据
        print(f"Received from {addr}: {data.decode()}")
        # 可选：发送一个响应包
        sock.sendto(b"ACK", addr)

udp_server()
