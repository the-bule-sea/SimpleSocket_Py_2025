import tkinter as tk
from tkinter import messagebox
import socket
import struct
import os
import time

class NetworkCommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("网络通信软件")

        # 创建组件
        self.create_widgets()

        # 初始化本机信息
        self.local_ips = self.get_local_ips()
        self.local_ip_var = tk.StringVar(value=self.local_ips[0] if self.local_ips else '')
        self.local_ip_menu = tk.OptionMenu(self.root, self.local_ip_var, *self.local_ips)
        self.local_ip_menu.grid(row=0, column=1)

        # 绑定事件
        self.send_button.config(command=self.send_packet)

    def create_widgets(self):
        # 创建标签和输入框
        tk.Label(self.root, text="本地IP:").grid(row=0, column=0)
        tk.Label(self.root, text="本地端口:").grid(row=1, column=0)
        tk.Label(self.root, text="远程IP:").grid(row=2, column=0)
        tk.Label(self.root, text="远程端口:").grid(row=3, column=0)
        tk.Label(self.root, text="报文类型:").grid(row=4, column=0)

        self.local_port_entry = tk.Entry(self.root)
        self.remote_ip_entry = tk.Entry(self.root)
        self.remote_port_entry = tk.Entry(self.root)

        self.packet_type_var = tk.StringVar(value="ICMP")
        self.packet_type_menu = tk.OptionMenu(self.root, self.packet_type_var, "ICMP", "UDP", "TCP", "DNS")

        self.local_port_entry.grid(row=1, column=1)
        self.remote_ip_entry.grid(row=2, column=1)
        self.remote_port_entry.grid(row=3, column=1)
        self.packet_type_menu.grid(row=4, column=1)

        # 创建按钮
        self.send_button = tk.Button(self.root, text="发送报文")
        self.send_button.grid(row=5, column=0, columnspan=2)

        # 创建结果显示框
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=6, column=0, columnspan=2)

    def get_local_ips(self):
        ips = []
        for interface in socket.getaddrinfo(socket.gethostname(), None):
            if interface[0] == socket.AF_INET:
                ips.append(interface[4][0])
        return ips

    def validate_inputs(self):
        try:
            local_port = int(self.local_port_entry.get())
            remote_port = int(self.remote_port_entry.get())
            if local_port <= 0 or local_port > 65535 or remote_port <= 0 or remote_port > 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "端口号必须是1-65535之间的正整数")
            return False

        remote_ip = self.remote_ip_entry.get()
        try:
            socket.inet_aton(remote_ip)
        except socket.error:
            messagebox.showerror("输入错误", "远程IP地址格式不正确")
            return False

        return True

    def send_packet(self):
        if not self.validate_inputs():
            return

        packet_type = self.packet_type_var.get()
        local_ip = self.local_ip_var.get()
        local_port = int(self.local_port_entry.get())
        remote_ip = self.remote_ip_entry.get()
        remote_port = int(self.remote_port_entry.get())

        if packet_type == "ICMP":
            self.send_icmp_packet(local_ip, remote_ip)
        elif packet_type == "UDP":
            self.send_udp_packet(local_ip, local_port, remote_ip, remote_port)
        elif packet_type == "TCP":
            self.send_tcp_packet(local_ip, local_port, remote_ip, remote_port)
        elif packet_type == "DNS":
            self.send_dns_packet(local_ip, local_port, remote_ip, remote_port)

    def send_icmp_packet(self, src_ip, dst_ip):
        # 构建ICMP包
        icmp_type = 8  # Echo request
        code = 0
        checksum = 0
        identifier = os.getpid() & 0xFFFF
        sequence = 1
        payload = b"Hello, World!"

        header = struct.pack("!BBHHH", icmp_type, code, checksum, identifier, sequence)
        packet = header + payload
        checksum = self.calculate_checksum(packet)
        packet = packet[:2] + struct.pack("!H", checksum) + packet[4:]

        # 发送ICMP包
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        start_time = time.time()
        sock.sendto(packet, (dst_ip, 0))
        sock.close()

        self.result_text.insert(tk.END, f"ICMP包已发送到 {dst_ip}\n")

        # 接收响应
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(2)
        try:
            data, addr = sock.recvfrom(1024)
            end_time = time.time()
            self.result_text.insert(tk.END, f"收到响应来自 {addr[0]}, 耗时: {end_time - start_time:.2f}秒\n")
        except socket.timeout:
            self.result_text.insert(tk.END, "未收到响应\n")
        finally:
            sock.close()

    def send_udp_packet(self, src_ip, src_port, dst_ip, dst_port):
        # 构建UDP包
        src_port = src_port
        dst_port = dst_port
        length = 8 + len(b"Hello, World!")
        checksum = 0
        payload = b"Hello, World!"

        header = struct.pack("!HHHH", src_port, dst_port, length, checksum)
        packet = header + payload

        # 发送UDP包
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (dst_ip, dst_port))
        sock.close()

        self.result_text.insert(tk.END, f"UDP包已发送到 {dst_ip}:{dst_port}\n")

    def send_tcp_packet(self, src_ip, src_port, dst_ip, dst_port):
        # 构建TCP包
        src_port = src_port
        dst_port = dst_port
        seq_num = 0
        ack_num = 0
        offset = 5  # 5 * 4 = 20 bytes
        flags = 0x02  # SYN flag
        window_size = 65535
        checksum = 0
        urgent_pointer = 0

        tcp_header = struct.pack("!HHLLBBHHH", src_port, dst_port, seq_num, ack_num, (offset << 4) + flags, window_size, checksum, urgent_pointer)

        # 计算校验和
        pseudo_header = struct.pack("!4s4sBBH", socket.inet_aton(src_ip), socket.inet_aton(dst_ip), 0, socket.IPPROTO_TCP, len(tcp_header))
        checksum = self.calculate_checksum(pseudo_header + tcp_header)
        tcp_header = tcp_header[:16] + struct.pack("!H", checksum) + tcp_header[18:]

        # 发送TCP包
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.sendto(tcp_header, (dst_ip, dst_port))
        sock.close()

        self.result_text.insert(tk.END, f"TCP包已发送到 {dst_ip}:{dst_port}\n")

    def send_dns_packet(self, src_ip, src_port, dst_ip, dst_port):
        # 构建DNS查询包
        id = os.urandom(2)
        flags = b'\x01\x00'  # Standard query
        qdcount = b'\x00\x01'  # One question
        ancount = b'\x00\x00'
        nscount = b'\x00\x00'
        arcount = b'\x00\x00'
        name = b'\x07example\x03com\x00'
        qtype = b'\x00\x01'  # A record
        qclass = b'\x00\x01'  # IN class

        packet = id + flags + qdcount + ancount + nscount + arcount + name + qtype + qclass

        # 发送DNS查询包
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (dst_ip, dst_port))

        # 接收响应
        sock.settimeout(2)
        try:
            data, addr = sock.recvfrom(1024)
            self.result_text.insert(tk.END, f"收到DNS响应来自 {addr[0]}:{addr[1]}\n")
        except socket.timeout:
            self.result_text.insert(tk.END, "未收到DNS响应\n")
        finally:
            sock.close()

    def calculate_checksum(self, message):
        s = 0
        for i in range(0, len(message), 2):
            w = (message[i] << 8) + (message[i+1] if i+1 < len(message) else 0)
            s += w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkCommunicationApp(root)
    root.mainloop()