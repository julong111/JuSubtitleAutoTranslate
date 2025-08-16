#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/10
# @Author : julong@111.com
# @Description : JuSubTitleAutoTranslate - SRT字幕文件AI自动翻译脚本
#   支持 Helsinki-NLP/opus-mt-en-zh（速度快）和facebook/nllb-200-distilled-600M（质量高）两种模型

import argparse
import logging
import sys
import time
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from language_code_utils import (
    nllb_language_codes,
    # ISO_639_2T_to_ISO_639_1,
    # ISO_15924_to_ISO_3166_1,
    # ISO_639_2T_ISO_15924_to_ISO_639_1_ISO_3166_1,
    # ISO_639_1_to_ISO_639_2T,
    # ISO_3166_1_to_ISO_15924,
    # ISO_639_1_ISO_3166_1_to_ISO_639_2T_ISO_15924
)
from srt_utils import (
    clean_text,
    get_output_file,
    parse_srt_file,
    validate_file_format,
    write_srt_file,
)

# 新增：调试模式，跳过模型加载和翻译
debug_skip = False

TRANSLATES_MODEL_MAP = {
    "opus": "Helsinki-NLP/opus-mt-en-zh",
    "nllb": "facebook/nllb-200-distilled-600M",
}


# 新增的函数，用于处理单个文件的所有逻辑
def process_single_file(input_path, output_path, args, tokenizer, model):
    """
    处理单个SRT文件的完整流程：解析、翻译、保存。
    """
    try:
        logging.info("📖 正在解析文件...")
        subtitles = parse_srt_file(input_path)
        logging.info(f"✅ 解析完成，共找到 {len(subtitles)} 条字幕")
        elapsed_time = 1
        # 翻译字幕
        if debug_skip:
            logging.info("🐞 调试模式已开启: 跳过翻译步骤。")
            translated_count = 0
            # 保持原始文本不变
            for i, subtitle in enumerate(subtitles):
                subtitle["text"] = subtitle["text"]
                translated_count += 1
        else:
            # 翻译字幕
            logging.info(f"🌐 正在使用{args.model}模型翻译字幕...")

            translated_count = 0
            start_time = time.time()

            for i, subtitle in enumerate(subtitles):
                logging.info(f"翻译进度: {i + 1}/{len(subtitles)}")

                # 根据模型类型选择性地传递参数
                if args.model == "nllb":
                    # NLLB模型需要指定源语言和目标语言
                    input_text = f"{args.source_lang} {subtitle['text']}"

                    inputs = tokenizer(
                        input_text,
                        return_tensors="pt",
                        padding=True,
                        truncation=True,
                        max_length=args.max_length,
                    )
                    outputs = model.generate(
                        **inputs,
                        forced_bos_token_id=tokenizer.convert_tokens_to_ids(
                            args.target_lang
                        ),
                    )
                    translated_text = tokenizer.decode(
                        outputs[0], skip_special_tokens=True
                    )
                else:  # 'opus'
                    inputs = tokenizer(
                        subtitle["text"],
                        return_tensors="pt",
                        padding=True,
                        truncation=True,
                        max_length=args.max_length,
                    )
                    outputs = model.generate(**inputs)
                    translated_text = tokenizer.decode(
                        outputs[0], skip_special_tokens=True
                    )

                subtitle["text"] = translated_text
                translated_count += 1

            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"\n✅ 翻译完成，共翻译 {translated_count} 条字幕")
            logging.info(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
            logging.info(f"🚀 平均速度: {len(subtitles) / elapsed_time:.2f} 条/秒")

        logging.info("💾 正在保存翻译后的文件...")
        if debug_skip:
            logging.info("🐞 调试模式已开启: 跳过文件保存步骤。")
            # 仅打印文件名，不实际保存
            print(f"调试模式：文件 {output_path} 将被保存，但实际未保存。")
        else:
            write_srt_file(subtitles, output_path)

        logging.info(f"✅ 文件保存成功: {output_path}")

        logging.info("📊 统计信息:")
        logging.info(f"   - 总字幕行数: {len(subtitles)}")
        logging.info(f"   - 翻译成功行数: {translated_count}")
        logging.info(f"   - 总耗时: {elapsed_time:.2f} 秒")
        logging.info(f"   - 平均速度: {len(subtitles) / elapsed_time:.2f} 条/秒")

    except Exception as e:
        logging.error(f"❌ 处理文件 {input_path.name} 时发生错误: {e}")
        return False, 0

    return True, translated_count


# 新增的函数，用于处理整个文件夹的批处理逻辑
def process_directory(input_dir, output_dir, args, tokenizer, model):
    """
    处理指定输入目录下的所有SRT文件，并将结果保存到输出目录。
    """
    if not input_dir.is_dir():
        logging.error(f"❌ 错误：输入目录不存在: {input_dir}")
        return

    if not output_dir.exists():
        logging.info(f"📁 创建输出目录: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

    srt_files = list(input_dir.glob("*.srt"))
    if not srt_files:
        logging.info(f"💡 在目录 {input_dir} 中未找到任何 srt 文件。")
        return

    logging.info(f"🔍 找到 {len(srt_files)} 个 srt 文件，准备开始批处理...")

    total_files = len(srt_files)
    processed_files = 0
    successful_translations = 0

    for i, input_path in enumerate(srt_files):
        try:
            output_path = get_output_file(input_path, output_dir)

            logging.info(
                f"\n--- 正在处理文件 [{i + 1}/{total_files}]: {input_path.name} -> {output_path}"
            )

            success, translated_count = process_single_file(
                input_path, output_path, args, tokenizer, model
            )
            if success:
                processed_files += 1
                successful_translations += translated_count
        except Exception as e:
            logging.error(f"❌ 处理文件 {input_path.name} 时发生错误: {e}")

    logging.info("\n=== 批处理完成 ===")
    logging.info(f"   - 总文件数: {total_files}")
    logging.info(f"   - 成功处理文件数: {processed_files}")
    logging.info(f"   - 总计翻译行数: {successful_translations}")
    logging.info("===================")


def load_model(model_type: str, model_path: str = None, auto_download: bool = False):
    """
    通用模型加载函数，支持opus和nllb。
    model_type: "opus" 或 "nllb"
    model_path: 本地模型路径或下载目录
    auto_download: 是否自动下载
    """
    model_name = TRANSLATES_MODEL_MAP.get(model_type)
    if not model_name:
        raise ValueError(f"不支持的模型类型: {model_type}")
    try:
        if auto_download or not model_path:
            # 下载到指定目录或默认缓存
            cache_dir = model_path if model_path else None
            logging.info(
                f"🔄 正在自动下载模型 {model_name} 到 {cache_dir or '默认缓存目录'}"
            )
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name, cache_dir=cache_dir
            )
        else:
            # 加载本地模型
            logging.info(f"🔒 正在加载本地模型 {model_path}")
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_path, local_files_only=True
            )
        logging.info(f"✅ {model_type} 模型加载成功")
        return tokenizer, model
    except Exception as e:
        if auto_download:
            logging.info(f"❌ 模型自动下载失败: {e}")
            logging.info("💡 解决方案：")
            logging.info("1. 检查网络连接并重试")
            logging.info("2. 手工下载并指定正确的模型路径")
        else:
            logging.info("❌ 本地模型加载失败")
            logging.info("💡 解决方案：")
            logging.info("1. 使用 --auto-download 参数自动下载模型")
            logging.info(f"2. 确保模型路径正确 {model_path}")
            logging.info("3. 手动下载模型到指定目录")
        raise


