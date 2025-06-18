#!/bin/bash

# 音频降噪项目安装脚本
# 适用于 Ubuntu/Debian 系统

echo "=== 音频降噪项目安装脚本 ==="
echo "正在检测系统类型..."

# 检测操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        echo "检测到 Ubuntu/Debian 系统"
        echo "正在安装系统依赖..."
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-dev python3-pip
    elif command -v yum &> /dev/null; then
        echo "检测到 CentOS/RHEL 系统"
        echo "正在安装系统依赖..."
        sudo yum install -y portaudio-devel python3-devel python3-pip
    else
        echo "警告: 无法检测到支持的包管理器"
        echo "请手动安装 portaudio19-dev 或 portaudio-devel"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "检测到 macOS 系统"
    if command -v brew &> /dev/null; then
        echo "正在安装系统依赖..."
        brew install portaudio
    else
        echo "警告: 未检测到 Homebrew"
        echo "请先安装 Homebrew: https://brew.sh/"
        echo "然后运行: brew install portaudio"
    fi
else
    echo "警告: 不支持的操作系统类型: $OSTYPE"
    echo "请手动安装 portaudio 库"
fi

echo ""
echo "正在创建虚拟环境..."
python3 -m venv venv

echo "激活虚拟环境..."
source venv/bin/activate

echo "升级 pip..."
pip install --upgrade pip

echo "安装 Python 依赖..."
pip install -r requirements.txt

echo ""
echo "=== 安装完成 ==="
echo "使用方法:"
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 运行主程序: python main.py"
echo "3. 或运行GUI界面: python main.py (会自动启动GUI)"
echo ""
echo "项目结构:"
echo "- main.py: 主程序"
echo "- gui.py: GUI界面"
echo "- utils/: 工具模块"
echo "- output/: 输出目录"
echo ""
echo "更多信息请查看 README.md" 