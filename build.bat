@echo off
chcp 65001 >nul
echo ============================================
echo 简PDF - Windows 打包脚本
echo ============================================
echo.

echo [1/5] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo [2/5] 安装依赖...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [3/5] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo.
echo [4/5] 开始打包...
echo 这可能需要几分钟，请耐心等待...
echo.

pyinstaller --name=简PDF --onefile --windowed --icon=assets/icon.ico src/main.py 2>nul
if not exist assets\icon.ico (
    echo 提示: 未找到icon.ico，使用默认图标
    pyinstaller --name=简PDF --onefile --windowed src/main.py
)

echo.
echo [5/5] 打包完成！
echo.
echo ============================================
echo 安装包位置: dist\简PDF.exe
echo 文件大小:
dir dist\简PDF.exe | find "简PDF.exe"
echo ============================================
echo.
echo 测试运行请执行: dist\简PDF.exe
echo.

pause