"""
简PDF - GUI界面模块
使用 Tkinter 构建
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from converter import PDFConverter


class JianPDFApp:
    """简PDF 主应用程序"""

    def __init__(self, root):
        self.root = root
        self.root.title("简PDF v0.1.0 - 轻量级PDF转Word工具")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        # 设置窗口居中
        self.center_window()

        # 初始化转换器
        self.converter = PDFConverter()
        self.converter.progress_callback = self.update_progress

        # 创建界面
        self.create_widgets()

        # 设置样式
        self.setup_styles()

    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        """设置UI样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置进度条样式
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor='#e0e0e0',
                        background='#1890ff',
                        bordercolor='#1890ff',
                        lightcolor='#1890ff',
                        darkcolor='#1890ff')

    def create_widgets(self):
        """创建所有界面组件"""

        # ========== 顶部标题栏 ==========
        header_frame = tk.Frame(self.root, bg="#1890ff", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="简PDF",
            font=("Microsoft YaHei", 32, "bold"),
            fg="white",
            bg="#1890ff"
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = tk.Label(
            header_frame,
            text="轻量级 PDF 转 Word 工具  |  本地转换  |  安全可靠",
            font=("Microsoft YaHei", 10),
            fg="white",
            bg="#1890ff"
        )
        subtitle_label.pack()

        # ========== 主体内容区 ==========
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === 功能按钮区 ===
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=20)

        # 单文件转换按钮
        self.single_btn = tk.Button(
            button_frame,
            text="📄 单文件转换",
            command=self.convert_single_file,
            width=16,
            height=2,
            bg="#1890ff",
            fg="white",
            font=("Microsoft YaHei", 13, "bold"),
            cursor="hand2",
            relief="flat",
            activebackground="#096dd9",
            activeforeground="white"
        )
        self.single_btn.grid(row=0, column=0, padx=12)

        # 批量转换按钮
        self.batch_btn = tk.Button(
            button_frame,
            text="📁 批量转换",
            command=self.convert_batch_files,
            width=16,
            height=2,
            bg="#52c41a",
            fg="white",
            font=("Microsoft YaHei", 13, "bold"),
            cursor="hand2",
            relief="flat",
            activebackground="#389e0d",
            activeforeground="white"
        )
        self.batch_btn.grid(row=0, column=1, padx=12)

        # === 进度显示区 ===
        progress_frame = tk.Frame(main_frame, bg="white")
        progress_frame.pack(pady=15, fill="x")

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=680,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack()

        # 状态标签
        self.status_label = tk.Label(
            progress_frame,
            text="就绪 - 请选择 PDF 文件开始转换",
            font=("Microsoft YaHei", 10),
            fg="#666",
            bg="white"
        )
        self.status_label.pack(pady=10)

        # === 日志显示区 ===
        log_frame = tk.LabelFrame(
            main_frame,
            text="  转换日志  ",
            font=("Microsoft YaHei", 10, "bold"),
            fg="#333",
            bg="white",
            relief="solid",
            borderwidth=1
        )
        log_frame.pack(fill="both", expand=True, pady=10)

        # 创建滚动条
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        # 日志文本框
        self.log_text = tk.Text(
            log_frame,
            height=10,
            font=("Consolas", 9),
            bg="#f7f7f7",
            fg="#333",
            yscrollcommand=scrollbar.set,
            wrap="word",
            relief="flat",
            padx=10,
            pady=10
        )
        self.log_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)

        # 初始日志
        self.log("欢迎使用简PDF！", "info")
        self.log("选择单文件转换或批量转换开始使用", "info")

        # ========== 底部信息栏 ==========
        footer_frame = tk.Frame(self.root, bg="#f5f5f5", height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="简PDF v0.1.0  |  本地转换，安全可靠  |  技术支持: your_contact",
            font=("Microsoft YaHei", 8),
            fg="#999",
            bg="#f5f5f5"
        )
        footer_label.pack(pady=12)

    def log(self, message, level="info"):
        """
        添加日志信息

        Args:
            message: 日志内容
            level: 日志级别 (info/success/error/warning)
        """
        # 日志前缀
        prefixes = {
            "info": "ℹ",
            "success": "✓",
            "error": "✗",
            "warning": "⚠"
        }
        prefix = prefixes.get(level, "•")

        # 插入日志
        self.log_text.insert("end", f"{prefix} {message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()

    def update_progress(self, progress, filename, current=None, total=None):
        """
        更新进度显示

        Args:
            progress: 进度百分比 (0-100)
            filename: 当前文件名
            current: 当前文件序号
            total: 总文件数
        """
        self.progress_var.set(progress)

        if current and total:
            status = f"正在转换: {filename}  ({current}/{total}) - {progress}%"
        else:
            status = f"正在转换: {filename} - {progress}%"

        self.status_label.config(text=status)
        self.root.update_idletasks()

    def set_buttons_state(self, state):
        """
        设置按钮状态

        Args:
            state: "normal" 或 "disabled"
        """
        self.single_btn.config(state=state)
        self.batch_btn.config(state=state)

    def convert_single_file(self):
        """单文件转换"""
        # 选择PDF文件
        pdf_file = filedialog.askopenfilename(
            title="选择 PDF 文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")],
            parent=self.root
        )

        if not pdf_file:
            return

        # 询问保存位置
        default_name = os.path.basename(pdf_file).rsplit('.', 1)[0] + '.docx'
        output_file = filedialog.asksaveasfilename(
            title="保存为",
            defaultextension=".docx",
            initialfile=default_name,
            filetypes=[("Word文档", "*.docx"), ("所有文件", "*.*")],
            parent=self.root
        )

        if not output_file:
            return

        # 开始转换
        self.log(f"开始转换: {os.path.basename(pdf_file)}", "info")
        self.progress_var.set(0)
        self.set_buttons_state("disabled")

        # 在新线程中执行转换
        thread = threading.Thread(
            target=self._do_single_convert,
            args=(pdf_file, output_file),
            daemon=True
        )
        thread.start()

    def _do_single_convert(self, pdf_file, output_file):
        """执行单文件转换（后台线程）"""
        self.status_label.config(text="转换中，请稍候...")
        self.progress_var.set(50)

        # 执行转换
        success, result = self.converter.convert_single(pdf_file, output_file)

        # 更新UI
        self.root.after(0, self._single_convert_complete, success, result, output_file)

    def _single_convert_complete(self, success, result, output_file):
        """单文件转换完成后的UI更新"""
        if success:
            self.progress_var.set(100)
            self.status_label.config(text="转换完成！")
            self.log(f"转换成功: {os.path.basename(output_file)}", "success")

            # 询问是否打开文件
            if messagebox.askyesno(
                    "转换成功",
                    f"转换完成！\n\n保存位置:\n{output_file}\n\n是否立即打开文件？",
                    parent=self.root
            ):
                try:
                    os.startfile(output_file)
                except Exception as e:
                    self.log(f"打开文件失败: {str(e)}", "error")
        else:
            self.progress_var.set(0)
            self.status_label.config(text="转换失败")
            self.log(f"转换失败: {result}", "error")
            messagebox.showerror("转换失败", f"转换失败:\n{result}", parent=self.root)

        self.set_buttons_state("normal")

    def convert_batch_files(self):
        """批量转换"""
        # 选择多个PDF文件
        pdf_files = filedialog.askopenfilenames(
            title="选择多个 PDF 文件（可多选）",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")],
            parent=self.root
        )

        if not pdf_files:
            return

        # 选择输出目录
        output_dir = filedialog.askdirectory(
            title="选择输出文件夹",
            parent=self.root
        )

        if not output_dir:
            return

        # 开始批量转换
        self.log("\n" + "=" * 60, "info")
        self.log(f"开始批量转换: 共 {len(pdf_files)} 个文件", "info")
        self.log(f"输出目录: {output_dir}", "info")
        self.log("=" * 60, "info")

        self.progress_var.set(0)
        self.set_buttons_state("disabled")

        # 在新线程中执行批量转换
        thread = threading.Thread(
            target=self._do_batch_convert,
            args=(pdf_files, output_dir),
            daemon=True
        )
        thread.start()

    def _do_batch_convert(self, pdf_files, output_dir):
        """执行批量转换（后台线程）"""
        results = self.converter.convert_batch(pdf_files, output_dir)

        # 更新UI
        self.root.after(0, self._batch_convert_complete, results, output_dir)

    def _batch_convert_complete(self, results, output_dir):
        """批量转换完成后的UI更新"""
        # 统计结果
        success_count = sum(1 for r in results if r['success'])
        fail_count = len(results) - success_count

        # 显示详细日志
        self.log("\n" + "=" * 60, "info")
        self.log("批量转换完成！", "success")
        self.log(f"总数: {len(results)}  |  成功: {success_count}  |  失败: {fail_count}", "info")
        self.log("=" * 60, "info")

        for r in results:
            if r['success']:
                self.log(f"{r['file']} → 转换成功", "success")
            else:
                self.log(f"{r['file']} → {r['error']}", "error")

        self.status_label.config(text=f"批量转换完成！成功 {success_count} 个，失败 {fail_count} 个")
        self.progress_var.set(100)

        # 显示完成对话框
        msg = (
            f"批量转换完成！\n\n"
            f"成功: {success_count} 个\n"
            f"失败: {fail_count} 个\n\n"
            f"输出目录:\n{output_dir}"
        )

        if messagebox.askyesno("转换完成", msg + "\n\n是否打开输出文件夹？", parent=self.root):
            try:
                os.startfile(output_dir)
            except Exception as e:
                self.log(f"打开文件夹失败: {str(e)}", "error")

        self.set_buttons_state("normal")


def create_app():
    """创建并返回应用程序"""
    root = tk.Tk()
    app = JianPDFApp(root)
    return root, app