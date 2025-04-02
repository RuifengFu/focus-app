import numpy as np
from scipy.io import wavfile
import os
import time
from scipy import signal


# 确保有一个存在的目录来保存文件
output_dir = os.path.join("src-tauri/resources", "notification_sounds")
os.makedirs(output_dir, exist_ok=True)

def create_clean_bell(filename="clean_bell.wav", duration=0.6):
    """创建一个干净清脆的铃声，类似高级手机的提醒音"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 使用明亮的频率
    freq1 = 1567.98  # G6
    freq2 = 2349.32  # D7
    
    # 基本音调
    bell = np.sin(2 * np.pi * freq1 * t) * 0.5 + np.sin(2 * np.pi * freq2 * t) * 0.3
    
    # 加一点点高频泛音增加清脆感
    harmonic = np.sin(2 * np.pi * freq1 * 2 * t) * 0.15
    
    # 组合并添加指数衰减
    sound = (bell + harmonic) * np.exp(-t * 8)
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_warm_notification(filename="warm_notification.wav", duration=0.8):
    """创建一个温暖舒适的提醒音，适合日常使用"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 使用温暖的大三和弦
    f_base = 392.00  # G4
    f_third = 493.88  # B4
    f_fifth = 587.33  # D5
    
    # 主音色
    tone1 = np.sin(2 * np.pi * f_base * t) * 0.5
    tone2 = np.sin(2 * np.pi * f_third * t) * 0.4
    tone3 = np.sin(2 * np.pi * f_fifth * t) * 0.4
    
    # 增加一些泛音和质感
    harmonic1 = np.sin(2 * np.pi * f_base * 2 * t) * 0.2
    harmonic2 = np.sin(2 * np.pi * f_third * 2 * t) * 0.1
    
    # 添加轻微的颤音效果
    vibrato = np.sin(2 * np.pi * 6 * t) * 0.05
    tone1 = tone1 * (1 + vibrato)
    
    # 混合所有音色
    tone = tone1 + tone2 + tone3 + harmonic1 + harmonic2
    
    # 使用更自然的衰减曲线
    envelope = np.exp(-t * 4) * (1 - np.exp(-t * 25))
    
    sound = tone * envelope
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_soft_chime(filename="soft_chime.wav", duration=1.2):
    """创建一个柔和的风铃音效，舒缓而不突兀"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 基础音调 - 五声音阶
    freqs = [783.99, 880.00, 987.77, 1174.66, 1318.51]  # G5, A5, B5, D6, E6
    
    # 创建基本的风铃声音
    chime = np.zeros_like(t)
    for i, freq in enumerate(freqs):
        # 为每个音调设置稍微不同的起始时间和衰减
        delay = i * 0.1
        decay = 2 + i * 0.5
        
        # 只有在延迟后才开始这个音符
        idx = int(delay * sample_rate)
        if idx < len(t):
            note_t = t[:len(t)-idx]
            note = np.sin(2 * np.pi * freq * note_t) * np.exp(-note_t * decay)
            chime[idx:] += note[:len(t)-idx] * (0.3 - i * 0.05)
    
    # 添加轻微噪音模拟真实风铃
    noise = np.random.normal(0, 0.01, len(t))
    noise_filtered = noise * np.exp(-t * 15)
    
    sound = chime + noise_filtered
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.85  # 稍微降低音量使其更柔和
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_modern_alert(filename="modern_alert.wav", duration=0.5):
    """创建一个现代感十足的简短提醒音，类似高端科技产品"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 使用上升的音调
    start_freq = 1000
    end_freq = 1800
    
    # 创建一个频率扫描
    freq = start_freq + (end_freq - start_freq) * (1 - np.exp(-t * 10)) / (1 - np.exp(-duration * 10))
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    sweep = np.sin(phase)
    
    # 添加一点数字化处理效果
    digital_effect = np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 30) * 0.2
    
    # 组合并塑造音量包络
    envelope = np.exp(-t * 6) * (1 - np.exp(-t * 100))
    sound = (sweep + digital_effect) * envelope
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_gentle_ding_dong(filename="gentle_ding_dong.wav", duration=1.0):
    """创建一个温和的"叮咚"双音节提醒音"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 叮咚的两个音符
    ding_freq = 880  # A5
    dong_freq = 659.25  # E5
    
    # 创建两个音符，时间上有重叠
    ding_t = t[:int(sample_rate * 0.6)]
    dong_t = t[int(sample_rate * 0.3):]
    
    ding = np.sin(2 * np.pi * ding_freq * ding_t) * np.exp(-ding_t * 6)
    ding = np.append(ding, np.zeros(len(t) - len(ding)))
    
    dong = np.sin(2 * np.pi * dong_freq * dong_t) * np.exp(-dong_t * 4)
    dong = np.append(np.zeros(len(t) - len(dong)), dong)[:len(t)]
    
    # 添加一些泛音增加音色丰富度
    ding_harmonic = np.sin(2 * np.pi * ding_freq * 2 * ding_t) * 0.2 * np.exp(-ding_t * 8)
    ding_harmonic = np.append(ding_harmonic, np.zeros(len(t) - len(ding_harmonic)))
    
    dong_harmonic = np.sin(2 * np.pi * dong_freq * 1.5 * dong_t) * 0.3 * np.exp(-dong_t * 5)
    dong_harmonic = np.append(np.zeros(len(t) - len(dong_harmonic)), dong_harmonic)[:len(t)]
    
    # 组合所有声音
    sound = ding + dong + ding_harmonic + dong_harmonic
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_uplifting_notification(filename="uplifting_notification.wav", duration=1.5):
    """创建一个振奋人心的上升音效，适合激励和积极的提醒"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 使用上升的和弦进行
    # 开始是C大调，结束是明亮的E大调
    chord_progression = [
        [261.63, 329.63, 392.00],  # C 大三和弦
        [293.66, 369.99, 440.00],  # D 大三和弦
        [329.63, 415.30, 493.88]   # E 大三和弦
    ]
    
    sound = np.zeros_like(t)
    
    # 为每个和弦创建一个音段
    segment_duration = duration / len(chord_progression)
    for i, chord in enumerate(chord_progression):
        segment_start = int(i * segment_duration * sample_rate)
        segment_end = int((i + 1) * segment_duration * sample_rate)
        if segment_end > len(t):
            segment_end = len(t)
            
        segment_t = t[segment_start:segment_end] - t[segment_start]
        segment = np.zeros_like(segment_t)
        
        # 创建和弦
        for freq in chord:
            note = np.sin(2 * np.pi * freq * segment_t)
            # 添加明亮的泛音
            harmonic = np.sin(2 * np.pi * freq * 2 * segment_t) * 0.3
            segment += note + harmonic
            
        # 每个和弦有渐强效果
        envelope = np.linspace(0.5, 1.0, len(segment_t))
        if i == len(chord_progression) - 1:  # 最后一个和弦有衰减
            decay = np.exp(-(segment_t - segment_duration) * 8)
            envelope = envelope * decay
            
        sound[segment_start:segment_end] = segment * envelope
    
    # 添加明亮的高频点缀，增强振奋感
    sparkle_freq = 1200
    sparkle = np.sin(2 * np.pi * sparkle_freq * t) * np.exp(-t * 6) * 0.15
    
    # 组合所有元素
    sound = sound + sparkle
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_calming_waves(filename="calming_waves.wav", duration=3.0):
    """创建一个镇静舒缓的海浪般音效，帮助放松心情"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 创建基础的平静音调
    f_base = 174.61  # F3，低沉的音调
    f_fifth = 261.63  # C4，完美五度
    
    # 创建缓慢起伏的调制
    mod_freq = 0.5  # 半赫兹的调制，像海浪
    modulation = 0.5 + 0.5 * np.sin(2 * np.pi * mod_freq * t)
    
    # 基础音调
    base = np.sin(2 * np.pi * f_base * t) * 0.5
    fifth = np.sin(2 * np.pi * f_fifth * t) * 0.3
    
    # 添加轻微的调制
    base = base * modulation
    fifth = fifth * modulation
    
    # 添加柔和的白噪声模拟海浪声
    noise = np.random.normal(0, 0.1, len(t))
    # 用带通滤波器过滤白噪声
    b, a = signal.butter(3, [0.1, 0.3], 'band')
    filtered_noise = signal.filtfilt(b, a, noise)
    filtered_noise = filtered_noise * modulation * 0.4
    
    # 混合声音
    sound = base + fifth + filtered_noise
    
    # 添加渐入渐出效果
    fade_time = 0.5  # 秒
    fade_samples = int(fade_time * sample_rate)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    sound[:fade_samples] = sound[:fade_samples] * fade_in
    sound[-fade_samples:] = sound[-fade_samples:] * fade_out
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_energetic_alert(filename="energetic_alert.wav", duration=1.2):
    """创建一个充满活力的提醒音，让人兴奋并准备行动"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 创建一个有节奏感的提醒
    rhythm_pattern = np.zeros_like(t)
    beat_points = [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8]
    
    for beat in beat_points:
        idx = int(beat * sample_rate)
        if idx < len(t):
            # 创建一个短促的打击音
            beat_env = np.exp(-(t[idx:] - t[idx]) * 30)
            beat_sound = np.sin(2 * np.pi * 880 * t[idx:]) * beat_env
            
            # 根据节拍位置调整音高
            if beat in [0.0, 0.4, 0.8]:  # 主要节拍用高音
                freq = 880  # A5
            else:  # 次要节拍用较低的音
                freq = 659.25  # E5
                
            beat_sound = np.sin(2 * np.pi * freq * t[idx:]) * beat_env
            rhythm_pattern[idx:] += beat_sound[:len(t)-idx] * 0.5
    
    # 添加上升的背景音，增加兴奋感
    sweep_start = 400
    sweep_end = 800
    sweep_freq = sweep_start + (sweep_end - sweep_start) * t / duration
    sweep_phase = 2 * np.pi * np.cumsum(sweep_freq) / sample_rate
    background_sweep = np.sin(sweep_phase) * 0.3
    
    # 添加一些明亮的高频泛音增强活力
    sparkles = np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 5) * 0.2
    sparkles += np.sin(2 * np.pi * 1500 * t) * np.exp(-t * 6) * 0.15
    
    # 组合所有元素
    sound = rhythm_pattern + background_sweep + sparkles
    
    # 添加整体音量包络
    envelope = 1.0 - 0.7 * np.exp(-t * 1.5)
    envelope = envelope * np.exp(-(t-duration+0.3) * 4)
    sound = sound * envelope
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_peaceful_chimes(filename="peaceful_chimes.wav", duration=2.5):
    """创建一个平和宁静的风铃音效，给人一种平静祥和的感觉"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 使用五声音阶中的音符 (中国传统五声音阶: 宫商角徵羽)
    pentatonic_freqs = [523.25, 587.33, 659.25, 783.99, 880.00]  # C5, D5, E5, G5, A5
    
    sound = np.zeros_like(t)
    
    # 随机时间点触发不同的音符
    for i in range(12):
        # 随机选择一个音符和时间点
        freq = np.random.choice(pentatonic_freqs)
        time_point = np.random.uniform(0, duration * 0.8)
        idx = int(time_point * sample_rate)
        
        if idx < len(t):
            # 创建衰减音符
            note_t = t[idx:] - t[idx]
            decay = 2 + np.random.uniform(0, 2)  # 随机衰减率增加自然感
            note = np.sin(2 * np.pi * freq * note_t) * np.exp(-note_t * decay)
            
            # 添加泛音
            harmonic1 = np.sin(2 * np.pi * freq * 2 * note_t) * 0.2 * np.exp(-note_t * (decay+1))
            harmonic2 = np.sin(2 * np.pi * freq * 3 * note_t) * 0.1 * np.exp(-note_t * (decay+2))
            
            # 组合音符和泛音
            full_note = note + harmonic1 + harmonic2
            
            # 添加到总声音
            sound[idx:] += full_note[:len(t)-idx] * 0.25
    
    # 添加柔和的背景音
    bg_freq = 196.00  # G3
    background = np.sin(2 * np.pi * bg_freq * t) * 0.1
    background = background * np.exp(-t * 1.5)
    
    # 组合所有元素
    sound = sound + background
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.85  # 稍微降低音量使其更柔和
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_motivational_flourish(filename="motivational_flourish.wav", duration=2.0):
    """创建一个鼓舞人心的音乐性提醒，适合完成任务后的庆祝"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 创建一个上升的音阶
    scale_notes = [392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 783.99]  # G4 到 G5 的大调音阶
    
    sound = np.zeros_like(t)
    note_duration = duration / (len(scale_notes) + 2)  # 留一些时间给最后的和弦
    
    # 演奏上升的音阶
    for i, freq in enumerate(scale_notes):
        start_idx = int(i * note_duration * sample_rate)
        if start_idx < len(t):
            # 每个音符持续时间
            note_t = t[start_idx:] - t[start_idx]
            note_env = np.exp(-note_t * 8)  # 快速衰减
            note = np.sin(2 * np.pi * freq * note_t) * note_env
            
            # 添加泛音增强明亮感
            harmonic = np.sin(2 * np.pi * freq * 2 * note_t) * 0.3 * note_env
            
            # 加到总声音
            max_len = min(len(note), len(t)-start_idx)
            sound[start_idx:start_idx+max_len] += (note + harmonic)[:max_len] * 0.3
    
    # 最后添加一个明亮的和弦作为结束
    chord_start = int((len(scale_notes) - 1) * note_duration * sample_rate)
    if chord_start < len(t):
        chord_t = t[chord_start:] - t[chord_start]
        
        # 创建一个明亮的大三和弦
        root = scale_notes[-1]  # G5
        third = root * 5/4  # B5
        fifth = root * 3/2  # D6
        
        chord = (np.sin(2 * np.pi * root * chord_t) * 0.5 + 
                np.sin(2 * np.pi * third * chord_t) * 0.4 + 
                np.sin(2 * np.pi * fifth * chord_t) * 0.4)
        
        # 添加延音效果
        chord_env = np.exp(-chord_t * 2)
        
        # 加到总声音
        max_len = min(len(chord), len(t)-chord_start)
        sound[chord_start:chord_start+max_len] += (chord * chord_env)[:max_len] * 0.6
    
    # 添加整体音量包络
    envelope = np.ones_like(t)
    fade_out = np.exp(-(t-duration+0.4) * 5)
    envelope = envelope * fade_out
    sound = sound * envelope
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_focus_pulse(filename="focus_pulse.wav", duration=2.0):
    """创建一个有助于集中注意力的脉冲音效，适合工作和学习环境"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 创建一个缓慢脉动的基础音调
    base_freq = 220.00  # A3
    pulse_rate = 4  # Hz
    
    # 脉冲包络
    pulse_env = 0.5 + 0.5 * np.sin(2 * np.pi * pulse_rate * t)
    pulse_env = pulse_env ** 2  # 使脉冲形状更加尖锐
    
    # 主音调
    base_tone = np.sin(2 * np.pi * base_freq * t) * 0.4
    fifth_tone = np.sin(2 * np.pi * base_freq * 1.5 * t) * 0.3  # 完美五度
    
    # 应用脉冲调制
    modulated_tone = (base_tone + fifth_tone) * pulse_env
    
    # 添加高频组件增强清晰度
    high_tone = np.sin(2 * np.pi * base_freq * 4 * t) * 0.1
    high_tone = high_tone * pulse_env
    
    # 添加微妙的噪声增加深度
    noise = np.random.normal(0, 0.05, len(t))
    b, a = signal.butter(3, 0.1, 'low')
    filtered_noise = signal.filtfilt(b, a, noise)
    filtered_noise = filtered_noise * pulse_env * 0.2
    
    # 组合所有声音
    sound = modulated_tone + high_tone + filtered_noise
    
    # 添加渐入渐出
    fade_in = np.linspace(0, 1, int(0.1 * sample_rate))
    fade_out = np.linspace(1, 0, int(0.3 * sample_rate))
    
    if len(fade_in) < len(sound):
        sound[:len(fade_in)] *= fade_in
    if len(fade_out) < len(sound):
        sound[-len(fade_out):] *= fade_out
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.85
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_gentle_awakening(filename="gentle_awakening.wav", duration=3.5):
    """创建一个柔和的唤醒音效，适合闹钟或冥想结束提醒"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 基于自然音调的和声
    f1 = 261.63  # C4
    f2 = 329.63  # E4
    f3 = 392.00  # G4
    f4 = 523.25  # C5
    
    # 创建缓慢的颤音效果
    vibrato_rate = 5
    vibrato_depth = 0.007
    vibrato = np.sin(2 * np.pi * vibrato_rate * t) * vibrato_depth
    
    # 创建主要音调，逐渐加入不同的音符
    phases = []
    for i, f in enumerate([f1, f2, f3, f4]):
        # 每个音符在不同时间点淡入
        delay = i * 0.6
        idx = int(delay * sample_rate)
        if idx < len(t):
            # 应用颤音
            f_vibrato = f * (1 + vibrato)
            # 累积相位确保连续性
            phase_t = np.zeros_like(t)
            phase_t[idx:] = t[idx:] - t[idx]
            phase = 2 * np.pi * f_vibrato * phase_t
            
            # 应用淡入
            fade_in_len = int(0.8 * sample_rate)
            env = np.zeros_like(t)
            if idx + fade_in_len < len(t):
                env[idx:idx+fade_in_len] = np.linspace(0, 1, fade_in_len)
                env[idx+fade_in_len:] = 1
                
                phases.append((phase, env, 0.3 - i * 0.05))
    
    # 组合所有相位
    sound = np.zeros_like(t)
    for phase, env, amp in phases:
        sound += np.sin(phase) * env * amp
    
    # 添加轻微的合成风铃声
    for i in range(5):
        time_point = duration * 0.5 + i * 0.3
        if time_point < duration:
            idx = int(time_point * sample_rate)
            note_freq = f4 * (1 + i * 0.2)  # 越来越高的音符
            note_t = t[idx:] - t[idx]
            note_env = np.exp(-note_t * 4)
            note = np.sin(2 * np.pi * note_freq * note_t) * note_env * 0.15
            
            if idx < len(sound):
                max_len = min(len(note), len(sound) - idx)
                sound[idx:idx+max_len] += note[:max_len]
    
    # 应用主包络
    main_env = np.exp(-(t-duration+0.8) * 3)  # 最后有一个缓慢的淡出
    sound = sound * main_env
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath

