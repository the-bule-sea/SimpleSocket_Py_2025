import socket
import time


def udp_client(host='192.168.0.101', port=92):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"Hello, UDP server!"
    for _ in range(1):  # 连续发送5次数据
        sock.sendto(payload, (host, port))
        print(f"Sent to {host}:{port}: {payload.decode()}")
        time.sleep(0.1)

udp_client()


# def send_udp_packet(self, src_ip, src_port, dst_ip, dst_port):
    #
    #     payload = b"Hello, World!"
    #     length = 8 + len(payload)  # UDP头部固定长度8字节 + 数据长度
    #     checksum = 0
    #
    #     # 构建UDP头部
    #     udp_header = struct.pack("!HHHH", src_port, dst_port, length, checksum)
    #
    #     # 伪头部用于校验和计算
    #     pseudo_header = struct.pack(
    #         "!4s4sBBH",
    #         socket.inet_aton(src_ip),
    #         socket.inet_aton(dst_ip),
    #         0,
    #         socket.IPPROTO_UDP,
    #         length
    #     )
    #
    #     # 计算校验和
    #     checksum = self.calculate_checksum(pseudo_header + udp_header + payload)
    #     udp_header = struct.pack("!HHHH", src_port, dst_port, length, checksum)
    #
    #     # 完整的UDP包
    #     packet = udp_header + payload
    #
    #     # 发送UDP包
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     try:
    #         sock.sendto(packet, (dst_ip, dst_port))
    #         self.result_text.insert(rev.END, f"UDP包已发送到 {dst_ip}:{dst_port}\n")
    #     except Exception as e:
    #         self.result_text.insert(rev.END, f"发送UDP包失败: {e}\n")
    #     finally:
    #         sock.close()

    # def send_tcp_packet(self, src_ip, src_port, dst_ip, dst_port):
    #     seq_num = 0
    #     ack_num = 0
    #     offset = 5  # 数据偏移，5 表示 5*4 = 20 字节 TCP 头部长度
    #     flags = 0x02  # SYN 标志
    #     window_size = 65535
    #     checksum = 0
    #     urgent_pointer = 0
    #
    #     # TCP头部
    #     tcp_header = struct.pack(
    #         "!HHLLBBHHH",
    #         src_port, dst_port, seq_num, ack_num,
    #         (offset << 4), flags,
    #         window_size, checksum, urgent_pointer
    #     )
    #
    #     # 伪头部用于校验和计算
    #     pseudo_header = struct.pack(
    #         "!4s4sBBH",
    #         socket.inet_aton(src_ip),
    #         socket.inet_aton(dst_ip),
    #         0,
    #         socket.IPPROTO_TCP,
    #         len(tcp_header)
    #     )
    #
    #     # 计算校验和
    #     checksum = self.calculate_checksum(pseudo_header + tcp_header)
    #     tcp_header = tcp_header[:16] + struct.pack("!H", checksum) + tcp_header[18:]
    #
    #     # 原始套接字发送数据包
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #     sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  # 自定义 IP 头部
    #     try:
    #         sock.sendto(tcp_header, (dst_ip, dst_port))
    #         self.result_text.insert(rev.END, f"TCP包已发送到 {dst_ip}:{dst_port}\n")
    #     except Exception as e:
    #         self.result_text.insert(rev.END, f"发送TCP包失败: {e}\n")
    #     finally:
    #         sock.close()
