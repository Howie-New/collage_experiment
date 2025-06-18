#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频降噪项目工具包
"""

from .noise import (
    add_gaussian_noise,
    add_narrowband_noise,
    add_single_frequency_interference,
    calculate_snr,
    add_impulse_noise
)

from .filters import (
    Filter,
    design_lowpass_filter,
    design_highpass_filter,
    design_bandpass_filter,
    design_bandstop_filter,
    design_notch_filter,
    design_adaptive_filter,
    design_wiener_filter
)

from .analysis import (
    plot_time_domain,
    plot_frequency_domain,
    plot_filter_response,
    plot_comparison,
    calculate_snr,
    calculate_psnr,
    calculate_spectral_centroid,
    calculate_spectral_rolloff,
    plot_spectrogram
)

__all__ = [
    # 噪声相关
    'add_gaussian_noise',
    'add_narrowband_noise',
    'add_single_frequency_interference',
    'calculate_snr',
    'add_impulse_noise',
    
    # 滤波器相关
    'Filter',
    'design_lowpass_filter',
    'design_highpass_filter',
    'design_bandpass_filter',
    'design_bandstop_filter',
    'design_notch_filter',
    'design_adaptive_filter',
    'design_wiener_filter',
    
    # 分析相关
    'plot_time_domain',
    'plot_frequency_domain',
    'plot_filter_response',
    'plot_comparison',
    'calculate_psnr',
    'calculate_spectral_centroid',
    'calculate_spectral_rolloff',
    'plot_spectrogram'
] 