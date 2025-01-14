import tkinter as tk
from tkinter import messagebox
import socket
import struct
import os
import time

class NetworkCommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("服务器 - 网络通信软件")

        # 创建组件
        self.create_widgets()

        # 初始化本机信息
        self.local_ips = self.get_local_ips()
        self.local_ip_var = tk.StringVar(value=self.local_ips[0] if self.local_ips else '')
        self.local_ip_menu = tk.OptionMenu(self.root, self.local_ip_var, *self.local_ips)
        self.local_ip_menu.grid(row=0, column=1)

        # 绑定事件
        self.listen_button.config(command=self.start_listening)

    def create_widgets(self):
        # 创建标签和输入框
        tk.Label(self.root, text="本地IP:").grid(row=0, column=0)
        tk.Label(self.root, text="本地端口:").grid(row=1, column=0)

        self.local_port_entry = tk.Entry(self.root)

        self.local_port_entry.grid(row=1, column=1)

        # 创建按钮
        self.listen_button = tk.Button(self.root, text="开始监听")
        self.listen_button.grid(row=2, column=0, columnspan=2)

        # 创建结果显示框
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=3, column=0, columnspan=2)

    def get_local_ips(self):
        ips = []
        for interface in socket.getaddrinfo(socket.gethostname(), None):
            if interface[0] == socket.AF_INET:
                ips.append(interface[4][0])
        return ips

    def start_listening(self):
        try:
            local_port = int(self.local_port_entry.get())
            if local_port <= 0 or local_port > 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "端口号必须是1-65535之间的正整数")
            return

        local_ip = self.local_ip_var.get()
        self.listen_for_packets(local_ip, local_port)

    def listen_for_packets(self, local_ip, local_port):
        # 创建UDP监听套接字
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind((local_ip, local_port))

        # 创建TCP监听套接字
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind((local_ip, local_port))
        tcp_sock.listen(1)

        self.result_text.insert(tk.END, f"开始监听 {local_ip}:{local_port}\n")

        while True:
            # 接收UDP包
            try:
                data, addr = udp_sock.recvfrom(1024)
                self.result_text.insert(tk.END, f"收到UDP包来自 {addr[0]}:{addr[1]}\n")
            except socket.error:
                pass

            # 接收TCP连接
            try:
                client_sock, addr = tcp_sock.accept()
                data = client_sock.recv(1024)
                self.result_text.insert(tk.END, f"收到TCP连接来自 {addr[0]}:{addr[1]}\n")
                client_sock.close()
            except socket.error:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkCommunicationApp(root)
    root.mainloop()