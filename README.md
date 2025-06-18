最简单的环境配置（仅限python）
在本项目中仅需在项目根目录执行 source exp_venv/bin/activate 

venv（Python 标准库）
这是 Python 自带的虚拟环境工具，从 Python 3.3 开始作为标准库的一部分。它的使用非常简单，适合一般的 Python 项目。

安装和使用：
确保你安装了 Python 3.x。

(Ubuntu linux)
sudo apt update
sudo apt install python3-venv

创建虚拟环境：
python3 -m venv myenv

激活虚拟环境：
source myenv/bin/activate

安装依赖：
pip install <package_name>

退出虚拟环境：
deactivate


优点：
无需额外安装任何工具，venv 是 Python 的标准工具。
轻量级，适合简单的项目。

缺点：
仅适用于单个 Python 版本，不能轻松管理多个版本的 Python 环境。