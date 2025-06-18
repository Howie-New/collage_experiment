@echo off
REM 音频降噪项目安装脚本 (Windows版本)

echo === 音频降噪项目安装脚本 ===
echo 正在检测Python环境...

REM 检测Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python
    echo 请先安装Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 检测到Python环境
echo.

echo 正在创建虚拟环境...
python -m venv venv

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 升级pip...
python -m pip install --upgrade pip

echo 安装Python依赖...
pip install -r requirements.txt

echo.
echo === 安装完成 ===
echo 使用方法:
echo 1. 激活虚拟环境: venv\Scripts\activate.bat
echo 2. 运行主程序: python main.py
echo 3. 或运行GUI界面: python main.py (会自动启动GUI)
echo.
echo 项目结构:
echo - main.py: 主程序
echo - gui.py: GUI界面
echo - utils/: 工具模块
echo - output/: 输出目录
echo.
echo 更多信息请查看 README.md
pause 