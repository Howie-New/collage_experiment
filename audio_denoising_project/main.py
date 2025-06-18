#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频降噪项目主程序
实现音频信号采集、噪声添加、滤波处理和GUI界面展示
"""

import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import os
from pathlib import Path

from utils.noise import add_gaussian_noise, add_narrowband_noise, add_single_frequency_interference
from utils.filters import design_lowpass_filter, design_bandpass_filter, design_notch_filter
from utils.analysis import plot_time_domain, plot_frequency_domain, plot_filter_response
from gui import AudioDenoisingGUI

class AudioDenoisingProcessor:
    """音频降噪处理器"""
    
    def __init__(self, input_file="chinese-beat-190047.wav"):
        self.input_file = input_file
        self.sample_rate = None
        self.audio_data = None
        self.noisy_signals = {}
        self.filtered_signals = {}
        self.filters = {}
        
        # 创建输出目录
        self.output_dirs = {
            'noisy': 'output/noisy_audio',
            'filtered': 'output/filtered_audio',
            'plots': 'output/plots'
        }
        
        for dir_path in self.output_dirs.values():
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def load_audio(self):
        """加载音频文件"""
        print("正在加载音频文件...")
        try:
            self.audio_data, self.sample_rate = sf.read(self.input_file)
            print(f"音频加载成功: 采样率={self.sample_rate}Hz, 时长={len(self.audio_data)/self.sample_rate:.2f}秒")
            return True
        except Exception as e:
            print(f"音频加载失败: {e}")
            return False
    
    def add_noise(self):
        """添加三种不同类型的噪声"""
        print("正在添加噪声...")
        
        # 1. 高斯白噪声
        self.noisy_signals['gaussian'] = add_gaussian_noise(
            self.audio_data, snr_db=10
        )
        
        # 2. 窄带高斯噪声 (1000Hz-2000Hz)
        self.noisy_signals['narrowband'] = add_narrowband_noise(
            self.audio_data, self.sample_rate, 
            low_freq=1000, high_freq=2000, snr_db=15
        )
        
        # 3. 单频干扰 (1500Hz正弦波)
        self.noisy_signals['single_freq'] = add_single_frequency_interference(
            self.audio_data, self.sample_rate, 
            frequency=1500, amplitude=0.3
        )
        
        print("噪声添加完成")
    
    def design_filters(self):
        """设计滤波器"""
        print("正在设计滤波器...")
        
        # 低通滤波器 (用于高斯白噪声)
        self.filters['lowpass'] = design_lowpass_filter(
            cutoff_freq=3000, sample_rate=self.sample_rate
        )
        
        # 带通滤波器 (用于窄带噪声)
        self.filters['bandpass'] = design_bandpass_filter(
            low_freq=200, high_freq=8000, sample_rate=self.sample_rate
        )
        
        # 陷波滤波器 (用于单频干扰)
        self.filters['notch'] = design_notch_filter(
            notch_freq=1500, sample_rate=self.sample_rate
        )
        
        print("滤波器设计完成")
    
    def apply_filters(self):
        """应用滤波器"""
        print("正在应用滤波器...")
        
        # 对高斯白噪声信号应用低通滤波器
        self.filtered_signals['gaussian'] = self.filters['lowpass'].filter(
            self.noisy_signals['gaussian']
        )
        
        # 对窄带噪声信号应用带通滤波器
        self.filtered_signals['narrowband'] = self.filters['bandpass'].filter(
            self.noisy_signals['narrowband']
        )
        
        # 对单频干扰信号应用陷波滤波器
        self.filtered_signals['single_freq'] = self.filters['notch'].filter(
            self.noisy_signals['single_freq']
        )
        
        print("滤波处理完成")
    
    def analyze_signals(self):
        """分析信号并生成图表"""
        print("正在生成分析图表...")
        
        # 原始信号分析
        plot_time_domain(self.audio_data, self.sample_rate, "原始信号", 
                        save_path=f"{self.output_dirs['plots']}/original_time.png")
        plot_frequency_domain(self.audio_data, self.sample_rate, "原始信号", 
                             save_path=f"{self.output_dirs['plots']}/original_freq.png")
        
        # 带噪信号分析
        for noise_type, noisy_signal in self.noisy_signals.items():
            plot_time_domain(noisy_signal, self.sample_rate, f"{noise_type}噪声信号", 
                           save_path=f"{self.output_dirs['plots']}/{noise_type}_noisy_time.png")
            plot_frequency_domain(noisy_signal, self.sample_rate, f"{noise_type}噪声信号", 
                                save_path=f"{self.output_dirs['plots']}/{noise_type}_noisy_freq.png")
        
        # 滤波后信号分析
        for noise_type, filtered_signal in self.filtered_signals.items():
            plot_time_domain(filtered_signal, self.sample_rate, f"{noise_type}滤波后信号", 
                           save_path=f"{self.output_dirs['plots']}/{noise_type}_filtered_time.png")
            plot_frequency_domain(filtered_signal, self.sample_rate, f"{noise_type}滤波后信号", 
                                save_path=f"{self.output_dirs['plots']}/{noise_type}_filtered_freq.png")
        
        # 滤波器响应
        for filter_type, filter_obj in self.filters.items():
            plot_filter_response(filter_obj, self.sample_rate, filter_type, 
                               save_path=f"{self.output_dirs['plots']}/{filter_type}_response.png")
        
        print("分析图表生成完成")
    
    def save_audio_files(self):
        """保存音频文件"""
        print("正在保存音频文件...")
        
        # 保存带噪音频
        for noise_type, noisy_signal in self.noisy_signals.items():
            sf.write(f"{self.output_dirs['noisy']}/{noise_type}_noisy.wav", 
                    noisy_signal, self.sample_rate)
        
        # 保存滤波后音频
        for noise_type, filtered_signal in self.filtered_signals.items():
            sf.write(f"{self.output_dirs['filtered']}/{noise_type}_filtered.wav", 
                    filtered_signal, self.sample_rate)
        
        print("音频文件保存完成")
    
    def play_audio_comparison(self):
        """播放音频对比"""
        print("播放音频对比...")
        
        # 播放原始音频
        print("播放原始音频...")
        sd.play(self.audio_data, self.sample_rate)
        sd.wait()
        
        # 播放带噪音频
        for noise_type, noisy_signal in self.noisy_signals.items():
            print(f"播放{noise_type}噪声音频...")
            sd.play(noisy_signal, self.sample_rate)
            sd.wait()
        
        # 播放滤波后音频
        for noise_type, filtered_signal in self.filtered_signals.items():
            print(f"播放{noise_type}滤波后音频...")
            sd.play(filtered_signal, self.sample_rate)
            sd.wait()
    
    def run_full_pipeline(self):
        """运行完整的处理流程"""
        print("开始音频降噪处理流程...")
        
        if not self.load_audio():
            return False
        
        self.add_noise()
        self.design_filters()
        self.apply_filters()
        self.analyze_signals()
        self.save_audio_files()
        
        print("处理流程完成！")
        return True

def main():
    """主函数"""
    # 创建处理器实例
    processor = AudioDenoisingProcessor()
    
    # 运行处理流程
    if processor.run_full_pipeline():
        # 启动GUI界面
        app = AudioDenoisingGUI(processor)
        app.run()

if __name__ == "__main__":
    main() 