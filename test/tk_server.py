# server.py
import tkinter as tk
import socket
import threading

def start_server():
    global s, conn, addr
    # host = socket.gethostname()
    # print("host is:", host)
    host = "114514"
    port = 8080
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    conn, addr = s.accept()
    status_label.config(text=f"Connected to {addr}")
    receive_messages()

def send_message():
    message = entry_message.get()
    if message:
        conn.send(message.encode('utf-8'))
        chat_box.insert(tk.END, f"Server: {message}\n")
        entry_message.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            incoming_message = conn.recv(1024).decode('utf-8')
            if not incoming_message:
                break
            chat_box.insert(tk.END, f"Client: {incoming_message}\n")
        except:
            break

root = tk.Tk()
root.title("Socket Server")



# 启动按钮
button_start = tk.Button(root, text="Start Server", command=start_server)
button_start.pack(pady=10)

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
