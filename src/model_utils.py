#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/12
# @Author : julong@111.com
# @Description : 模型相关工具函数

from pathlib import Path
import sys
import os
import subprocess
import tempfile
import stat


def is_model_folder_complete(model_base_path, essential_files):
    """
    Checks if a model folder is complete by verifying the existence and integrity of essential files.

    Args:
        model_base_path (str or Path): The base directory of the model.
        essential_files (list): A list of filenames that are considered essential.

    Returns:
        bool: True if the model is complete, False otherwise.
    """
    base_path = Path(model_base_path)
    if not base_path.is_dir():
        return False

    snapshots_path = base_path / "snapshots"
    if not snapshots_path.is_dir():
        return False

    try:
        snapshot_dirs = [d for d in snapshots_path.iterdir() if d.is_dir()]
        if not snapshot_dirs:
            return False
        
        # A model is complete if any of its snapshot directories is complete
        for snapshot_dir in snapshot_dirs:
            is_snapshot_complete = True
            for file_name in essential_files:
                file_path = snapshot_dir / file_name
                if not file_path.is_file():
                    is_snapshot_complete = False
                    break  # Missing a file, this snapshot is incomplete

                # For the main model file, check if its size is substantial
                if file_name == "pytorch_model.bin":
                    # If model file is less than 1MB, it's likely incomplete.
                    if file_path.stat().st_size < 1_000_000:
                        is_snapshot_complete = False
                        break  # Incomplete file, this snapshot is incomplete
            
            if is_snapshot_complete:
                return True  # Found a complete snapshot

        return False  # No complete snapshot was found
    except (OSError, FileNotFoundError):
        return False


def download_model(model_type, log_queue):
    """
    Downloads a model using the hf command-line tool with progress logging.
    A new console window will be opened to show the download progress.

    Args:
        model_type (str): The type of the model to download ('opus' or 'nllb').
        log_queue (queue.Queue): The queue to put log messages into.
    """
    model_map = {
        "opus": "Helsinki-NLP/opus-mt-en-zh",
        "nllb": "facebook/nllb-200-distilled-600M"
    }
    model_id = model_map.get(model_type)
    if not model_id:
        log_queue.put(f"❌ 错误: 无效的模型类型 '{model_type}'\n")
        return

    log_queue.put(f"--- 开始使用 hf cli 下载 {model_type.upper()} 模型 ---\n")
    log_queue.put(f"模型ID: {model_id}\n")

    hf_mirror = "https://hf-mirror.com"
    log_queue.put(f"使用镜像: {hf_mirror}\n")

    cli_name = "hf"
    cli_path = Path(sys.executable).parent / cli_name
    if not cli_path.exists():
        # Fallback for windows where it might be in Scripts and have .exe
        cli_path = Path(sys.executable).parent / 'Scripts' / f'{cli_name}.exe'

    if not cli_path.exists():
        log_queue.put(f"❌ 错误: 未找到 '{cli_name}' 命令。\n")
        log_queue.put("请确保 'huggingface-hub' 库已正确安装 (pip install huggingface-hub)。\n")
        return

    project_root = Path(__file__).parent.parent
    cache_dir = project_root / "models"
    
    log_queue.put(f"下载路径: {cache_dir.resolve()}\n\n")
    log_queue.put("🚀 即将打开一个新的控制台窗口进行下载，请稍候...下载完成后请重启软件\n")

    # The CLI argument is `--cache-dir`, not `--cache` as in the original code.
    command = [
        str(cli_path.resolve()),
        "download",
        model_id,
        "--cache-dir",
        str(cache_dir.resolve()),
    ]

    returncode = -1
    
    try:
        if sys.platform == "win32":
            env = os.environ.copy()
            env["HF_ENDPOINT"] = hf_mirror
            process = subprocess.Popen(
                command,
                env=env,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            process.wait()
            returncode = process.returncode
        elif sys.platform == "darwin":
            # On macOS, create a temporary shell script and run it with Terminal.
            # The `-W` flag makes `open` wait for the script to finish.
            script_content = f'''#!/bin/bash
export HF_ENDPOINT="{hf_mirror}"
{' '.join(f'"{arg}"' for arg in command)}
'''
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.sh') as f:
                script_path = f.name
                f.write(script_content)

            os.chmod(script_path, stat.S_IRWXU)
            
            process = subprocess.run(['open', '-a', 'Terminal.app', '-W', script_path])
            returncode = process.returncode
            os.remove(script_path)
        else:
            # For other OS (e.g., Linux), use the original method but with fixes.
            log_queue.put("非 Windows/macOS 平台，将在后台进行下载...\n")
            env = os.environ.copy()
            env['HF_ENDPOINT'] = hf_mirror
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=project_root,
                env=env
            )

            for line in iter(process.stdout.readline, ''):
                if not line:
                    break
                log_queue.put(line)
            
            process.stdout.close()
            process.wait()
            returncode = process.returncode

        if returncode == 0:
            log_queue.put(f"\n🎉 模型 '{model_id}' 下载成功!\n")
        else:
            log_queue.put(f"\n❌ 模型下载失败，退出代码: {returncode}\n")

    except Exception as e:
        log_queue.put(f"\n❌ 执行下载时发生异常: {e}\n")
