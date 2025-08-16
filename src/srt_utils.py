#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/10
# @Author : julong@111.com
# @File : srt_utils.py
# @Description : SRT字幕文件通用处理工具

import re
from pathlib import Path
from typing import List, Dict, Any
from typing import Optional


def parse_srt_file(file_path: Path) -> List[Dict[str, Any]]:
    """解析SRT文件，返回字幕条目列表

    Args:
        file_path: SRT文件路径

    Returns:
        字幕条目列表，每个条目包含index, start_time, end_time, text
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            with open(file_path, "r", encoding="gbk") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()

    # SRT格式：序号 + 时间码 + 文本内容 + 空行
    pattern = r"(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\s+([\s\S]*?)(?=\n\s*\n|\s*$)"
    matches = re.findall(pattern, content)

    subtitles = []
    for match in matches:
        subtitle = {
            "index": int(match[0]),
            "start_time": match[1],
            "end_time": match[2],
            "text": match[3].strip(),
        }
        subtitles.append(subtitle)

    return subtitles


def write_srt_file(subtitles: List[Dict[str, Any]], output_path: Path) -> None:
    """将字幕条目写入SRT文件

    Args:
        subtitles: 字幕条目列表
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
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
    clean_text = re.sub(r"<[^>]+>", "", text)
    # 保留基本标点符号和字符
    clean_text = re.sub(r"[^\w\s.,!?;:()\-\'\"]", "", clean_text)
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

    if not file_path.suffix.lower() == ".srt":
        return False

    try:
        subtitles = parse_srt_file(file_path)
        return len(subtitles) > 0
    except Exception:
        return False


def get_output_file(input_path: Path, output: Optional[str] = None) -> Path:
    """
    一个假设的 get_output_file 函数。为了让测试通过，它应该能处理所有情况。
    """
    if not isinstance(input_path, Path):
        input_path = Path(input_path)

    if output is None:
        # 情况 1: output 为 None
        return input_path.with_name(f"{input_path.stem}.translated{input_path.suffix}")

    output_path = Path(output)

    # 情况 2: output 是一个目录
    if output_path.is_dir():
        translated_filename = f"{input_path.stem}.translated{input_path.suffix}"
        return output_path / translated_filename

    # 情况 3: output 是一个完整的文件名
    return output_path
