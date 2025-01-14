import tkinter
import socket
import uuid


def get_ip_address():
    hostname = socket.gethostname()
    ip_add = socket.gethostbyname(hostname)
    return ip_add

def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
    return mac

def get_hostname():
    return socket.gethostname()

def create_window():
    root = tkinter.Tk()
    root.title("本机信息")
    # 获取信息
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    hostname = get_hostname()
    # 创建文本框
    text_box = tkinter.Text(root, height=10, width=50)
    text_box.pack(pady= 10)
    # 写入信息
    text_box.insert(tkinter.END, "IP地址: " + ip_address + "\n")
    text_box.insert(tkinter.END, "MAC地址: " + mac_address + "\n")
    text_box.insert(tkinter.END, "主机名: " + hostname + "\n")
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    create_window()
