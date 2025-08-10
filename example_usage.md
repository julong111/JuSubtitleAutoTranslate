# JuSubTrans 使用示例

## 🚀 基本用法

### 1. 使用OPUS-MT模型（推荐用于日常翻译）

```bash
# 基本用法
python trans.py movie.srt --model opus

# 指定输出文件
python trans.py movie.srt --model opus -o movie_opus_translated.srt

# 使用本地模型
python trans.py movie.srt --model opus -m /path/to/local/opus-model
```

### 2. 使用NLLB模型（推荐用于高质量翻译）

```bash
# 基本用法（首次使用会自动下载模型）
python trans.py movie.srt --model nllb

# 指定输出文件
python trans.py movie.srt --model nllb -o movie_nllb_translated.srt

# 自动下载模型
python trans.py movie.srt --model nllb --auto-download
```

## 🔧 高级用法

### 3. 自定义语言设置（仅NLLB模型）

```bash
# 英文到简体中文（默认）
python trans.py movie.srt --model nllb --source-lang eng_Latn --target-lang zho_Hans

# 英文到繁体中文
python trans.py movie.srt --model nllb --source-lang eng_Latn --target-lang zho_Hant

# 法文到中文
python trans.py movie.srt --model nllb --source-lang fra_Latn --target-lang zho_Hans
```

### 4. 性能优化

```bash
# 调整最大输入长度（提高翻译质量）
python trans.py movie.srt --model nllb --max-length 1024

# 使用OPUS-MT快速翻译
python trans.py movie.srt --model opus --max-length 256
```

## 📁 实际使用场景

### 场景1：快速翻译英文字幕
```bash
# 使用OPUS-MT快速翻译
python trans.py english_movie.srt --model opus
# 输出：english_movie_opus_translated.srt
```

### 场景2：高质量翻译重要内容
```bash
# 使用NLLB高质量翻译
python trans.py important_document.srt --model nllb --auto-download
# 输出：important_document_nllb_translated.srt
```

### 场景3：批量处理多个文件
```bash
# 批量翻译多个SRT文件
for file in *.srt; do
    python trans.py "$file" --model opus
done
```

## 🎯 模型选择建议

| 使用场景 | 推荐模型 | 原因 |
|----------|----------|------|
| 日常观看 | OPUS-MT | 速度快，质量够用 |
| 学习研究 | NLLB | 质量高，理解准确 |
| 实时翻译 | OPUS-MT | 响应快，延迟低 |
| 正式场合 | NLLB | 质量高，专业性强 |
| 资源受限 | OPUS-MT | 内存占用少 |

## 🚨 注意事项

1. **首次使用NLLB模型**需要下载约1.2GB模型文件
2. **OPUS-MT模型**建议使用本地模型以提高速度
3. **内存要求**：NLLB > OPUS-MT
4. **网络要求**：自动下载模式需要稳定网络

## 🔍 故障排除

### 模型加载失败
```bash
# 检查模型路径
python trans.py movie.srt --model opus -m /correct/model/path

# 使用自动下载
python trans.py movie.srt --model nllb --auto-download
```

### 内存不足
```bash
# 使用OPUS-MT模型（内存占用少）
python trans.py movie.srt --model opus

# 重启程序释放内存
```

### 翻译质量不佳
```bash
# 切换到NLLB模型
python trans.py movie.srt --model nllb

# 调整max-length参数
python trans.py movie.srt --model nllb --max-length 1024
```

## 📊 性能对比示例

```bash
# 测试OPUS-MT速度
time python trans.py sample.srt --model opus
# 典型结果：100条字幕，耗时约30秒

# 测试NLLB质量
time python trans.py sample.srt --model nllb
# 典型结果：100条字幕，耗时约120秒，质量更高
```

## 🎉 成功案例

使用JuSubTrans成功翻译了：
- 电影字幕：从英文到中文
- 教学视频：从英文到中文
- 纪录片：从英文到中文
- 技术讲座：从英文到中文

翻译质量得到用户一致好评，特别是NLLB模型在专业术语翻译方面表现优异！
