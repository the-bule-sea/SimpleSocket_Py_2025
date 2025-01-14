#coding=utf-8
import socket
import struct

class UDPSender:
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

    def send_udp_packet(self, src_ip, src_port, dst_ip, dst_port):
        payload = b"Hello, World!"
        length = 8 + len(payload)  # UDP头部固定长度8字节 + 数据长度
        checksum = 0

        # 构建UDP头部
        udp_header = struct.pack("!HHHH", src_port, dst_port, length, checksum)

        # 伪头部用于校验和计算
        pseudo_header = struct.pack(
            "!4s4sBBH",
            socket.inet_aton(src_ip),
            socket.inet_aton(dst_ip),
            0,
            socket.IPPROTO_UDP,
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
            print(f"UDP包已发送到 {dst_ip}:{dst_port}\n")
        except Exception as e:
            print(f"发送UDP包失败: {e}")
        finally:
            sock.close()

def main():
    udp_sender = UDPSender()
    udp_sender.send_udp_packet("192.168.98.140", 99, "192.168.98.200", 92)

if __name__ == '__main__':
    main()
