@echo off
chcp 65001 >nul
cls
echo ============================================
echo 简PDF - Windows 打包脚本 v0.1.0
echo ============================================
echo.

echo [1/6] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请在 Anaconda Prompt 中运行此脚本
    pause
    exit /b 1
)
echo ✓ Python环境正常

echo.
echo [2/6] 安装/更新依赖...
pip install -q -U pdf2docx pyinstaller
echo ✓ 依赖安装完成

echo.
echo [3/6] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo ✓ 清理完成

echo.
echo [4/6] 开始打包...
echo    这可能需要1-2分钟，请稍候...
echo.

REM 检查是否有图标文件
if exist assets\icon.ico (
    echo    使用自定义图标...
    pyinstaller --name=简PDF --onefile --windowed --icon=assets\icon.ico src\main.py
) else (
    echo    使用默认图标...
    pyinstaller --name=简PDF --onefile --windowed src\main.py
)

if not exist dist\简PDF.exe (
    echo ❌ 打包失败！
    pause
    exit /b 1
)

echo ✓ 打包成功

echo.
echo [5/6] 检查文件信息...
for %%A in (dist\简PDF.exe) do (
    set size=%%~zA
    set /A sizeMB=%%~zA/1024/1024
)
echo    文件: dist\简PDF.exe
echo    大小: %sizeMB% MB
echo ✓ 检查完成

echo.
echo [6/6] 测试运行...
echo    正在启动程序测试...
start "" "dist\简PDF.exe"
timeout /t 3 >nul
echo ✓ 测试完成

echo.
echo ============================================
echo 🎉 打包完成！
echo ============================================
echo.
echo 📦 安装包位置: dist\简PDF.exe
echo 📊 文件大小: %sizeMB% MB
echo.
echo 💡 下一步:
echo    1. 测试 exe 是否正常运行
echo    2. 准备发布到 GitHub Release
echo.

pause