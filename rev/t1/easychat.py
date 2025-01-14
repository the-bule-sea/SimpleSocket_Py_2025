import tkinter as tk
def send_message():
    message = message_entry.get()  # 获取输入框中的消息
    if message:
        # 在聊天框中显示消息
        chat_listbox.insert(tk.END, f"你: {message}")
        # 清空输入框
        message_entry.delete(0, tk.END)
# 初始化
root = tk.Tk()
root.title("简易聊天室")
root.geometry("400x300")
# 创建一个容器
chat_frame = tk.Frame(root)
chat_frame.pack(fill=tk.BOTH, expand=True)
chat_listbox = tk.Listbox(chat_frame)
chat_listbox.pack(fill=tk.BOTH, expand=True)
# 收集用户输入的单行文本
message_entry = tk.Entry(root)
message_entry.pack(fill=tk.X, padx=5, pady=5)

send_button = tk.Button(root, text="发送", command=send_message)
send_button.pack(pady=5)
root.mainloop()
