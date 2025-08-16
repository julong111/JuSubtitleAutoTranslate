#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path


def clean_directory():
    """
    清理当前目录下的a.srt文件以及out文件夹中所有.srt文件。
    """
    current_dir = Path.cwd()

    files_to_be_deleted = []

    # 检查并准备删除 out 文件夹中的所有 .srt 文件
    out_dir = current_dir / "output"
    if out_dir.exists() and out_dir.is_dir():
        for srt_file in out_dir.glob("*.srt"):
            files_to_be_deleted.append(srt_file)

    if not files_to_be_deleted:
        print("🎉 未找到需要清理的 .srt 文件。")
        return

    print("⚠️ 以下文件将被永久删除！")
    for f in files_to_be_deleted:
        print(f" - {f}")

    for f in files_to_be_deleted:
        try:
            f.unlink()  # 删除文件
            print(f"✅ 已删除：{f}")
        except OSError as e:
            print(f"❌ 删除失败 {f}: {e}")
    print("\n✅ 清理完成！")


if __name__ == "__main__":
    clean_directory()