def create_achievement_fanfare(filename="achievement_fanfare.wav", duration=2.2):
    """创建一个庆祝成就的欢快号角音效，适合完成重要任务时的提醒"""
    filepath = os.path.join(output_dir, filename)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 设计一个欢快的号角主题
    # 主旋律基于大三和弦的分解和装饰
    melody_notes = [
        (0.0, 392.00, 0.2),   # G4
        (0.2, 523.25, 0.2),   # C5
        (0.4, 659.25, 0.3),   # E5
        (0.7, 783.99, 0.7),   # G5
        (1.4, 659.25, 0.25),  # E5
        (1.65, 739.99, 0.55)  # F#5
    ]
    
    sound = np.zeros_like(t)
    
    # 创建每个音符
    for start_time, freq, note_duration in melody_notes:
        idx = int(start_time * sample_rate)
        end_idx = int((start_time + note_duration) * sample_rate)
        
        if idx < len(t) and end_idx <= len(t):
            note_t = t[idx:end_idx] - t[idx]
            
            # 创建号角音色（使用方波和三角波的混合）
            square = np.sign(np.sin(2 * np.pi * freq * note_t)) * 0.3
            triangle = 2 * np.abs(2 * (note_t * freq - np.floor(note_t * freq + 0.5))) - 1
            triangle = triangle * 0.3
            
            # 添加一些泛音
            sine = np.sin(2 * np.pi * freq * note_t) * 0.2
            harmonic = np.sin(2 * np.pi * freq * 1.5 * note_t) * 0.15
            
            # 组合音色
            note_sound = square + triangle + sine + harmonic
            
            # 应用包络
            attack = 0.1
            decay = 0.2
            attack_samples = int(attack * sample_rate)
            decay_samples = int(decay * sample_rate)
            
            env = np.ones_like(note_t)
            if attack_samples < len(note_t):
                env[:attack_samples] = np.linspace(0, 1, attack_samples)
            if decay_samples < len(note_t):
                env[-decay_samples:] = np.linspace(1, 0.7, decay_samples)
            
            # 应用振动效果
            vibrato_rate = 6
            vibrato_depth = 0.03
            vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * note_t)
            
            # 最终音符声音
            final_note = note_sound * env * vibrato
            
            # 添加到总音效
            sound[idx:end_idx] += final_note
    
    # 添加一点混响效果
    reverb_delay = int(0.05 * sample_rate)
    reverb = np.zeros_like(sound)
    if reverb_delay < len(sound):
        reverb[reverb_delay:] = sound[:-reverb_delay] * 0.3
        sound = sound + reverb
    
    # 标准化并转换
    sound = sound / np.max(np.abs(sound)) * 0.9
    sound_int = np.int16(sound * 32767)
    
    wavfile.write(filepath, sample_rate, sound_int)
    return filepath


# 生成所有提醒音
print("正在生成多种提醒音...")
files = [
    create_clean_bell(),
    create_warm_notification(),
    create_soft_chime(),
    create_modern_alert(),
    create_gentle_ding_dong(),
    create_uplifting_notification(),
    create_calming_waves(),
    create_energetic_alert(),
    create_peaceful_chimes(),
    create_motivational_flourish(),
    create_focus_pulse(),
    create_gentle_awakening(),
    create_achievement_fanfare()
]

print("\n所有提醒音已成功生成在以下位置:")
for file in files:
    print(f"- {file}")
print("\n你可以根据喜好选择使用任何一种提醒音。")