def translate_with_opus(text: str, tokenizer, model, max_length: int = 512) -> str:
    """使用OPUS-MT模型翻译文本"""
    try:
        clean_text_result = clean_text(text)

        if not clean_text_result.strip():
            return text

        inputs = tokenizer(
            clean_text_result,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        )
        outputs = model.generate(**inputs)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return result
    except Exception as e:
        logging.info(f"翻译文本时出错: {e}")
        return text


def translate_with_nllb(
    text: str,
    tokenizer,
    model,
    source_lang: str = "eng_Latn",
    target_lang: str = "zho_Hans",
    max_length: int = 512,
) -> str:
    """使用NLLB模型翻译文本"""
    try:
        clean_text_result = clean_text(text)

        if not clean_text_result.strip():
            return text

        input_text = f"{source_lang} {clean_text_result}"

        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        )
        outputs = model.generate(
            **inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang)
        )
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return result
    except Exception as e:
        logging.info(f"翻译文本时出错: {e}")
        return text


def main():
    # 1. 解析命令行参数
    parser = argparse.ArgumentParser(
        description="JuSubTrans - 统一SRT字幕文件AI自动翻译脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用OPUS-MT模型（速度快）   默认模型
  python translate.py -i input.srt
  
  # 使用NLLB模型（质量高）
  python translate.py -di ./input_dir/ -do ./output_dir/
  
  # 指定模型路径
  python translate.py -i input.srt -m opus --modelpath /path/to/model
  
  # 自动下载模型   同时指定下载位置（非必填）
  python translate.py -di ./input_dir/ -do ./output_dir/ --auto-download --modelpath /path/to/model
        """,
    )

    # 创建互斥组，用于单文件或批处理模式
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-i", "--input_file", help="输入的SRT文件路径 (单文件模式)")
    mode_group.add_argument(
        "-di", "--input_dir", help="输入的SRT文件夹路径 (批处理模式)"
    )

    # 非互斥的参数
    parser.add_argument(
        "-o",
        "--output",
        help="输出文件路径（可选，仅单文件模式有效，默认在原文件名后加模型标识）",
    )
    parser.add_argument(
        "-do",
        "--output_dir",
        help="输出文件夹路径（可选，仅批处理模式有效，默认在输入文件夹内创建translated子目录）",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["opus", "nllb"],
        default="opus",
        help="选择翻译模型: opus(速度快) 或 nllb(质量高) [默认: opus]",
    )
    parser.add_argument("--model_path", help="模型路径（可选，使用默认路径）")
    parser.add_argument(
        "--auto-download",
        default=False,
        action="store_true",
        help="如果本地模型不存在，自动从Hugging Face下载（默认：否）",
    )
    parser.add_argument(
        "--source_lang",
        default="eng_Latn",
        help="源语言代码（仅NLLB模型有效，默认：eng_Latn 英文）",
    )
    parser.add_argument(
        "--target_lang",
        default="zho_Hans",
        help="目标语言代码（仅NLLB模型有效，默认：zho_Hans 简体中文）",
    )
    parser.add_argument(
        "--max_length", type=int, default=512, help="最大输入长度（默认：512）"
    )

    args = parser.parse_args()
    logging.debug(f"DEBUG: args = {args}")

    nomodelpath = False
    # 设置默认模型路径
    if not args.model_path:
        nomodelpath = True
        if args.model == "opus":
            args.model_path = "./models/models--Helsinki-NLP--opus-mt-en-zh/snapshots/408d9bc410a388e1d9aef112a2daba955b945255"
        else:  # nllb
            args.model_path = "./models/models--facebook--nllb-200-distilled-600M/snapshots/f8d333a098d19b4fd9a8b18f94170487ad3f821d"

    # 打印一些基本信息
    logging.info("🎯 JuSubTitleAutoTranslate - 字幕翻译工具")
    logging.info(f"🤖 模型: {args.model}")
    logging.info(f"📂 模型路径: {args.model_path}")
    logging.info(f"⬇️  自动下载: {'是' if args.auto_download else '否'}")
    argmodelpath = Path(args.model_path)
    if args.auto_download:
        if nomodelpath:
            argmodelpath = "./models/"
        logging.info(f"📁 下载目录: {argmodelpath}")

    # 处理 NLLB 模型的语言代码
    if args.model == "nllb":
        logging.info(f"🌐 源语言: {args.source_lang}")
        logging.info(f"🌐 目标语言: {args.target_lang}")
        # 1. 检查源语言是否已经是NLLB官方代码
        if args.source_lang.lower() not in nllb_language_codes:
            logging.error(
                f"⚠️ 无法识别的语言代码: {args.source_lang}，根据nllb模型规定请使用ISO 639-2/T + ISO 15924 格式的语言代码。"
            )
            return
        # 2. 检查目标语言是否已经是NLLB官方代码
        if args.target_lang.lower() not in nllb_language_codes:
            logging.error(
                f"⚠️ 无法识别的语言代码: {args.source_lang}，根据nllb模型规定请使用ISO 639-2/T + ISO 15924 格式的语言代码。"
            )
            return

    # 2. 统一加载模型和分词器
    tokenizer, model = None, None
    if debug_skip:
        logging.info("🐞 调试模式已开启: 跳过模型加载和翻译。")
    else:
        try:
            tokenizer, model = load_model(args.model, argmodelpath, args.auto_download)
        except Exception as e:
            logging.error(f"❌ 模型加载失败: {e}")
            sys.exit(1)

    # 3. 根据参数选择模式并执行
    if args.input_file:
        # 单文件模式
        input_path = Path(args.input_file)
        if not validate_file_format(input_path):
            logging.error(f"❌ 错误：输入文件格式暂不支持: {input_path}")
            sys.exit(1)

        output_path = get_output_file(input_path, args.output)

        logging.info("--- 进入单文件翻译模式 ---")
        logging.info(f"📁 输入文件: {input_path}")
        logging.info(f"📁 输出文件: {output_path}")

        success, _ = process_single_file(
            input_path, output_path, args, tokenizer, model
        )
        if success:
            logging.info(f"🎉 翻译完成！输出文件: {output_path}")

    elif args.input_dir:
        # 批处理模式
        input_dir = Path(args.input_dir)
        output_dir = (
            Path(args.output_dir) if args.output_dir else input_dir / "translated"
        )

        logging.info("--- 进入批处理翻译模式 ---")
        logging.info(f"📁 输入目录: {input_dir}")
        logging.info(f"📁 输出目录: {output_dir}")

        process_directory(input_dir, output_dir, args, tokenizer, model)

    else:
        # 此处理论上不会执行，因为 argparse 的 required=True 已经强制用户提供了参数
        logging.error("❌ 错误：请提供 -i 或 -di 参数")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Starting JuSubTitleAutoTranslate...")
    main()
