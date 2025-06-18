#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI界面模块
使用tkinter实现音频降噪的可视化界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sounddevice as sd
import soundfile as sf
from pathlib import Path
import threading
import time

from utils.analysis import plot_time_domain, plot_frequency_domain, plot_comparison, calculate_snr
from utils.noise import add_gaussian_noise, add_narrowband_noise, add_single_frequency_interference
from utils.filters import design_lowpass_filter, design_bandpass_filter, design_notch_filter

class AudioDenoisingGUI:
    """音频降噪GUI界面"""
    
    def __init__(self, processor=None):
        self.processor = processor
        self.root = tk.Tk()
        self.root.title("音频降噪系统")
        self.root.geometry("1200x800")
        
        # 音频数据
        self.audio_data = None
        self.sample_rate = None
        self.noisy_signals = {}
        self.filtered_signals = {}
        
        # 创建界面
        self.create_widgets()
        
        # 如果有处理器，加载数据
        if self.processor and self.processor.audio_data is not None:
            self.load_processor_data()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="音频降噪系统", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 文件加载
        file_frame = ttk.LabelFrame(control_frame, text="文件操作", padding="5")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="加载音频文件", command=self.load_audio_file).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="保存处理结果", command=self.save_results).pack(fill=tk.X, pady=2)
        
        # 噪声添加
        noise_frame = ttk.LabelFrame(control_frame, text="噪声添加", padding="5")
        noise_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 高斯白噪声
        ttk.Label(noise_frame, text="高斯白噪声 SNR (dB):").pack(anchor=tk.W)
        self.gaussian_snr_var = tk.StringVar(value="10")
        ttk.Entry(noise_frame, textvariable=self.gaussian_snr_var, width=10).pack(fill=tk.X, pady=2)
        ttk.Button(noise_frame, text="添加高斯白噪声", 
                  command=lambda: self.add_noise('gaussian')).pack(fill=tk.X, pady=2)
        
        # 窄带噪声
        ttk.Label(noise_frame, text="窄带噪声频率范围:").pack(anchor=tk.W)
        narrowband_frame = ttk.Frame(noise_frame)
        narrowband_frame.pack(fill=tk.X, pady=2)
        
        self.low_freq_var = tk.StringVar(value="1000")
        self.high_freq_var = tk.StringVar(value="2000")
        ttk.Entry(narrowband_frame, textvariable=self.low_freq_var, width=8).pack(side=tk.LEFT)
        ttk.Label(narrowband_frame, text="-").pack(side=tk.LEFT)
        ttk.Entry(narrowband_frame, textvariable=self.high_freq_var, width=8).pack(side=tk.LEFT)
        ttk.Label(narrowband_frame, text="Hz").pack(side=tk.LEFT)
        
        ttk.Button(noise_frame, text="添加窄带噪声", 
                  command=lambda: self.add_noise('narrowband')).pack(fill=tk.X, pady=2)
        
        # 单频干扰
        ttk.Label(noise_frame, text="单频干扰频率 (Hz):").pack(anchor=tk.W)
        self.single_freq_var = tk.StringVar(value="1500")
        ttk.Entry(noise_frame, textvariable=self.single_freq_var, width=10).pack(fill=tk.X, pady=2)
        ttk.Button(noise_frame, text="添加单频干扰", 
                  command=lambda: self.add_noise('single_freq')).pack(fill=tk.X, pady=2)
        
        # 滤波处理
        filter_frame = ttk.LabelFrame(control_frame, text="滤波处理", padding="5")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(filter_frame, text="应用低通滤波器", 
                  command=lambda: self.apply_filter('lowpass')).pack(fill=tk.X, pady=2)
        ttk.Button(filter_frame, text="应用带通滤波器", 
                  command=lambda: self.apply_filter('bandpass')).pack(fill=tk.X, pady=2)
        ttk.Button(filter_frame, text="应用陷波滤波器", 
                  command=lambda: self.apply_filter('notch')).pack(fill=tk.X, pady=2)
        
        # 音频播放
        play_frame = ttk.LabelFrame(control_frame, text="音频播放", padding="5")
        play_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(play_frame, text="播放原始音频", 
                  command=lambda: self.play_audio('original')).pack(fill=tk.X, pady=2)
        ttk.Button(play_frame, text="播放带噪音频", 
                  command=lambda: self.play_audio('noisy')).pack(fill=tk.X, pady=2)
        ttk.Button(play_frame, text="播放滤波后音频", 
                  command=lambda: self.play_audio('filtered')).pack(fill=tk.X, pady=2)
        
        # 分析功能
        analysis_frame = ttk.LabelFrame(control_frame, text="信号分析", padding="5")
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(analysis_frame, text="显示时域波形", 
                  command=self.show_time_domain).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="显示频域谱", 
                  command=self.show_frequency_domain).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="显示对比图", 
                  command=self.show_comparison).pack(fill=tk.X, pady=2)
        
        # 右侧显示区域
        display_frame = ttk.LabelFrame(main_frame, text="信号显示", padding="10")
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建matplotlib图形
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def load_processor_data(self):
        """从处理器加载数据"""
        if self.processor:
            self.audio_data = self.processor.audio_data
            self.sample_rate = self.processor.sample_rate
            self.noisy_signals = self.processor.noisy_signals
            self.filtered_signals = self.processor.filtered_signals
            self.status_var.set(f"已加载音频: {self.processor.input_file}")
    
    def load_audio_file(self):
        """加载音频文件"""
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.audio_data, self.sample_rate = sf.read(file_path)
                self.status_var.set(f"已加载: {Path(file_path).name}")
                self.plot_original_signal()
            except Exception as e:
                messagebox.showerror("错误", f"加载文件失败: {e}")
    
    def add_noise(self, noise_type):
        """添加噪声"""
        if self.audio_data is None:
            messagebox.showwarning("警告", "请先加载音频文件")
            return
        
        try:
            if noise_type == 'gaussian':
                snr = float(self.gaussian_snr_var.get())
                self.noisy_signals['gaussian'] = add_gaussian_noise(self.audio_data, snr)
                self.status_var.set(f"已添加高斯白噪声 (SNR: {snr}dB)")
                
            elif noise_type == 'narrowband':
                low_freq = float(self.low_freq_var.get())
                high_freq = float(self.high_freq_var.get())
                self.noisy_signals['narrowband'] = add_narrowband_noise(
                    self.audio_data, self.sample_rate, low_freq, high_freq
                )
                self.status_var.set(f"已添加窄带噪声 ({low_freq}-{high_freq}Hz)")
                
            elif noise_type == 'single_freq':
                freq = float(self.single_freq_var.get())
                self.noisy_signals['single_freq'] = add_single_frequency_interference(
                    self.audio_data, self.sample_rate, freq
                )
                self.status_var.set(f"已添加单频干扰 ({freq}Hz)")
            
            self.plot_noisy_signal(noise_type)
            
        except ValueError as e:
            messagebox.showerror("错误", f"参数错误: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"添加噪声失败: {e}")
    
    def apply_filter(self, filter_type):
        """应用滤波器"""
        if not self.noisy_signals:
            messagebox.showwarning("警告", "请先添加噪声")
            return
        
        try:
            if filter_type == 'lowpass':
                filter_obj = design_lowpass_filter(3000, self.sample_rate)
                for noise_type, noisy_signal in self.noisy_signals.items():
                    self.filtered_signals[f"{noise_type}_lowpass"] = filter_obj.filter(noisy_signal)
                    
            elif filter_type == 'bandpass':
                filter_obj = design_bandpass_filter(200, 8000, self.sample_rate)
                for noise_type, noisy_signal in self.noisy_signals.items():
                    self.filtered_signals[f"{noise_type}_bandpass"] = filter_obj.filter(noisy_signal)
                    
            elif filter_type == 'notch':
                filter_obj = design_notch_filter(1500, self.sample_rate)
                for noise_type, noisy_signal in self.noisy_signals.items():
                    self.filtered_signals[f"{noise_type}_notch"] = filter_obj.filter(noisy_signal)
            
            self.status_var.set(f"已应用{filter_type}滤波器")
            self.plot_filtered_signal(filter_type)
            
        except Exception as e:
            messagebox.showerror("错误", f"应用滤波器失败: {e}")
    
    def play_audio(self, audio_type):
        """播放音频"""
        if audio_type == 'original' and self.audio_data is not None:
            self.play_audio_thread(self.audio_data, "原始音频")
        elif audio_type == 'noisy' and self.noisy_signals:
            # 播放第一个带噪信号
            noise_type = list(self.noisy_signals.keys())[0]
            self.play_audio_thread(self.noisy_signals[noise_type], f"{noise_type}噪声音频")
        elif audio_type == 'filtered' and self.filtered_signals:
            # 播放第一个滤波后信号
            filter_type = list(self.filtered_signals.keys())[0]
            self.play_audio_thread(self.filtered_signals[filter_type], f"{filter_type}滤波后音频")
        else:
            messagebox.showwarning("警告", "没有可播放的音频")
    
    def play_audio_thread(self, audio_data, description):
        """在独立线程中播放音频"""
        def play():
            self.status_var.set(f"正在播放: {description}")
            sd.play(audio_data, self.sample_rate)
            sd.wait()
            self.status_var.set("播放完成")
        
        thread = threading.Thread(target=play)
        thread.daemon = True
        thread.start()
    
    def plot_original_signal(self):
        """绘制原始信号"""
        if self.audio_data is None:
            return
        
        self.ax.clear()
        duration = len(self.audio_data) / self.sample_rate
        time_axis = np.linspace(0, duration, len(self.audio_data))
        
        # 限制显示时长
        max_duration = 5
        if duration > max_duration:
            max_samples = int(max_duration * self.sample_rate)
            plot_data = self.audio_data[:max_samples]
            plot_time = time_axis[:max_samples]
        else:
            plot_data = self.audio_data
            plot_time = time_axis
        
        self.ax.plot(plot_time, plot_data, linewidth=0.5)
        self.ax.set_title("原始音频信号", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("时间 (秒)")
        self.ax.set_ylabel("幅度")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def plot_noisy_signal(self, noise_type):
        """绘制带噪信号"""
        if noise_type not in self.noisy_signals:
            return
        
        noisy_signal = self.noisy_signals[noise_type]
        
        self.ax.clear()
        duration = len(noisy_signal) / self.sample_rate
        time_axis = np.linspace(0, duration, len(noisy_signal))
        
        # 限制显示时长
        max_duration = 5
        if duration > max_duration:
            max_samples = int(max_duration * self.sample_rate)
            plot_data = noisy_signal[:max_samples]
            plot_time = time_axis[:max_samples]
        else:
            plot_data = noisy_signal
            plot_time = time_axis
        
        self.ax.plot(plot_time, plot_data, linewidth=0.5)
        self.ax.set_title(f"{noise_type}噪声信号", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("时间 (秒)")
        self.ax.set_ylabel("幅度")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def plot_filtered_signal(self, filter_type):
        """绘制滤波后信号"""
        # 找到对应的滤波后信号
        filtered_key = None
        for key in self.filtered_signals.keys():
            if filter_type in key:
                filtered_key = key
                break
        
        if filtered_key is None:
            return
        
        filtered_signal = self.filtered_signals[filtered_key]
        
        self.ax.clear()
        duration = len(filtered_signal) / self.sample_rate
        time_axis = np.linspace(0, duration, len(filtered_signal))
        
        # 限制显示时长
        max_duration = 5
        if duration > max_duration:
            max_samples = int(max_duration * self.sample_rate)
            plot_data = filtered_signal[:max_samples]
            plot_time = time_axis[:max_samples]
        else:
            plot_data = filtered_signal
            plot_time = time_axis
        
        self.ax.plot(plot_time, plot_data, linewidth=0.5)
        self.ax.set_title(f"{filtered_key}滤波后信号", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("时间 (秒)")
        self.ax.set_ylabel("幅度")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def show_time_domain(self):
        """显示时域波形"""
        if self.audio_data is None:
            messagebox.showwarning("警告", "请先加载音频文件")
            return
        
        plot_time_domain(self.audio_data, self.sample_rate, "原始信号时域波形")
    
    def show_frequency_domain(self):
        """显示频域谱"""
        if self.audio_data is None:
            messagebox.showwarning("警告", "请先加载音频文件")
            return
        
        plot_frequency_domain(self.audio_data, self.sample_rate, "原始信号频域谱")
    
    def show_comparison(self):
        """显示对比图"""
        if not self.noisy_signals or not self.filtered_signals:
            messagebox.showwarning("警告", "请先添加噪声并应用滤波器")
            return
        
        # 选择第一个信号进行对比
        noise_type = list(self.noisy_signals.keys())[0]
        filtered_key = list(self.filtered_signals.keys())[0]
        
        plot_comparison(
            self.noisy_signals[noise_type],
            self.filtered_signals[filtered_key],
            self.sample_rate,
            f"{noise_type} vs {filtered_key}"
        )
    
    def save_results(self):
        """保存处理结果"""
        if not self.filtered_signals:
            messagebox.showwarning("警告", "没有可保存的结果")
            return
        
        save_dir = filedialog.askdirectory(title="选择保存目录")
        if save_dir:
            try:
                for name, signal_data in self.filtered_signals.items():
                    file_path = Path(save_dir) / f"{name}_filtered.wav"
                    sf.write(str(file_path), signal_data, self.sample_rate)
                
                self.status_var.set(f"结果已保存到: {save_dir}")
                messagebox.showinfo("成功", "处理结果已保存")
                
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
    
    def run(self):
        """运行GUI"""
        self.root.mainloop() 