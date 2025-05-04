import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import pyperclip
from typing import Optional


class AutoInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动输入工具")
        self.root.geometry("800x900")
        self.root.minsize(800, 900)

        # 设置主题色
        self.primary_color = "#2196F3"
        self.bg_color = "#F5F5F5"
        self.text_color = "#333333"

        self.root.config(bg=self.bg_color)
        self.setup_ui()
        self.setup_bindings()
        self.setup_watermark()

    def setup_watermark(self):
        """设置水印"""
        # 创建水印标签
        self.watermark = tk.Label(
            self.root,
            text="田某人原创，请勿到处传播",
            font=("Microsoft YaHei UI", 9),
            fg="#999999",
            bg=self.bg_color
        )
        # 将水印放在右下角
        self.watermark.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def setup_ui(self):
        """设置UI界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(
            title_frame,
            text="自动输入工具",
            font=("Microsoft YaHei UI", 24, "bold"),
            foreground=self.primary_color
        )
        title_label.pack(side=tk.LEFT)

        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="设置", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 20))

        # 延迟设置
        delay_frame = ttk.Frame(settings_frame)
        delay_frame.pack(fill=tk.X, pady=5)

        ttk.Label(delay_frame, text="字符间隔(秒):").pack(side=tk.LEFT, padx=5)
        self.delay_var = tk.StringVar(value="0.05")
        delay_entry = ttk.Entry(delay_frame, textvariable=self.delay_var, width=10)
        delay_entry.pack(side=tk.LEFT, padx=5)

        # 文本输入区域
        input_frame = ttk.LabelFrame(main_frame, text="输入文本", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # 使用scrolledtext替代普通Text
        self.textbox = scrolledtext.ScrolledText(
            input_frame,
            height=15,
            width=70,
            font=("Microsoft YaHei UI", 11),
            wrap=tk.WORD
        )
        self.textbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # 清空按钮
        clear_button = ttk.Button(
            button_frame,
            text="清空文本",
            command=self.clear_text,
            style="Secondary.TButton"
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        # 开始输入按钮
        self.input_button = ttk.Button(
            button_frame,
            text="开始输入",
            command=self.start_input,
            style="Primary.TButton"
        )
        self.input_button.pack(side=tk.RIGHT, padx=5)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Microsoft YaHei UI", 9),
            foreground="#666666"
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))

        # 设置样式
        self.setup_styles()

    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()

        # 主要按钮样式
        style.configure(
            "Primary.TButton",
            font=("Microsoft YaHei UI", 10),
            padding=10
        )

        # 次要按钮样式
        style.configure(
            "Secondary.TButton",
            font=("Microsoft YaHei UI", 10),
            padding=10
        )

    def setup_bindings(self):
        """设置快捷键绑定"""
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-Return>', lambda e: self.start_input())
        # 为文本框单独绑定Ctrl+V事件
        self.textbox.bind('<Control-v>', self.paste_text)

    def clear_text(self):
        """清空文本框"""
        self.textbox.delete("1.0", tk.END)
        self.status_var.set("文本已清空")

    def paste_text(self, event=None):
        """处理粘贴操作"""
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                # 如果有选中的文本，则替换选中部分
                try:
                    sel_start = self.textbox.index("sel.first")
                    sel_end = self.textbox.index("sel.last")
                    self.textbox.delete(sel_start, sel_end)
                    self.textbox.insert(sel_start, clipboard_text)
                except tk.TclError:  # 没有选中文本
                    # 在当前光标位置插入
                    current_pos = self.textbox.index("insert")
                    self.textbox.insert(current_pos, clipboard_text)
                self.status_var.set("文本已粘贴")
        except Exception as e:
            messagebox.showerror("错误", f"粘贴失败: {str(e)}")

    def type_text(self, text: str, delay: float):
        """逐字输入文本"""
        # 删除每行前面的空格
        lines = text.split('\n')
        cleaned_lines = [line.lstrip() for line in lines]
        cleaned_text = '\n'.join(cleaned_lines)

        for char in cleaned_text:
            pyautogui.typewrite(char)
            time.sleep(delay)

        # 删除光标后的所有内容
        pyautogui.hotkey('ctrl', 'shift', 'end')
        pyautogui.press('delete')

    def start_input(self):
        """开始输入文本"""
        str_in = self.textbox.get("1.0", "end-1c")

        if not str_in.strip():
            messagebox.showwarning("警告", "请输入要自动输入的文本")
            return

        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                raise ValueError("延迟时间不能为负数")

            self.status_var.set("准备输入...")
            messagebox.showinfo("提示", "3秒后开始输入，请将光标移动到目标位置")
            time.sleep(3)

            # 逐字输入
            self.type_text(str_in, delay)

            self.status_var.set("输入完成")
            messagebox.showinfo("成功", "文本输入完成")
        except ValueError as e:
            messagebox.showerror("错误", "请输入有效的延迟时间")
        except Exception as e:
            messagebox.showerror("错误", f"输入失败: {str(e)}")
            self.status_var.set("输入失败")


def main():
    root = tk.Tk()
    app = AutoInputApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
