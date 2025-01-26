import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Tkinter Example")
# 第一个是指窗口的宽度，第二个窗口的高度，第三个窗口左上点离左屏幕边界距离，第四个窗口左上点离上面屏幕边界距离
root.geometry("900x600+300+50")

top = tk.Menu(root)

root.config(menu=top)

# 添加标签
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

# 运行主循环
root.mainloop()
