import socket
import struct
import random


class TcpPacket:
    def __init__(self):
        pass

    def calculate_checksum(self, data):
        # 校验和计算
        s = 0
        n = len(data) % 2
        for i in range(0, len(data) - n, 2):
            s += (data[i] << 8) + data[i + 1]
        if n:
            s += data[-1] << 8
        while s >> 16:
            s = (s & 0xFFFF) + (s >> 16)
        return ~s & 0xFFFF

    def send_tcp_packet(self, src_ip, src_port, dst_ip, dst_port):
        # TCP SYN
        payload = b""  # SYN无payload

        # TCP 头部字段
        seq = random.randint(0, 0xFFFF_FFFF)  # 随机初始化序列号
        ack_seq = 0  # ACK号 (初始发送不设置ACK)
        doff = 5  # 数据偏移（TCP头部长度，单位为32位字，5*4=20字节）
        fin = 0
        syn = 1  # SYN标志，用于初始化连接
        rst = 0
        psh = 0
        ack = 0
        urg = 0
        window = socket.htons(5840)  # 窗口大小，通常为默认值
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

        # 构建完整的 TCP 报文
        packet = tcp_header + payload

        # 发送 TCP 报文
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        try:
            sock.sendto(packet, (dst_ip, dst_port))
            print(f"TCP 报文已发送到 {dst_ip}:{dst_port}")
        except Exception as e:
            print(f"发送 TCP 报文失败: {e}")


if __name__ == "__main__":
    tcp = TcpPacket()
    src_ip = "192.168.98.200"
    dst_ip = "192.168.98.140"
    src_port = 11451
    dst_port = 80
    tcp.send_tcp_packet(src_ip, src_port, dst_ip, dst_port)
