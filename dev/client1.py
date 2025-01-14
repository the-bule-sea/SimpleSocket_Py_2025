import random
import tkinter as tk
from tkinter import messagebox, ttk
import socket
import struct
import os
import time
import re


class NetworkCommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("客户端 - 网络通信软件")

        # 创建组件
        self.create_widgets()

        # 初始化本机信息
        self.local_ips = self.get_local_ips()
        self.local_ip_var = tk.StringVar(value=self.local_ips[0] if self.local_ips else '')
        # 下拉框
        self.local_ip_menu = ttk.Combobox(self.root, textvariable=self.local_ip_var, values=self.local_ips,
                                          state="readonly")
        self.local_ip_menu.grid(row=0, column=1)

        # 显示本机信息
        self.display_local_info()

        # 绑定事件
        self.send_button.config(command=self.send_packet)

    def create_widgets(self):
        # 本机信息
        tk.Label(self.root, text="本机信息:").grid(row=0, column=0)
        self.local_info_text = tk.Text(self.root, height=5, width=50, state="disabled")
        self.local_info_text.grid(row=1, column=0, columnspan=2)

        # 输入部分
        tk.Label(self.root, text="本地端口:").grid(row=2, column=0)
        tk.Label(self.root, text="目的主机 (IP/域名):").grid(row=3, column=0)
        tk.Label(self.root, text="目的端口:").grid(row=4, column=0)
        tk.Label(self.root, text="报文类型:").grid(row=5, column=0)

        self.local_port_entry = tk.Entry(self.root)
        self.remote_host_entry = tk.Entry(self.root)
        self.remote_port_entry = tk.Entry(self.root)

        self.local_port_entry.grid(row=2, column=1)
        self.remote_host_entry.grid(row=3, column=1)
        self.remote_port_entry.grid(row=4, column=1)

        self.packet_type_var = tk.StringVar(value="ICMP")
        self.packet_type_frame = tk.Frame(self.root)
        self.packet_type_frame.grid(row=5, column=1)
        for packet_type in ["ICMP", "UDP", "TCP", "DNS", "IP"]:
            tk.Radiobutton(self.packet_type_frame, text=packet_type, variable=self.packet_type_var,
                           value=packet_type).pack(side=tk.LEFT)

        # 按钮
        self.send_button = tk.Button(self.root, text="发送报文")
        self.send_button.grid(row=6, column=0, columnspan=2)

        # 结果显示框
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=7, column=0, columnspan=2)

    def get_local_ips(self):
        ips = []
        try:
            addrs = socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET)
            for addr in addrs:
                if addr[4][0] != '127.0.0.1':
                    ips.append(addr[4][0])
        except socket.gaierror:
            pass

            # 手动添加特定接口的IP地址
        try:
            eth0_addrs = socket.getaddrinfo('wlo1', None, family=socket.AF_INET)
            for addr in eth0_addrs:
                if addr[4][0] != '127.0.0.1':
                    ips.append(addr[4][0])
        except socket.gaierror:
            pass

        return ips

    # linux获取ip请用以下代码
    # def get_local_ips():
    #     ips = []
    #     interfaces = ["eth0", "wlo1", "ens33", "enp0s3", "lo"]  # 常见网络接口名称，按需添加
    #     for iface in interces:
    #         try:
    #             sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #             ip = socket.inet_ntoa(fcntl.ioctl(
    #                 sock.fileno(),
    #                 0x8915,  # SIOCGIFADDR
    #                 struct.pack('256s', iface[:15].encode('utf-8'))
    #             )[20:24])
    #             ips.append(ip)
    #         except OSError:
    #             pass
    #     return ips

    def display_local_info(self):
        host_name = 3
        mac_addr = self.get_mac_address()
        ip_addr = ", ".join(self.local_ips)
        info = f"主机名: {host_name}\nMAC 地址: {mac_addr}\n本机 IP 地址: {ip_addr}"
        self.local_info_text.config(state="normal")
        self.local_info_text.delete(1.0, tk.END)
        self.local_info_text.insert(tk.END, info)
        self.local_info_text.config(state="disabled")

    def get_mac_address(self):
        mac = ':'.join(re.findall('..', '%012x' % os.getpid()))
        return mac

    def validate_inputs(self):
        try:
            local_port = int(self.local_port_entry.get())
            remote_port = int(self.remote_port_entry.get())
            if local_port <= 0 or local_port > 65535 or remote_port <= 0 or remote_port > 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "端口号必须是1-65535之间的正整数")
            return False

        remote_host = self.remote_host_entry.get()
        if not (self.is_valid_ip(remote_host) or self.is_valid_domain(remote_host)):
            messagebox.showerror("输入错误", "目的主机格式不正确 (应为有效的 IP 地址或域名)")
            return False

        return True

    def is_valid_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def is_valid_domain(self, domain):
        pattern = r'^[a-zA-Z0-9-]{1,63}(\.[a-zA-Z]{2,6})+$'
        return bool(re.match(pattern, domain))

    def send_icmp_packet(self, src_ip, dst_ip):
        # 构建ICMP包
        icmp_type = 8  # request请求类型
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
        start_time = time.time()
        sock.sendto(packet, (dst_ip, 0))
        # sock.close()
        print("icmp发送")
        self.result_text.insert(tk.END, f"ICMP包已发送到 {dst_ip}\n")
        # 接收响应
        # sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        # 使用同一个socket接收响应
        sock.settimeout(5)
        try:
            data, addr = sock.recvfrom(1024)
            end_time = time.time()
            print("接受响应")
            self.result_text.insert(tk.END, f"收到响应来自 {addr[0]}, 耗时: {(end_time - start_time) * 1000:.3f}ms\n")
        except socket.timeout:
            self.result_text.insert(tk.END, "未收到响应\n")

    def send_tcp_packet(self, src_ip, src_port, dst_ip, dst_port):
        try:
            # 解析目标地址
            dst_ip = socket.gethostbyname(dst_ip)

            # 构建TCP包
            payload = b""
            seq = random.randint(0, 0xFFFF_FFFF)
            ack_seq = 0  # ack
            doff = 5  # 数据偏移量
            fin = 0
            syn = 1  # SYN标志
            rst = 0
            psh = 0
            ack = 0
            urg = 0
            window = socket.htons(5840)  # 窗口大小
            checksum = 0
            urg_ptr = 0

            # TCP 标志字段
            offset_res_flags = (doff << 12) | (fin << 0) | (syn << 1) | (rst << 2) | \
                               (psh << 3) | (ack << 4) | (urg << 5)
            # 构建 TCP 头部
            tcp_header = struct.pack('!HHLLHHHH',
                                     src_port,  # 源端口
                                     dst_port,  # 目标端口
                                     seq,  # 序列号
                                     ack_seq,  # 确认号
                                     offset_res_flags,  # 数据偏移和标志
                                     window,  # 窗口大小
                                     checksum,  # 校验和
                                     urg_ptr)  # 紧急指针

            # 构建伪头部（用于校验和计算，不发送）
            tcp_length = len(tcp_header) + len(payload)
            pseudo_header = struct.pack('!4s4sBBH',
                                        socket.inet_aton(src_ip),  # 源IP地址
                                        socket.inet_aton(dst_ip),  # 目的IP地址
                                        0,
                                        socket.IPPROTO_TCP,  # 协议类型
                                        tcp_length)  # TCP总长度

            # 计算校验和
            checksum = self.calculate_checksum(pseudo_header + tcp_header + payload)

            # 重新生成 TCP 头部，带上校验和
            tcp_header = struct.pack('!HHLLHHHH',
                                     src_port,
                                     dst_port,
                                     seq,
                                     ack_seq,
                                     offset_res_flags,
                                     window,
                                     checksum,
                                     urg_ptr)
            # 完整的 TCP 包
            packet = tcp_header + payload
            # 发送 TCP 包
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.sendto(packet, (dst_ip, dst_port))
            # 显示成功信息
            self.result_text.insert(tk.END, f"TCP报文已发送到 {dst_ip}:{dst_port}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"发送TCP报文失败: {e}\n")
            # 错误处理
            messagebox.showerror("发送失败", f"发送TCP报文时出错：{e}")

    def send_udp_packet(self, src_ip, src_port, dst_ip, dst_port):

        dst_ip = socket.gethostbyname(dst_ip)

        payload = b"Hello, World!"
        length = 8 + len(payload)  # UDP头部固定长度8字节 + 数据长度
        checksum = 0

        # 构建UDP头部
        udp_header = struct.pack("!HHHH", src_port, dst_port, length, checksum)

        # 伪头部用于校验和计算,并不会被发送出去
        """
        inet_aton(src_ip), Convert an IP address in string format (123.45.67.89) to the 32-bit packed
        IPPROTO_UDP, 8位协议, UDP是17
        """
        pseudo_header = struct.pack(
            "!4s4sBBH",
            socket.inet_aton(src_ip),  # 源IP地址
            socket.inet_aton(dst_ip),  # 目的IP地址
            0,
            socket.IPPROTO_UDP,  # 协议类型，常量-17
            length
        )

        # 计算校验和
        checksum = self.calculate_checksum(pseudo_header + udp_header + payload)
        udp_header = struct.pack("!HHHH", src_port, dst_port, length, checksum)

        # 完整的UDP包
        packet = udp_header + payload

        # 发送UDP包
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        try:
            sock.sendto(packet, (dst_ip, dst_port))
            self.result_text.insert(tk.END, f"UDP包已发送到 {dst_ip}:{dst_port}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"发送UDP包失败: {e}\n")
            messagebox.showerror("发送失败", f"发送UDP包失败: {e}")

    # dst_port应为53
    def send_dns_packet(self, src_ip, src_port, dst_ip, dst_port):
        # 构建DNS查询包
        id = os.urandom(2)  # 随机生成查询ID
        flags = b'\x01\x00'  # 表明标准查询（Standard query）
        qdcount = b'\x00\x01'  # 表示只有一个查询
        ancount = b'\x00\x00'  # 没有应答
        nscount = b'\x00\x00'  # 没有权威应答
        arcount = b'\x00\x00'  # 无附加记录数量
        name = b'\x07example\x03com\x00'  # 查询的域名
        qtype = b'\x00\x01'  # 查询类型: A 记录
        qclass = b'\x00\x01'  # 查询类: IN 类

        packet = id + flags + qdcount + ancount + nscount + arcount + name + qtype + qclass

        # 发送DNS查询包
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 因为DNS查询通常使用UDP协议
        sock.sendto(packet, (dst_ip, dst_port))

        # 接收响应
        sock.settimeout(2)
        try:
            data, addr = sock.recvfrom(1024)
            print(data)
            self.result_text.insert(tk.END, f"收到DNS响应来自 {addr[0]}:{addr[1]}\n")
            self.result_text.insert(tk.END, f"收到的DNS响应为{data}\n")
        except socket.timeout:
            self.result_text.insert(tk.END, "未收到DNS响应\n")
        finally:
            sock.close()

    def send_ip_packet(self, src_ip, src_port, dst_ip, dst_port):
        # data
        payload = b""
        # ICMP Header
        icmp_type = 8  # 请求
        icmp_code = 0
        icmp_checksum = 0
        identifier = os.getpid() & 0xFFFF
        sequence = 1
        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, identifier, sequence)
        icmp_checksum = self.calculate_checksum(icmp_header + payload)
        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, identifier, sequence)

        icmp_packet = icmp_header + payload

        # IP头
        version = 4  # IPv4
        ihl = 5  # IP头长度，5*4字节=20字节
        tos = 0  # 服务类型
        total_length = 20 + len(icmp_packet)  # IP头长度
        identification = os.getpid() & 0xFFFF  # 标识符
        flags = 0  # 标志
        fragment_offset = 0  # 片偏移
        ttl = 255  # 生存时间
        protocol = socket.IPPROTO_ICMP  # 协议类型: 协议字段指出此数据报携带的数据使用何种协议，以便使目的主机的IP层知道应将数据部分上交给哪个协议进行处理。
        checksum = 0  # 校验和
        print("src_ip:", src_ip)
        print("src_port:", src_port)
        print("dst_ip:", dst_ip)
        print("dst_port:", dst_port)

        # 构建IP头
        ihl_version = (version << 4) + ihl
        flags_fragment_offset = (flags << 13) + fragment_offset
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                ihl_version, tos, total_length, identification,
                                flags_fragment_offset, ttl, protocol, checksum,
                                socket.inet_aton(src_ip), socket.inet_aton(dst_ip))

        # 计算校验和
        header_checksum = self.calculate_checksum(ip_header)
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                ihl_version, tos, total_length, identification,
                                flags_fragment_offset, ttl, protocol, header_checksum,
                                socket.inet_aton(src_ip), socket.inet_aton(dst_ip))

        # 2. 数据部分（例如UDP数据）
        # 这里为了简单，直接使用字符串作为数据
        # 如果需要发送其他协议的数据，需要按照相应的协议格式进行封装
        ip_packet = ip_header + icmp_packet
        # 3. 发送IP报文
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)  # 使用RAW socket
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  # 告诉内核我们自己构建IP头部
            sock.sendto(ip_packet, (dst_ip, 0))  # 发送到目标IP

            print(f"IP报文已发送到 {dst_ip}")
            self.result_text.insert(tk.END, f"IP报文已发送到 {dst_ip}\n")
        except Exception as e:
            print(f"发送IP报文失败: {e}")
            messagebox.showerror("发送失败",f"发送IP报文时出错：{e}")
            self.result_text.insert(tk.END, f"发送IP报文失败: {e}\n")

    def send_packet(self):
        if not self.validate_inputs():
            return

        packet_type = self.packet_type_var.get()
        local_ip = self.local_ip_var.get()
        local_port = int(self.local_port_entry.get())
        remote_host = self.remote_host_entry.get()
        remote_port = int(self.remote_port_entry.get())

        if packet_type == "ICMP":
            self.send_icmp_packet(local_ip, remote_host)
        elif packet_type == "UDP":
            self.send_udp_packet(local_ip, local_port, remote_host, remote_port)
        elif packet_type == "TCP":
            self.send_tcp_packet(local_ip, local_port, remote_host, remote_port)
        elif packet_type == "DNS":
            self.send_dns_packet(local_ip, local_port, remote_host, remote_port)
        elif packet_type == "IP":
            # self.send_ip_packet(local_ip, remote_host)
            self.send_ip_packet(local_ip, local_port, remote_host, remote_port)

    def calculate_checksum(self, data):
        if len(data) % 2 != 0:
            data += b"\x00"  # 如果数据长度为奇数，填充一个字节

        checksum = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            checksum += word
            checksum = (checksum & 0xFFFF) + (checksum >> 16)  # 进位加回低16位

        return ~checksum & 0xFFFF  # 取反，返回16位结果


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkCommunicationApp(root)
    root.mainloop()
