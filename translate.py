#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/10
# @Author : julong@111.com
# @Description : JuSubTitleAutoTranslate - SRT字幕文件AI自动翻译脚本
#   支持 Helsinki-NLP/opus-mt-en-zh（速度快）和facebook/nllb-200-distilled-600M（质量高）两种模型

import argparse
import sys
import time
import logging
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from srt_utils import (
    parse_srt_file, 
    write_srt_file, 
    clean_text, 
    validate_srt_file,
    get_output_filename
)

MODEL_MAP = {
    "opus": "Helsinki-NLP/opus-mt-en-zh",
    "nllb": "facebook/nllb-200-distilled-600M"
}

def load_model(model_type: str, model_path: str = None, auto_download: bool = False):
    """
    通用模型加载函数，支持opus和nllb。
    model_type: "opus" 或 "nllb"
    model_path: 本地模型路径或下载目录
    auto_download: 是否自动下载
    """
    model_name = MODEL_MAP.get(model_type)
    if not model_name:
        raise ValueError(f"不支持的模型类型: {model_type}")
    try:
        if auto_download or not model_path:
            # 下载到指定目录或默认缓存
            cache_dir = model_path if model_path else None
            logging.info(f"🔄 正在自动下载模型 {model_name} 到 {cache_dir or '默认缓存目录'}")
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)
        else:
            # 加载本地模型
            logging.info(f"🔒 正在加载本地模型 {model_path}")
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True)
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

class TranslationModel:
    """翻译模型基类"""

    def __init__(self, name: str):
        self.name = name
     
    def translate_text(self, text: str, tokenizer, model, **kwargs) -> str:
        """翻译文本"""
        raise NotImplementedError

class OPUSMTModel(TranslationModel):
    """OPUS-MT模型实现"""
    
    def __init__(self):
        super().__init__(name="OPUS-MT") 

    def translate_text(self, text: str, tokenizer, model, max_length: int = 512) -> str:
        """使用OPUS-MT模型翻译文本"""
        try:
            clean_text_result = clean_text(text)
            
            if not clean_text_result.strip():
                return text
            
            inputs = tokenizer(clean_text_result, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
            outputs = model.generate(**inputs)
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return result
        except Exception as e:
            logging.info(f"翻译文本时出错: {e}")
            return text

class NLLBModel(TranslationModel):
    """NLLB模型实现"""
    
    def __init__(self):
        super().__init__(name="NLLB-200-distilled-600M")
    
    def translate_text(self, text: str, tokenizer, model, source_lang: str = "eng_Latn", 
                      target_lang: str = "zho_Hans", max_length: int = 512) -> str:
        """使用NLLB模型翻译文本"""
        try:
            clean_text_result = clean_text(text)
            
            if not clean_text_result.strip():
                return text
            
            # NLLB模型需要指定源语言和目标语言
            input_text = f"{source_lang} {clean_text_result}"
            
            inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
            # outputs = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
            outputs = model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang))
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return result
        except Exception as e:
            logging.info(f"翻译文本时出错: {e}")
            return text

def get_model_class(model_type: str) -> TranslationModel:
    """根据模型类型获取对应的模型类"""
    model_map = {
        'opus': OPUSMTModel,
        'nllb': NLLBModel
    }
    
    model_type_lower = model_type.lower()
    for key, model_class in model_map.items():
        if key in model_type_lower:
            return model_class()
    
    raise ValueError(f"不支持的模型类型: {model_type}。支持的类型: opus, nllb")

