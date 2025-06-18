# 音频降噪系统

这是一个完整的音频降噪项目，实现了音频信号采集、噪声添加、滤波处理和GUI界面展示等功能。

## 项目结构

```
audio_denoising_project/
│
├── main.py              # 主程序文件
├── gui.py               # GUI界面模块
├── requirements.txt     # 项目依赖
├── README.md           # 项目说明
├── install.sh          # Linux/macOS安装脚本
├── install.bat         # Windows安装脚本
├── .gitignore          # Git忽略文件
│
├── utils/              # 工具模块
│   ├── __init__.py
│   ├── noise.py        # 噪声生成模块
│   ├── filters.py      # 滤波器模块
│   └── analysis.py     # 信号分析模块
│
├── assets/             # 资源文件
│   └── input_audio.wav # 输入音频文件
│
├── output/             # 输出目录
│   ├── noisy_audio/    # 带噪音频文件
│   ├── filtered_audio/ # 滤波后音频文件
│   └── plots/          # 图表文件
│
└── chinese-beat-190047.wav  # 示例音频文件
```

## 快速开始

### 方法一：使用安装脚本（推荐）

#### Linux/macOS
```bash
# 克隆项目
git clone <your-repository-url>
cd audio_denoising_project

# 运行安装脚本
chmod +x install.sh
./install.sh
```

#### Windows
```cmd
# 克隆项目
git clone <your-repository-url>
cd audio_denoising_project

# 运行安装脚本
install.bat
```

### 方法二：手动安装

#### 1. 安装系统依赖

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-dev python3-pip
```

**CentOS/RHEL:**
```bash
sudo yum install -y portaudio-devel python3-devel python3-pip
```

**macOS:**
```bash
brew install portaudio
```

**Windows:**
- 通常不需要额外安装系统依赖

#### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate.bat  # Windows
```

#### 3. 安装Python依赖
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 使用方法

### 运行主程序
```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate.bat  # Windows

# 运行程序
python main.py
```

### GUI界面使用

1. 启动程序后会自动加载示例音频文件
2. 在控制面板中选择要添加的噪声类型
3. 调节噪声参数(SNR、频率范围等)
4. 点击相应的按钮添加噪声
5. 选择滤波器类型进行降噪处理
6. 使用播放功能对比音频效果
7. 查看时域和频域分析图表
8. 保存处理结果

## 功能特性

### 1. 信号采集
- 支持WAV格式音频文件读取
- 自动获取采样率和采样点数
- 支持立体声和单声道音频

### 2. 噪声添加
- **高斯白噪声**: 可调节信噪比(SNR)
- **窄带高斯噪声**: 指定频率范围(1000Hz-2000Hz)
- **单频干扰**: 指定频率的正弦波干扰(1500Hz)

### 3. 信号分析
- **时域分析**: 绘制时域波形图
- **频域分析**: 绘制频谱图(FFT)
- **对比分析**: 原始信号与处理信号的对比
- **性能指标**: 信噪比、峰值信噪比等

### 4. 滤波处理
- **低通滤波器**: 用于去除高频噪声
- **带通滤波器**: 保留指定频率范围
- **陷波滤波器**: 去除特定频率干扰
- **滤波器响应**: 显示幅频和相频响应

### 5. GUI界面
- 直观的图形用户界面
- 实时信号显示
- 音频播放功能
- 参数调节界面
- 结果保存功能

## 依赖说明

### Python依赖
- `numpy>=1.21.0`: 数值计算
- `scipy>=1.7.0`: 科学计算
- `matplotlib>=3.5.0`: 绘图
- `soundfile>=0.10.0`: 音频文件读写
- `sounddevice>=0.4.0`: 音频播放

### 系统依赖
- `portaudio19-dev`: 音频设备支持（Linux/macOS）
- `python3-dev`: Python开发头文件
- `python3-pip`: Python包管理器

## 技术实现

### 噪声生成
- 高斯白噪声: 基于正态分布生成
- 窄带噪声: 使用带通滤波器对白噪声进行滤波
- 单频干扰: 生成指定频率的正弦波

### 滤波器设计
- 巴特沃斯滤波器: 平坦的通带响应
- 切比雪夫滤波器: 更陡峭的过渡带
- 椭圆滤波器: 最优的过渡带特性
- 陷波滤波器: 专门用于去除单频干扰

### 信号分析
- FFT变换: 快速傅里叶变换
- 功率谱密度: 信号能量分布
- 频谱质心: 信号频率中心
- 频谱滚降: 信号带宽特征

## 性能指标

- **信噪比(SNR)**: 衡量信号与噪声的相对强度
- **峰值信噪比(PSNR)**: 评估信号质量
- **频谱质心**: 反映信号的主要频率成分
- **频谱滚降**: 表示信号的带宽特性

## 输出文件

程序运行后会在 `output/` 目录下生成以下文件：

### 音频文件
- `noisy_audio/`: 带噪音频文件
- `filtered_audio/`: 滤波后音频文件

### 图表文件
- `plots/`: 时域波形、频域谱、滤波器响应等图表

## 故障排除

### 常见问题

1. **PortAudio库未找到**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install portaudio19-dev
   
   # CentOS/RHEL
   sudo yum install portaudio-devel
   
   # macOS
   brew install portaudio
   ```

2. **Python包安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 重新安装依赖
   pip install -r requirements.txt
   ```

3. **音频播放无声音**
   - 检查系统音频设备
   - 确保音量设置正确
   - 尝试使用不同的音频后端

4. **GUI界面无法显示**
   - 确保安装了tkinter
   - 检查X11转发设置（远程连接时）

## 扩展功能

项目支持以下扩展功能：
- 自适应滤波器(LMS算法)
- 维纳滤波器
- 小波变换降噪
- 频谱减法
- 多通道处理

## 注意事项

1. 确保音频文件格式为WAV
2. 采样率建议为44.1kHz或48kHz
3. 音频时长建议不超过10分钟
4. 滤波参数需要根据具体音频特征调整
5. 立体声音频会自动处理所有声道

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过GitHub Issues联系。 