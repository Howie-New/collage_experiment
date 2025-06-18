#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
噪声生成模块
实现高斯白噪声、窄带高斯噪声和单频干扰的添加
"""

import numpy as np
from scipy import signal

def add_gaussian_noise(audio_data, snr_db=10):
    """
    添加高斯白噪声
    
    参数:
        audio_data: 原始音频数据
        snr_db: 信噪比 (dB)
    
    返回:
        带噪音频数据
    """
    # 处理立体声音频
    if len(audio_data.shape) > 1:
        # 立体声，对每个声道分别处理
        noisy_channels = []
        for channel in range(audio_data.shape[1]):
            channel_data = audio_data[:, channel]
            # 计算信号功率
            signal_power = np.mean(channel_data ** 2)
            
            # 根据信噪比计算噪声功率
            noise_power = signal_power / (10 ** (snr_db / 10))
            
            # 生成高斯白噪声
            noise = np.random.normal(0, np.sqrt(noise_power), len(channel_data))
            
            # 添加噪声
            noisy_channel = channel_data + noise
            noisy_channels.append(noisy_channel)
        
        return np.column_stack(noisy_channels)
    else:
        # 单声道
        # 计算信号功率
        signal_power = np.mean(audio_data ** 2)
        
        # 根据信噪比计算噪声功率
        noise_power = signal_power / (10 ** (snr_db / 10))
        
        # 生成高斯白噪声
        noise = np.random.normal(0, np.sqrt(noise_power), len(audio_data))
        
        # 添加噪声
        noisy_signal = audio_data + noise
        
        return noisy_signal

def add_narrowband_noise(audio_data, sample_rate, low_freq=1000, high_freq=2000, snr_db=15):
    """
    添加窄带高斯噪声
    
    参数:
        audio_data: 原始音频数据
        sample_rate: 采样率
        low_freq: 低频截止频率
        high_freq: 高频截止频率
        snr_db: 信噪比 (dB)
    
    返回:
        带噪音频数据
    """
    # 处理立体声音频
    if len(audio_data.shape) > 1:
        # 立体声，对每个声道分别处理
        noisy_channels = []
        for channel in range(audio_data.shape[1]):
            channel_data = audio_data[:, channel]
            noisy_channel = _add_narrowband_noise_single_channel(
                channel_data, sample_rate, low_freq, high_freq, snr_db
            )
            noisy_channels.append(noisy_channel)
        
        return np.column_stack(noisy_channels)
    else:
        # 单声道
        return _add_narrowband_noise_single_channel(
            audio_data, sample_rate, low_freq, high_freq, snr_db
        )

def _add_narrowband_noise_single_channel(audio_data, sample_rate, low_freq, high_freq, snr_db):
    """为单声道添加窄带噪声"""
    # 计算信号功率
    signal_power = np.mean(audio_data ** 2)
    
    # 根据信噪比计算噪声功率
    noise_power = signal_power / (10 ** (snr_db / 10))
    
    # 生成高斯白噪声
    white_noise = np.random.normal(0, 1, len(audio_data))
    
    # 设计带通滤波器
    nyquist = sample_rate / 2
    low_norm = low_freq / nyquist
    high_norm = high_freq / nyquist
    
    # 使用巴特沃斯滤波器
    b, a = signal.butter(4, [low_norm, high_norm], btype='band')
    
    # 滤波得到窄带噪声
    narrowband_noise = signal.filtfilt(b, a, white_noise)
    
    # 调整噪声功率
    current_power = np.mean(narrowband_noise ** 2)
    scale_factor = np.sqrt(noise_power / current_power)
    narrowband_noise = narrowband_noise * scale_factor
    
    # 添加噪声
    noisy_signal = audio_data + narrowband_noise
    
    return noisy_signal

def add_single_frequency_interference(audio_data, sample_rate, frequency=1500, amplitude=0.3):
    """
    添加单频干扰 (正弦波)
    
    参数:
        audio_data: 原始音频数据
        sample_rate: 采样率
        frequency: 干扰频率
        amplitude: 干扰幅度
    
    返回:
        带噪音频数据
    """
    # 生成时间轴
    t = np.arange(len(audio_data)) / sample_rate
    
    # 处理立体声音频
    if len(audio_data.shape) > 1:
        # 立体声，对每个声道分别处理
        noisy_channels = []
        for channel in range(audio_data.shape[1]):
            channel_data = audio_data[:, channel]
            # 生成正弦波干扰
            interference = amplitude * np.sin(2 * np.pi * frequency * t)
            # 添加干扰
            noisy_channel = channel_data + interference
            noisy_channels.append(noisy_channel)
        
        return np.column_stack(noisy_channels)
    else:
        # 单声道
        # 生成正弦波干扰
        interference = amplitude * np.sin(2 * np.pi * frequency * t)
        # 添加干扰
        noisy_signal = audio_data + interference
        
        return noisy_signal

def calculate_snr(original_signal, noisy_signal):
    """
    计算信噪比
    
    参数:
        original_signal: 原始信号
        noisy_signal: 带噪信号
    
    返回:
        信噪比 (dB)
    """
    # 处理立体声音频
    if len(original_signal.shape) > 1:
        # 立体声，计算所有声道的平均SNR
        snrs = []
        for channel in range(original_signal.shape[1]):
            orig_channel = original_signal[:, channel]
            noisy_channel = noisy_signal[:, channel]
            snr = _calculate_snr_single_channel(orig_channel, noisy_channel)
            snrs.append(snr)
        return np.mean(snrs)
    else:
        # 单声道
        return _calculate_snr_single_channel(original_signal, noisy_signal)

def _calculate_snr_single_channel(original_signal, noisy_signal):
    """计算单声道信噪比"""
    # 计算信号功率
    signal_power = np.mean(original_signal ** 2)
    
    # 计算噪声功率
    noise = noisy_signal - original_signal
    noise_power = np.mean(noise ** 2)
    
    # 计算信噪比
    snr = 10 * np.log10(signal_power / noise_power)
    
    return snr

def add_impulse_noise(audio_data, probability=0.01, amplitude=0.5):
    """
    添加脉冲噪声 (可选功能)
    
    参数:
        audio_data: 原始音频数据
        probability: 脉冲出现概率
        amplitude: 脉冲幅度
    
    返回:
        带噪音频数据
    """
    # 处理立体声音频
    if len(audio_data.shape) > 1:
        # 立体声，对每个声道分别处理
        noisy_channels = []
        for channel in range(audio_data.shape[1]):
            channel_data = audio_data[:, channel]
            noisy_channel = _add_impulse_noise_single_channel(
                channel_data, probability, amplitude
            )
            noisy_channels.append(noisy_channel)
        
        return np.column_stack(noisy_channels)
    else:
        # 单声道
        return _add_impulse_noise_single_channel(audio_data, probability, amplitude)

def _add_impulse_noise_single_channel(audio_data, probability, amplitude):
    """为单声道添加脉冲噪声"""
    noisy_signal = audio_data.copy()
    
    # 随机生成脉冲位置
    impulse_positions = np.random.random(len(audio_data)) < probability
    
    # 添加脉冲噪声
    noisy_signal[impulse_positions] += amplitude * np.random.choice([-1, 1], size=np.sum(impulse_positions))
    
    return noisy_signal 