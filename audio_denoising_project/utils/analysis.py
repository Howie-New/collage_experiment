#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信号分析模块
实现时域和频域分析、图表绘制等功能
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def plot_time_domain(signal_data, sample_rate, title="时域信号", save_path=None, max_duration=10):
    """
    绘制时域波形图
    
    参数:
        signal_data: 信号数据
        sample_rate: 采样率
        title: 图表标题
        save_path: 保存路径
        max_duration: 最大显示时长(秒)
    """
    # 计算时间轴
    duration = len(signal_data) / sample_rate
    time_axis = np.linspace(0, duration, len(signal_data))
    
    # 限制显示时长
    if duration > max_duration:
        max_samples = int(max_duration * sample_rate)
        signal_data = signal_data[:max_samples]
        time_axis = time_axis[:max_samples]
    
    plt.figure(figsize=(12, 6))
    plt.plot(time_axis, signal_data, linewidth=0.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('时间 (秒)', fontsize=12)
    plt.ylabel('幅度', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"时域图保存至: {save_path}")
    
    plt.show()

def plot_frequency_domain(signal_data, sample_rate, title="频域信号", save_path=None):
    """
    绘制频域图 (FFT)
    
    参数:
        signal_data: 信号数据
        sample_rate: 采样率
        title: 图表标题
        save_path: 保存路径
    """
    # 计算FFT
    n = len(signal_data)
    fft_result = fft(signal_data)
    frequencies = fftfreq(n, 1/sample_rate)
    
    # 只显示正频率部分
    positive_freq_mask = frequencies >= 0
    frequencies = frequencies[positive_freq_mask]
    magnitude = np.abs(fft_result[positive_freq_mask])
    
    # 转换为dB
    magnitude_db = 20 * np.log10(magnitude + 1e-10)
    
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, magnitude_db, linewidth=0.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('频率 (Hz)', fontsize=12)
    plt.ylabel('幅度 (dB)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sample_rate/2)  # 显示到奈奎斯特频率
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"频域图保存至: {save_path}")
    
    plt.show()

def plot_filter_response(filter_obj, sample_rate, filter_name="滤波器", save_path=None):
    """
    绘制滤波器频率响应
    
    参数:
        filter_obj: 滤波器对象
        sample_rate: 采样率
        filter_name: 滤波器名称
        save_path: 保存路径
    """
    frequencies, magnitude, phase = filter_obj.get_frequency_response()
    
    # 转换为dB
    magnitude_db = 20 * np.log10(magnitude + 1e-10)
    
    # 创建子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # 幅频响应
    ax1.plot(frequencies, magnitude_db, linewidth=2)
    ax1.set_title(f'{filter_name} - 幅频响应', fontsize=14, fontweight='bold')
    ax1.set_xlabel('频率 (Hz)', fontsize=12)
    ax1.set_ylabel('幅度 (dB)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, sample_rate/2)
    
    # 相频响应
    ax2.plot(frequencies, np.unwrap(phase), linewidth=2)
    ax2.set_title(f'{filter_name} - 相频响应', fontsize=14, fontweight='bold')
    ax2.set_xlabel('频率 (Hz)', fontsize=12)
    ax2.set_ylabel('相位 (弧度)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, sample_rate/2)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"滤波器响应图保存至: {save_path}")
    
    plt.show()

def plot_comparison(original, processed, sample_rate, title="信号对比", save_path=None):
    """
    绘制原始信号和处理后信号的对比图
    
    参数:
        original: 原始信号
        processed: 处理后信号
        sample_rate: 采样率
        title: 图表标题
        save_path: 保存路径
    """
    # 计算时间轴
    duration = len(original) / sample_rate
    time_axis = np.linspace(0, duration, len(original))
    
    # 限制显示时长
    max_duration = 5
    if duration > max_duration:
        max_samples = int(max_duration * sample_rate)
        original = original[:max_samples]
        processed = processed[:max_samples]
        time_axis = time_axis[:max_samples]
    
    # 创建子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # 时域对比
    ax1.plot(time_axis, original, label='原始信号', linewidth=0.5)
    ax1.plot(time_axis, processed, label='处理后信号', linewidth=0.5)
    ax1.set_title(f'{title} - 时域对比', fontsize=14, fontweight='bold')
    ax1.set_xlabel('时间 (秒)', fontsize=12)
    ax1.set_ylabel('幅度', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 频域对比
    # 计算FFT
    n = len(original)
    fft_original = fft(original)
    fft_processed = fft(processed)
    frequencies = fftfreq(n, 1/sample_rate)
    
    # 只显示正频率部分
    positive_freq_mask = frequencies >= 0
    frequencies = frequencies[positive_freq_mask]
    magnitude_original = np.abs(fft_original[positive_freq_mask])
    magnitude_processed = np.abs(fft_processed[positive_freq_mask])
    
    # 转换为dB
    magnitude_original_db = 20 * np.log10(magnitude_original + 1e-10)
    magnitude_processed_db = 20 * np.log10(magnitude_processed + 1e-10)
    
    ax2.plot(frequencies, magnitude_original_db, label='原始信号', linewidth=0.5)
    ax2.plot(frequencies, magnitude_processed_db, label='处理后信号', linewidth=0.5)
    ax2.set_title(f'{title} - 频域对比', fontsize=14, fontweight='bold')
    ax2.set_xlabel('频率 (Hz)', fontsize=12)
    ax2.set_ylabel('幅度 (dB)', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, sample_rate/2)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"对比图保存至: {save_path}")
    
    plt.show()

def calculate_snr(original_signal, noisy_signal):
    """
    计算信噪比
    
    参数:
        original_signal: 原始信号
        noisy_signal: 带噪信号
    
    返回:
        信噪比 (dB)
    """
    # 计算信号功率
    signal_power = np.mean(original_signal ** 2)
    
    # 计算噪声功率
    noise = noisy_signal - original_signal
    noise_power = np.mean(noise ** 2)
    
    # 计算信噪比
    snr = 10 * np.log10(signal_power / noise_power)
    
    return snr

def calculate_psnr(original_signal, processed_signal):
    """
    计算峰值信噪比
    
    参数:
        original_signal: 原始信号
        processed_signal: 处理后信号
    
    返回:
        峰值信噪比 (dB)
    """
    # 计算峰值
    max_value = np.max(np.abs(original_signal))
    
    # 计算均方误差
    mse = np.mean((original_signal - processed_signal) ** 2)
    
    # 计算PSNR
    psnr = 20 * np.log10(max_value / np.sqrt(mse))
    
    return psnr

def calculate_spectral_centroid(signal_data, sample_rate):
    """
    计算频谱质心
    
    参数:
        signal_data: 信号数据
        sample_rate: 采样率
    
    返回:
        频谱质心频率
    """
    # 计算FFT
    fft_result = fft(signal_data)
    frequencies = fftfreq(len(signal_data), 1/sample_rate)
    
    # 计算功率谱
    power_spectrum = np.abs(fft_result) ** 2
    
    # 计算频谱质心
    centroid = np.sum(frequencies * power_spectrum) / np.sum(power_spectrum)
    
    return centroid

def calculate_spectral_rolloff(signal_data, sample_rate, percentile=85):
    """
    计算频谱滚降点
    
    参数:
        signal_data: 信号数据
        sample_rate: 采样率
        percentile: 百分位数
    
    返回:
        频谱滚降频率
    """
    # 计算FFT
    fft_result = fft(signal_data)
    frequencies = fftfreq(len(signal_data), 1/sample_rate)
    
    # 计算功率谱
    power_spectrum = np.abs(fft_result) ** 2
    
    # 只考虑正频率
    positive_mask = frequencies >= 0
    frequencies = frequencies[positive_mask]
    power_spectrum = power_spectrum[positive_mask]
    
    # 计算累积功率
    total_power = np.sum(power_spectrum)
    cumulative_power = np.cumsum(power_spectrum)
    
    # 找到滚降点
    threshold = total_power * percentile / 100
    rolloff_idx = np.where(cumulative_power >= threshold)[0][0]
    rolloff_freq = frequencies[rolloff_idx]
    
    return rolloff_freq

def plot_spectrogram(signal_data, sample_rate, title="频谱图", save_path=None):
    """
    绘制频谱图
    
    参数:
        signal_data: 信号数据
        sample_rate: 采样率
        title: 图表标题
        save_path: 保存路径
    """
    plt.figure(figsize=(12, 6))
    
    # 计算频谱图
    f, t, Sxx = signal.spectrogram(signal_data, sample_rate, nperseg=1024, noverlap=512)
    
    # 绘制频谱图
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('时间 (秒)', fontsize=12)
    plt.ylabel('频率 (Hz)', fontsize=12)
    plt.colorbar(label='功率谱密度 (dB/Hz)')
    plt.ylim(0, sample_rate/2)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"频谱图保存至: {save_path}")
    
    plt.show() 