def translate_subtitles(subtitles: list, model_instance: TranslationModel, 
                       tokenizer, model, **kwargs) -> tuple:
    """翻译字幕列表"""
    logging.info(f"🌐 正在使用{model_instance.name}模型翻译字幕...")
    
    translated_count = 0
    start_time = time.time()
    
    for i, subtitle in enumerate(subtitles):
        logging.info(f"翻译进度: {i+1}/{len(subtitles)}")
        
        # 翻译文本
        translated_text = model_instance.translate_text(subtitle['text'], tokenizer, model, **kwargs)
        subtitle['text'] = translated_text
        translated_count += 1
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    logging.info(f"\n✅ 翻译完成，共翻译 {translated_count} 条字幕")
    logging.info(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
    logging.info(f"🚀 平均速度: {len(subtitles)/elapsed_time:.2f} 条/秒")
    
    return translated_count, elapsed_time

def main():
    parser = argparse.ArgumentParser(
        description='JuSubTrans - 统一SRT字幕文件AI自动翻译脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用OPUS-MT模型（速度快）   默认模型
  python translate.py -i input.srt
  
  # 使用NLLB模型（质量高）
  python translate.py -i input.srt -m nllb
  
  # 指定模型路径
  python translate.py -i input.srt -m opus --modelpath /path/to/model
  
  # 自动下载模型   同时指定下载位置（非必填）
  python translate.py -i input.srt -m nllb --auto-download --modelpath /path/to/model
        """
    )
    
    parser.add_argument('-i','--input_file', required=True, help='输入的SRT文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（可选，默认在原文件名后加模型标识.zh-CN）')
    parser.add_argument('-m', '--model', choices=['opus', 'nllb'], default='opus',
                       help='选择翻译模型: opus(速度快) 或 nllb(质量高) [默认: opus]')
    parser.add_argument('--modelpath', 
                       help='模型路径（可选，使用默认路径）')
    parser.add_argument('--auto-download', default=False, action='store_true',
                       help='如果本地模型不存在，自动从Hugging Face下载（默认：否）')
    parser.add_argument('--source_lang', default='eng_Latn', 
                       help='源语言代码（仅NLLB模型有效，默认：eng_Latn 英文）')
    parser.add_argument('--target_lang', default='zho_Hans', 
                       help='目标语言代码（仅NLLB模型有效，默认：zho_Hans 简体中文）')
    parser.add_argument('--max-length', type=int, default=512,
                       help='最大输入长度（默认：512）')
    
    args = parser.parse_args()
    logging.debug(f"DEBUG: args = {args}")
    
    # 检查输入文件
    input_path = Path(args.input_file)
    if not validate_srt_file(input_path):
        logging.info(f"❌ 错误：输入文件无效或不是SRT格式: {input_path}")
        sys.exit(1)
    
    # 获取模型实例
    try:
        model_instance = get_model_class(args.model)
    except ValueError as e:
        logging.info(f"❌ 错误：{e}")
        sys.exit(1)
    nomodelpath = False
    # 设置默认模型路径
    if not args.modelpath:
        nomodelpath = True
        if args.model == 'opus':
            args.modelpath = './models/models--Helsinki-NLP--opus-mt-en-zh/snapshots/408d9bc410a388e1d9aef112a2daba955b945255'
        else:  # nllb
            args.modelpath = './models/models--facebook--nllb-200-distilled-600M/snapshots/f8d333a098d19b4fd9a8b18f94170487ad3f821d' 
    
    # 设置输出文件路径
    if args.output:
        output_path = Path(args.output)
    else:
        suffix = f"_{args.model}_translated.zh-CN"
        output_path = get_output_filename(input_path, suffix)
    
    logging.info("🎯 JuSubTitleAutoTranslate - 字幕翻译工具")
    logging.info(f"📁 输入文件: {input_path}")
    logging.info(f"📁 输出文件: {output_path}")
    logging.info(f"🤖 模型: {model_instance.name}")
    logging.info(f"📂 模型路径: {args.modelpath}")
    logging.info(f"⬇️  自动下载: {'是' if args.auto_download else '否'}")
    argmodelpath = Path(args.modelpath)
    if args.auto_download:
        if nomodelpath:
            argmodelpath = './models/'
        logging.info(f"📁 下载目录: {argmodelpath}")
    
    if args.model == 'nllb':
        logging.info(f"🌐 源语言: {args.source_lang}")
        logging.info(f"🌐 目标语言: {args.target_lang}")
    
    try:
        # 加载模型
        tokenizer, model = load_model(args.model, argmodelpath, args.auto_download)
        
        logging.info("📖 正在解析SRT文件...")
        subtitles = parse_srt_file(input_path)
        logging.info(f"✅ 解析完成，共找到 {len(subtitles)} 条字幕")
        
        # 翻译字幕
        if args.model == 'opus':
            translated_count, elapsed_time = translate_subtitles(
                subtitles, model_instance, tokenizer, model, 
                max_length=args.max_length
            )
        else:  # nllb
            translated_count, elapsed_time = translate_subtitles(
                subtitles, model_instance, tokenizer, model,
                source_lang=args.source_lang,
                target_lang=args.target_lang,
                max_length=args.max_length
            )
        
        logging.info("💾 正在保存翻译后的文件...")
        write_srt_file(subtitles, output_path)
        logging.info(f"✅ 文件保存成功: {output_path}")
        
        logging.info(f"🎉 翻译完成！输出文件: {output_path}")
        logging.info("📊 统计信息:")
        logging.info(f"   - 总字幕行数: {len(subtitles)}")
        logging.info(f"   - 翻译成功行数: {translated_count}")
        logging.info(f"   - 总耗时: {elapsed_time:.2f} 秒")
        logging.info(f"   - 平均速度: {len(subtitles)/elapsed_time:.2f} 条/秒")
    except Exception as e:
        logging.info(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Starting JuSubTitleAutoTranslate...")
    main()
