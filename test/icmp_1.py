#coding=utf-8
import socket
import struct
import os

class ICMPSender:
    def calculate_checksum(self, data):
        # 计算校验和
        if len(data) % 2:
            data += b'\x00'

        checksum = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            checksum += word
            checksum = (checksum & 0xffff) + (checksum >> 16)

        return ~checksum & 0xffff

    def send_icmp_packet(self, src_ip, dst_ip):
        # 构建ICMP包
        icmp_type = 8
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
        sock.sendto(packet, (dst_ip, 0))

        # self.result_text.insert(rev.END, f"ICMP包已发送到 {dst_ip}\n")

def main():
    icmp_sender = ICMPSender()
    icmp_sender.send_icmp_packet("192.168.0.113", 99, "192.168.0.106", 92)

if __name__ == '__main__':
    main()
