#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/10
# @Author : julong@111.com
# @File : srt_utils.py
# @Description : SRT字幕文件通用处理工具

import re
from pathlib import Path
from typing import List, Dict, Any

def parse_srt_file(file_path: Path) -> List[Dict[str, Any]]:
    """解析SRT文件，返回字幕条目列表
    
    Args:
        file_path: SRT文件路径
        
    Returns:
        字幕条目列表，每个条目包含index, start_time, end_time, text
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
    
    # SRT格式：序号 + 时间码 + 文本内容 + 空行
    pattern = r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\s+([\s\S]*?)(?=\n\s*\n|\s*$)'
    matches = re.findall(pattern, content)
    
    subtitles = []
    for match in matches:
        subtitle = {
            'index': int(match[0]),
            'start_time': match[1],
            'end_time': match[2],
            'text': match[3].strip()
        }
        subtitles.append(subtitle)
    
    return subtitles

def write_srt_file(subtitles: List[Dict[str, Any]], output_path: Path) -> None:
    """将字幕条目写入SRT文件
    
    Args:
        subtitles: 字幕条目列表
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{subtitle['start_time']} --> {subtitle['end_time']}\n")
            f.write(f"{subtitle['text']}\n\n")

def clean_text(text: str) -> str:
    """清理文本，移除HTML标签和特殊字符
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    # 移除HTML标签
    clean_text = re.sub(r'<[^>]+>', '', text)
    # 保留基本标点符号和字符
    clean_text = re.sub(r'[^\w\s.,!?;:()\-\'\"]', '', clean_text)
    return clean_text

def validate_srt_file(file_path: Path) -> bool:
    """验证SRT文件格式是否正确
    
    Args:
        file_path: SRT文件路径
        
    Returns:
        文件格式是否有效
    """
    # file_path = Path(file_path)
    # print(f"[DEBUG] 检查文件路径: {file_path.resolve()}")
     
    if not file_path.exists():
        return False
    
    if not file_path.suffix.lower() == '.srt':
        return False
    
    try:
        subtitles = parse_srt_file(file_path)
        return len(subtitles) > 0
    except Exception:
        return False

def get_output_filename(input_path: Path, suffix: str = "_translated") -> Path:
    """生成输出文件名
    
    Args:
        input_path: 输入文件路径
        suffix: 文件名后缀
        
    Returns:
        输出文件路径
    """
    return input_path.parent / f"{input_path.stem}{suffix}{input_path.suffix}"
