# 聊天客户端
import socket
import tkinter as tk
def connect_to_server():
    global client_socket
    pass
    try:
        client_socket = socket.socket()
        client_socket.connect((dst_ip.get(), int(dst_port.get())))
        chat_listbox.insert(tk.END, "连接到服务器")
    except Exception as e:
        chat_listbox.insert(tk.END, "连接失败")
def send_message():
    msg = message_entry.get()
    if msg:
        chat_listbox.insert(tk.END, f"我: {msg}")
        client_socket.send(msg.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        chat_listbox.insert(tk.END, f"服务器: {response}")
        message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Chat Client")
root.geometry("400x300")
# 使用columnspan=2使其跨越两个列
chat_listbox = tk.Listbox(root)
chat_listbox.pack()
label_msg = tk.Label(root, text="消息:")
label_msg.pack()
message_entry = tk.Entry(root)
message_entry.pack()
label_ip = tk.Label(root, text="目的IP:")
label_ip.pack()
dst_ip = tk.Entry(root)
dst_ip.pack()
label_port = tk.Label(root, text="目的端口:")
label_port.pack()
dst_port = tk.Entry(root)
dst_port.pack()

connect_button = tk.Button(root, text="Connect", command=connect_to_server)
connect_button.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()
root.mainloop()