# client.py
import tkinter as tk
import socket
import uuid


def connect_to_server():
    global s, host, port
    host = entry_host.get()
    port = int(entry_port.get())
    s = socket.socket()
    s.connect((host, port))
    status_label.config(text=f"Connected to {host}:{port}")
    receive_messages()

def send_message():
    message = entry_message.get()
    if message:
        s.send(message.encode('utf-8'))
        chat_box.insert(tk.END, f"Client: {message}\n")
        entry_message.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            incoming_message = s.recv(1024).decode('utf-8')
            if not incoming_message:
                break
            chat_box.insert(tk.END, f"Server: {incoming_message}\n")
        except:
            break

# 获取本机数据
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x','').upper()
    mac = '-'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
    return mac

def get_hostname():
    return socket.gethostname()


# def creat_window():
root = tk.Tk()
root.title("Socket Client")

# 信息框
frame_info = tk.Frame(root)
frame_info.pack(pady=10)

label_ip = tk.Label(frame_info, text=f"IP Address: {get_ip_address()}")
label_ip.grid(row=0, column=0, padx=5)
label_mac = tk.Label(frame_info, text=f"MAC Address: {get_mac_address()}")
label_mac.grid(row=0, column=1, padx=5)
label_hostname = tk.Label(frame_info, text=f"Hostname: {get_hostname()}")
label_hostname.grid(row=0, column=2, padx=5)

# 输入框和按钮
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_host = tk.Label(frame_input, text="Host:")
label_host.grid(row=0, column=0, padx=5)
entry_host = tk.Entry(frame_input)
entry_host.grid(row=0, column=1, padx=5)

label_port = tk.Label(frame_input, text="Port:")
label_port.grid(row=0, column=2, padx=5)
entry_port = tk.Entry(frame_input)
entry_port.grid(row=0, column=3, padx=5)

button_connect = tk.Button(frame_input, text="Connect", command=connect_to_server)
button_connect.grid(row=0, column=4, padx=5)

status_label = tk.Label(root, text="Not connected")
status_label.pack(pady=5)

# 聊天框
chat_box = tk.Text(root, height=15, width=50)
chat_box.pack(pady=10)

# 消息输入框
frame_message = tk.Frame(root)
frame_message.pack(pady=10)

entry_message = tk.Entry(frame_message, width=40)
entry_message.grid(row=0, column=0, padx=5)

button_send = tk.Button(frame_message, text="Send", command=send_message)
button_send.grid(row=0, column=1, padx=5)

root.mainloop()
