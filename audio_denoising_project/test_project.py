#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目测试脚本
验证所有模块是否正常工作
"""

import sys
import os
import numpy as np

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    try:
        from utils.noise import add_gaussian_noise, add_narrowband_noise, add_single_frequency_interference
        from utils.filters import design_lowpass_filter, design_bandpass_filter, design_notch_filter
        from utils.analysis import plot_time_domain, plot_frequency_domain
        print("✓ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_audio_loading():
    """测试音频加载"""
    print("测试音频加载...")
    try:
        import soundfile as sf
        if os.path.exists("chinese-beat-190047.wav"):
            audio_data, sample_rate = sf.read("chinese-beat-190047.wav")
            print(f"✓ 音频加载成功: 采样率={sample_rate}Hz, 形状={audio_data.shape}")
            return audio_data, sample_rate
        else:
            print("✗ 音频文件不存在")
            return None, None
    except Exception as e:
        print(f"✗ 音频加载失败: {e}")
        return None, None

def test_noise_generation(audio_data, sample_rate):
    """测试噪声生成"""
    print("测试噪声生成...")
    try:
        from utils.noise import add_gaussian_noise, add_narrowband_noise, add_single_frequency_interference
        
        # 测试高斯白噪声
        noisy_gaussian = add_gaussian_noise(audio_data, snr_db=10)
        print("✓ 高斯白噪声生成成功")
        
        # 测试窄带噪声
        noisy_narrowband = add_narrowband_noise(audio_data, sample_rate, 1000, 2000)
        print("✓ 窄带噪声生成成功")
        
        # 测试单频干扰
        noisy_single = add_single_frequency_interference(audio_data, sample_rate, 1500)
        print("✓ 单频干扰生成成功")
        
        return True
    except Exception as e:
        print(f"✗ 噪声生成失败: {e}")
        return False

def test_filter_design(sample_rate):
    """测试滤波器设计"""
    print("测试滤波器设计...")
    try:
        from utils.filters import design_lowpass_filter, design_bandpass_filter, design_notch_filter
        
        # 测试低通滤波器
        lowpass_filter = design_lowpass_filter(3000, sample_rate)
        print("✓ 低通滤波器设计成功")
        
        # 测试带通滤波器
        bandpass_filter = design_bandpass_filter(200, 8000, sample_rate)
        print("✓ 带通滤波器设计成功")
        
        # 测试陷波滤波器
        notch_filter = design_notch_filter(1500, sample_rate)
        print("✓ 陷波滤波器设计成功")
        
        return True
    except Exception as e:
        print(f"✗ 滤波器设计失败: {e}")
        return False

def test_analysis_functions(audio_data, sample_rate):
    """测试分析函数"""
    print("测试分析函数...")
    try:
        from utils.analysis import plot_time_domain, plot_frequency_domain
        
        # 测试时域分析（不显示图形）
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端
        
        # 只测试前1秒的数据
        test_data = audio_data[:sample_rate]
        plot_time_domain(test_data, sample_rate, "测试", save_path="test_time.png")
        plot_frequency_domain(test_data, sample_rate, "测试", save_path="test_freq.png")
        
        # 清理测试文件
        if os.path.exists("test_time.png"):
            os.remove("test_time.png")
        if os.path.exists("test_freq.png"):
            os.remove("test_freq.png")
        
        print("✓ 分析函数测试成功")
        return True
    except Exception as e:
        print(f"✗ 分析函数测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 音频降噪项目测试 ===")
    print()
    
    # 测试模块导入
    if not test_imports():
        print("测试失败：模块导入有问题")
        return False
    
    print()
    
    # 测试音频加载
    audio_data, sample_rate = test_audio_loading()
    if audio_data is None:
        print("测试失败：音频加载有问题")
        return False
    
    print()
    
    # 测试噪声生成
    if not test_noise_generation(audio_data, sample_rate):
        print("测试失败：噪声生成有问题")
        return False
    
    print()
    
    # 测试滤波器设计
    if not test_filter_design(sample_rate):
        print("测试失败：滤波器设计有问题")
        return False
    
    print()
    
    # 测试分析函数
    if not test_analysis_functions(audio_data, sample_rate):
        print("测试失败：分析函数有问题")
        return False
    
    print()
    print("=== 所有测试通过！项目可以正常使用 ===")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 