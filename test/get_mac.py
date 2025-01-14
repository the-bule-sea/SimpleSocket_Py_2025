import re
import os

# def get_mac_address():
#     mac = ':'.join(re.findall('..', '%012x' % os.getpid()))
#     return mac
#
# if __name__ == '__main__':
#     print(get_mac_address())

import uuid

def get_mac_address():
    mac = uuid.getnode()  # 获取MAC地址
    mac_address = ':'.join(f'{(mac >> i) & 0xff:02x}' for i in range(40, -1, -8))
    return mac_address

print("本机 MAC 地址:", get_mac_address())
if __name__ == '__main__':
    get_mac_address()

