#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滤波器模块
实现低通、带通、陷波等滤波器的设计和应用
"""

import numpy as np
from scipy import signal
from scipy.signal import butter, cheby1, cheby2, ellip, filtfilt

class Filter:
    """滤波器基类"""
    
    def __init__(self, b, a, sample_rate, filter_type="Unknown"):
        self.b = b  # 分子系数
        self.a = a  # 分母系数
        self.sample_rate = sample_rate
        self.filter_type = filter_type
    
    def filter(self, signal_data):
        # 支持多声道
        if len(signal_data.shape) > 1:
            filtered_channels = []
            for ch in range(signal_data.shape[1]):
                channel_data = signal_data[:, ch]
                if len(channel_data) <= 15:
                    raise ValueError("每个声道长度必须大于15")
                filtered = filtfilt(self.b, self.a, channel_data)
                filtered_channels.append(filtered)
            return np.column_stack(filtered_channels)
        else:
            if len(signal_data) <= 15:
                raise ValueError("信号长度必须大于15")
            return filtfilt(self.b, self.a, signal_data)
    
    def get_frequency_response(self, n_points=1024):
        """获取频率响应"""
        w, h = signal.freqz(self.b, self.a, worN=n_points)
        frequencies = w * self.sample_rate / (2 * np.pi)
        magnitude = np.abs(h)
        phase = np.angle(h)
        
        return frequencies, magnitude, phase

def design_lowpass_filter(cutoff_freq, sample_rate, order=4, filter_type='butterworth'):
    """
    设计低通滤波器
    
    参数:
        cutoff_freq: 截止频率
        sample_rate: 采样率
        order: 滤波器阶数
        filter_type: 滤波器类型 ('butterworth', 'chebyshev1', 'chebyshev2', 'elliptic')
    
    返回:
        Filter对象
    """
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff_freq / nyquist
    
    if filter_type == 'butterworth':
        b, a = butter(order, normalized_cutoff, btype='low')
    elif filter_type == 'chebyshev1':
        b, a = cheby1(order, 1, normalized_cutoff, btype='low')
    elif filter_type == 'chebyshev2':
        b, a = cheby2(order, 40, normalized_cutoff, btype='low')
    elif filter_type == 'elliptic':
        b, a = ellip(order, 1, 40, normalized_cutoff, btype='low')
    else:
        raise ValueError(f"不支持的滤波器类型: {filter_type}")
    
    return Filter(b, a, sample_rate, f"Lowpass_{filter_type}")

def design_highpass_filter(cutoff_freq, sample_rate, order=4, filter_type='butterworth'):
    """
    设计高通滤波器
    
    参数:
        cutoff_freq: 截止频率
        sample_rate: 采样率
        order: 滤波器阶数
        filter_type: 滤波器类型
    
    返回:
        Filter对象
    """
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff_freq / nyquist
    
    if filter_type == 'butterworth':
        b, a = butter(order, normalized_cutoff, btype='high')
    elif filter_type == 'chebyshev1':
        b, a = cheby1(order, 1, normalized_cutoff, btype='high')
    elif filter_type == 'chebyshev2':
        b, a = cheby2(order, 40, normalized_cutoff, btype='high')
    elif filter_type == 'elliptic':
        b, a = ellip(order, 1, 40, normalized_cutoff, btype='high')
    else:
        raise ValueError(f"不支持的滤波器类型: {filter_type}")
    
    return Filter(b, a, sample_rate, f"Highpass_{filter_type}")

def design_bandpass_filter(low_freq, high_freq, sample_rate, order=4, filter_type='butterworth'):
    """
    设计带通滤波器
    
    参数:
        low_freq: 低频截止频率
        high_freq: 高频截止频率
        sample_rate: 采样率
        order: 滤波器阶数
        filter_type: 滤波器类型
    
    返回:
        Filter对象
    """
    nyquist = sample_rate / 2
    low_norm = low_freq / nyquist
    high_norm = high_freq / nyquist
    
    if filter_type == 'butterworth':
        b, a = butter(order, [low_norm, high_norm], btype='band')
    elif filter_type == 'chebyshev1':
        b, a = cheby1(order, 1, [low_norm, high_norm], btype='band')
    elif filter_type == 'chebyshev2':
        b, a = cheby2(order, 40, [low_norm, high_norm], btype='band')
    elif filter_type == 'elliptic':
        b, a = ellip(order, 1, 40, [low_norm, high_norm], btype='band')
    else:
        raise ValueError(f"不支持的滤波器类型: {filter_type}")
    
    return Filter(b, a, sample_rate, f"Bandpass_{filter_type}")

def design_bandstop_filter(low_freq, high_freq, sample_rate, order=4, filter_type='butterworth'):
    """
    设计带阻滤波器
    
    参数:
        low_freq: 低频截止频率
        high_freq: 高频截止频率
        sample_rate: 采样率
        order: 滤波器阶数
        filter_type: 滤波器类型
    
    返回:
        Filter对象
    """
    nyquist = sample_rate / 2
    low_norm = low_freq / nyquist
    high_norm = high_freq / nyquist
    
    if filter_type == 'butterworth':
        b, a = butter(order, [low_norm, high_norm], btype='bandstop')
    elif filter_type == 'chebyshev1':
        b, a = cheby1(order, 1, [low_norm, high_norm], btype='bandstop')
    elif filter_type == 'chebyshev2':
        b, a = cheby2(order, 40, [low_norm, high_norm], btype='bandstop')
    elif filter_type == 'elliptic':
        b, a = ellip(order, 1, 40, [low_norm, high_norm], btype='bandstop')
    else:
        raise ValueError(f"不支持的滤波器类型: {filter_type}")
    
    return Filter(b, a, sample_rate, f"Bandstop_{filter_type}")

def design_notch_filter(notch_freq, sample_rate, quality_factor=30):
    """
    设计陷波滤波器 (用于去除单频干扰)
    
    参数:
        notch_freq: 陷波频率
        sample_rate: 采样率
        quality_factor: 品质因数 (Q值)
    
    返回:
        Filter对象
    """
    # 计算带宽
    bandwidth = notch_freq / quality_factor
    
    # 计算归一化频率
    nyquist = sample_rate / 2
    notch_norm = notch_freq / nyquist
    bandwidth_norm = bandwidth / nyquist
    
    # 设计陷波滤波器
    b, a = signal.iirnotch(notch_norm, quality_factor)
    
    return Filter(b, a, sample_rate, "Notch")

def design_adaptive_filter(reference_signal, desired_signal, filter_length=64, mu=0.01):
    """
    设计自适应滤波器 (LMS算法)
    
    参数:
        reference_signal: 参考信号 (噪声)
        desired_signal: 期望信号 (原始信号)
        filter_length: 滤波器长度
        mu: 步长参数
    
    返回:
        滤波后的信号
    """
    # 初始化滤波器系数
    w = np.zeros(filter_length)
    
    # 初始化输出信号
    output = np.zeros_like(desired_signal)
    
    # LMS算法
    for n in range(filter_length, len(desired_signal)):
        # 获取输入向量
        x = reference_signal[n-filter_length+1:n+1][::-1]
        
        # 计算滤波器输出
        y = np.dot(w, x)
        output[n] = y
        
        # 计算误差
        error = desired_signal[n] - y
        
        # 更新滤波器系数
        w = w + mu * error * x
    
    return output

def design_wiener_filter(signal_data, noise_data, sample_rate):
    """
    设计维纳滤波器
    
    参数:
        signal_data: 信号数据
        noise_data: 噪声数据
        sample_rate: 采样率
    
    返回:
        滤波后的信号
    """
    # 计算功率谱密度
    f, psd_signal = signal.welch(signal_data, sample_rate, nperseg=1024)
    f, psd_noise = signal.welch(noise_data, sample_rate, nperseg=1024)
    
    # 计算维纳滤波器频率响应
    h_wiener = psd_signal / (psd_signal + psd_noise)
    
    # 应用滤波器
    # 这里简化处理，实际应用中需要更复杂的实现
    filtered_signal = signal_data * np.mean(h_wiener)
    
    return filtered_signal 