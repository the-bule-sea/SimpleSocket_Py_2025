import tkinter as tk
import socket
def get_info():
    try:
        # 主机名+获取IP地址
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        info_listbox.insert(tk.END, f"主机名: {hostname}")
        info_listbox.insert(tk.END, f"IP地址: {ip}")
    except Exception as e:
        info_listbox.insert(tk.END, f"获取信息失败: {str(e)}")
root = tk.Tk() # 生成一个主窗口对象
root.geometry('300x200')  # 大小
root.title('信息获取小工具')  # 标题
# Listbox是一个列表控件，用于显示多个项目
info_listbox = tk.Listbox(root)
info_listbox.pack()  # 将Listbox控件添加到主窗口中
# 创建按钮
get_info_button = tk.Button(root, text='获取信息', command=get_info)
get_info_button.pack()
# 进入消息循环
root.mainloop()