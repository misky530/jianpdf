# 简PDF

轻量级 PDF 转 Word 工具

## 特性

- ✅ 单文件转换
- ✅ 批量转换
- ✅ 本地转换，安全可靠
- ✅ 轻量级（~20MB）
- ✅ 无需安装额外依赖

## 快速开始

### 方式1: 下载安装包（推荐）

1. 下载 `简PDF.exe`
2. 双击运行
3. 选择PDF文件开始转换

### 方式2: 从源码运行
```bash
# 1. 克隆仓库
git clone https://gitcode.com/your-name/jianpdf.git
cd jianpdf

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python src/main.py
```

### 方式3: 自己打包
```bash
# Windows
build.bat

# Linux/Mac
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --name=简PDF --onefile --windowed src/main.py
```

## 使用说明

### 单文件转换
1. 点击"单文件转换"
2. 选择PDF文件
3. 选择保存位置
4. 等待转换完成

### 批量转换
1. 点击"批量转换"
2. 选择多个PDF文件（可多选）
3. 选择输出文件夹
4. 等待转换完成

## 系统要求

- Windows 10/11
- 无需安装其他软件

## 技术栈

- Python 3.9+
- pdf2docx
- Tkinter

## 更新日志

### v0.1.0 (2025-01-XX)
- 首次发布
- 支持单文件转换
- 支持批量转换
- GUI界面

## 许可证

MIT License

## 联系方式

- 微信: your_wechat
- 邮箱: your_email
- GitHub: https://github.com/your-name/jianpdf