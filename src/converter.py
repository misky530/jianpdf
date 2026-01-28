"""
PDF转Word转换器核心模块
基于 pdf2docx 库
"""

from pdf2docx import Converter
import os


class PDFConverter:
    """PDF转Word转换器"""

    def __init__(self):
        self.current_file = ""
        self.progress_callback = None

    def convert_single(self, pdf_path, output_path=None):
        """
        单文件转换

        Args:
            pdf_path: PDF文件路径
            output_path: 输出docx路径（可选，默认同名同目录）

        Returns:
            (success: bool, result: str) - 成功返回输出路径，失败返回错误信息
        """
        try:
            # 验证输入文件
            if not os.path.exists(pdf_path):
                return False, "文件不存在"

            if not pdf_path.lower().endswith('.pdf'):
                return False, "不是PDF文件"

            # 确定输出路径
            if output_path is None:
                output_path = pdf_path.rsplit('.', 1)[0] + '.docx'

            # 创建转换器并转换
            cv = Converter(pdf_path)
            cv.convert(output_path)
            cv.close()

            # 验证输出文件
            if os.path.exists(output_path):
                return True, output_path
            else:
                return False, "转换失败：输出文件未生成"

        except Exception as e:
            return False, f"转换错误: {str(e)}"

    def convert_batch(self, pdf_files, output_dir=None):
        """
        批量转换

        Args:
            pdf_files: PDF文件路径列表
            output_dir: 输出目录（可选，默认原文件目录）

        Returns:
            list - 转换结果列表，每项包含文件名、是否成功、输出路径或错误信息
        """
        results = []
        total = len(pdf_files)

        for index, pdf_path in enumerate(pdf_files, 1):
            self.current_file = os.path.basename(pdf_path)

            # 更新进度（如果设置了回调函数）
            if self.progress_callback:
                progress = int((index / total) * 100)
                self.progress_callback(progress, self.current_file, index, total)

            # 确定输出路径
            if output_dir:
                # 使用指定的输出目录
                filename = os.path.basename(pdf_path).rsplit('.', 1)[0] + '.docx'
                output_path = os.path.join(output_dir, filename)
            else:
                # 使用原文件所在目录
                output_path = pdf_path.rsplit('.', 1)[0] + '.docx'

            # 执行转换
            success, result = self.convert_single(pdf_path, output_path)

            # 记录结果
            results.append({
                'file': self.current_file,
                'input': pdf_path,
                'success': success,
                'output': result if success else None,
                'error': result if not success else None
            })

        return results

    def get_file_info(self, pdf_path):
        """
        获取PDF文件信息

        Args:
            pdf_path: PDF文件路径

        Returns:
            dict - 文件信息
        """
        try:
            file_size = os.path.getsize(pdf_path)
            file_size_mb = file_size / (1024 * 1024)

            return {
                'name': os.path.basename(pdf_path),
                'path': pdf_path,
                'size': f"{file_size_mb:.2f} MB",
                'exists': True
            }
        except Exception as e:
            return {
                'name': os.path.basename(pdf_path),
                'path': pdf_path,
                'error': str(e),
                'exists': False
            }