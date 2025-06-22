clone project后 cd 进入到对应的子项目目录中
第一件事：
创建自己本地运行python项目的虚拟环境
venv（Python 标准库）
这是 Python 自带的虚拟环境工具，从 Python 3.3 开始作为标准库的一部分。它的使用非常简单，适合一般的 Python 项目。

安装和使用：
确保你安装了 Python 3.x。
查看
pip install --upgrade pip
python --version
pip --version

创建虚拟环境：
(Linxu)python3 -m venv my_venv
(Windows)python -m venv my_venv

激活虚拟环境：
(linux)source my_venv/bin/activate
(Windows)my_venv/Scripts/activate
💡 第一次使用 PowerShell 激活可能遇到权限问题
你可能会看到这个错误：
execution of scripts is disabled on this system

解决方法：以管理员身份运行 PowerShell，然后执行：
Set-ExecutionPolicy RemoteSigned

安装依赖：
pip install <package_name>

退出虚拟环境：
deactivate


优点：
无需额外安装任何工具，venv 是 Python 的标准工具。
轻量级，适合简单的项目。

缺点：
仅适用于单个 Python 版本，不能轻松管理多个版本的 Python 环境。


当进入你本地的venv后，执行：
pip install -r .\requirements.txt

当你在安装了新的依赖之后，可以执行：
pip freeze > requirements.txt
方便其他人也能知道最新的项目的依赖情况