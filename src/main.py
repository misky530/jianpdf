"""
简PDF - 程序入口
轻量级 PDF 转 Word 工具
"""

import sys
import os

# 添加当前目录到路径（打包后需要）
if getattr(sys, 'frozen', False):
    # 打包后的exe运行
    application_path = sys._MEIPASS
else:
    # 开发环境运行
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from gui import create_app


def main():
    """主函数"""
    try:
        root, app = create_app()
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"程序启动失败:\n{str(e)}\n\n{traceback.format_exc()}"

        # 尝试显示错误对话框
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("错误", error_msg)
        except:
            print(error_msg)

        sys.exit(1)


if __name__ == "__main__":
    main()