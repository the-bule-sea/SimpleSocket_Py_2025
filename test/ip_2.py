import socket
import struct
import os
import binascii

def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += int.from_bytes(data[i:i+2], 'big')
    if n:
        s += data[len(data) - 1]
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    return (~s & 0xFFFF).to_bytes(2, 'big') # 返回字节串

class PktGen():

    def send_packet(self, src_ip, src_port, dst_ip, dst_port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            payload = b"Hello, IP!"

            # ICMP Header
            icmp_type = 8  # Echo Request
            code = 0
            checksum_placeholder = 0 # 校验和占位符
            identifier = os.getpid() & 0xFFFF
            sequence = 1
            icmp_header = struct.pack("!BBHHH", icmp_type, code, checksum_placeholder, identifier, sequence)
            icmp_checksum = checksum(icmp_header + payload) # 计算校验和
            icmp_header = struct.pack("!BBHHH", icmp_type, code, int.from_bytes(icmp_checksum,'big'), identifier, sequence) # 重新打包头部，填入计算好的校验和

            icmp_packet = icmp_header + payload

            # IP Header
            ihl = 5
            version = 4
            tos = 0
            total_length = 20 + len(icmp_packet)
            identification = os.getpid() & 0xFFFF
            flags = 0
            frag_off = 0
            ttl = 255
            protocol = socket.IPPROTO_ICMP
            check = 0
            saddr = socket.inet_aton(src_ip)
            daddr = socket.inet_aton(dst_ip)
            ihl_version = (version << 4) + ihl

            ip_header = struct.pack('!BBHHHBBH4s4s', ihl_version, tos, total_length, identification, frag_off, ttl, protocol, check, saddr, daddr)
            ip_checksum = checksum(ip_header)
            ip_header = ip_header[:10] + ip_checksum + ip_header[12:]

            packet = ip_header + icmp_packet
            s.sendto(packet, (dst_ip, 0))
            print(f"IP报文已发送到 {dst_ip}")

        except Exception as e:
            print(f"发送IP报文失败: {e}")
        finally:
            if 's' in locals():
                s.close()

if __name__ == '__main__':
    pkt = PktGen()
    src_ip = "192.168.0.113"  # 修改为你的源IP
    dst_ip = "192.168.0.104"  # 修改为你的目标IP
    src_port = 12345  # 这个端口在ICMP中没有意义，可以忽略
    dst_port = 369  # 这个端口在ICMP中没有意义，可以忽略
    pkt.send_packet(src_ip, src_port, dst_ip, dst_port)