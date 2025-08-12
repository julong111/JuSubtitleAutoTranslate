# JuSubtitleAutoTranslate

SRT字幕文件AI自动翻译脚本


一个支持多种AI翻译模型的SRT字幕文件自动翻译工具，支持OPUS-MT（速度快）和NLLB（质量高）两种模型。

## 📋 功能特性

- 🎯 **统一接口**: 一个脚本支持多种翻译模型
- 🚀 **OPUS-MT**: 速度快，质量一般，适合实时翻译
- 🎨 **NLLB**: 质量高，速度慢，适合高质量翻译
- 📁 **智能命名**: 自动生成带模型标识的输出文件名
- ⏱️ **性能统计**: 显示翻译速度和耗时
- 🔧 **灵活配置**: 支持自定义模型路径和参数

## 📁 实际使用场景
- 快速翻译英文字幕
- 批量处理多个字幕文件(待开发)
- 翻译其他文本格式（待开发）

---

## 📊 性能对比

| 模型    | 速度   | 质量   | 内存占用 | 适用场景   |
|---------|--------|--------|----------|------------|
| OPUS-MT | ⚡⚡⚡   | ⭐⭐    | 💾💾     | 速度快     |
| NLLB    | ⚡     | ⭐⭐⭐⭐⭐ | 💾💾💾   | 高质量翻译 |

---

## 🚨 注意事项
网络不好自动下载会断线。  建议手工下载模型至本地。
1. **NLLB模型**  约3.2GB   https://huggingface.co/facebook/nllb-200-distilled-600M
2. **OPUS-MT模型**  约1.3GB  https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
3. **内存要求**: OPUS-MT模型需要较少内存，速度快。  NLLB模型需要更多内存，速度慢。
4. **网络要求**: 自动下载模式需要稳定的网络连接


## 🚀 快速开始

### 🛠️ 初始化并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
退出venv命令 deactivate

### 模型位置与下载方式

1. **手工指定模型路径**  
   ```bash
   python3 translate.py input.srt -m opus --modelpath /user/path 
   ```
2. **手工下载并建立软链接**  
   国内自动下载模型网速不好的情况下，先手动下载翻译模型到本地，然后手动建立软链接：
   ```bash
   ln -s /user/opus-mt-en-zh ./models/opus-mt-en-zh
   python3 translate.py input.srt -m opus
   ```
3. **全自动下载模型**（适合网速快）  
   ```bash
   python3 translate.py input.srt
   ```



## 📖 详细用法
```bash
python translate.py [选项]

选项:
  -i, --input             输入字幕文件路径
  -o, --output            输出字幕文件路径
  -m                      选择翻译模型  opus,nllb [默认: opus]
  --modelpath            模型路径（可选/可自动下载）
  --auto-download         自动下载模型标志,默认False
  --source-lang           源语言代码（仅NLLB有效）
  --target-lang           目标语言代码（仅NLLB有效）
  --max-length            最大输入长度 [默认: 512]
```

```bash
# 基本用法
python translate.py -i input.srt --modelpath /user/opus-modelpath

# 使用OPUS-MT模型（速度快，质量一般）
python translate.py -i input.srt -m opus

# 使用NLLB模型（质量高，速度慢）
python translate.py -i input.srt -m nllb

# 指定输出文件
python translate.py -i input.srt -o output.srt

# 自动下载模型
python translate.py -i input.srt -m nllb --auto-download
 
# 自动下载模型至指定路径
python translate.py -i input.srt -m nllb --auto-download --modelpath /user/opus-modelpath

# 自定义输出和参数
python translate.py -i input.srt -o translated.srt -m nllb --modelpath /user/opus-modelpath --source_lang eng_Latn --target_lang zho_Hans --max-length 1024

# 查看帮助
python translate.py --help
```

## 🔧 模型默认配置

### OPUS-MT模型
- **默认路径**: `/models/models--Helsinki-NLP--opus-mt-en-zh/snapshots/408d9bc410a388e1d9aef112a2daba955b945255`
- **特点**: 速度快，质量一般，适合日常使用
- **支持语言**: 英文 → 中文   不支持语言参数 单向 英文转中文（后续优化）

### NLLB模型
- **默认路径**: `/models/models--facebook--nllb-200-distilled-600M/snapshots/f8d333a098d19b4fd9a8b18f94170487ad3f821d`
- **特点**: 质量高，速度慢，适合高质量要求
- **支持语言**: 多语言支持，默认英文→中文 
      语言参数代码见下表  
         source_lang 默认：eng_Latn 英文  
         target_lang 默认：zho_Hans 简体中文


## NLLB 支持的语言代码列表

以下为 NLLB 支持的全部语言代码 

```

*eng_Latn,    英语, 英国/美国/全球*

*zho_Hans,    中文（简体）, 中国大陆/新加坡*
*zho_Hant,    中文（繁体）, 台湾/香港/澳门*
*yue_Hant,    粤语（繁体）, 香港/广东*
*bod_Tibt,    藏语, 中国/印度/尼泊尔*
*uig_Arab,    维吾尔语, 中国*

*kor_Hang,    韩语, 韩国*
*jpn_Jpan,    日语, 日本*

ace_Arab,    亚齐语（阿拉伯字母）, 印度尼西亚
ace_Latn,    亚齐语（拉丁字母）, 印度尼西亚
acm_Arab,    伊拉克阿拉伯语, 伊拉克
acq_Arab,    阿拉伯语（也门）, 也门
aeb_Arab,    突尼斯阿拉伯语, 突尼斯
afr_Latn,    南非荷兰语, 南非/纳米比亚
ajp_Arab,    南黎凡特阿拉伯语, 叙利亚
aka_Latn,    阿坎语, 加纳
amh_Ethi,    阿姆哈拉语, 埃塞俄比亚
apc_Arab,    北黎凡特阿拉伯语, 黎巴嫩/叙利亚
arb_Arab,    标准阿拉伯语, 阿拉伯国家
ars_Arab,    纳吉迪阿拉伯语, 沙特阿拉伯
ary_Arab,    摩洛哥阿拉伯语, 摩洛哥
arz_Arab,    埃及阿拉伯语, 埃及
asm_Beng,    阿萨姆语, 印度
ast_Latn,    阿斯图里亚斯语, 西班牙
awa_Deva,    阿瓦迪语, 印度
ayr_Latn,    南艾马拉语, 玻利维亚/秘鲁
azb_Arab,    南阿塞拜疆土耳其语, 伊朗
azj_Latn,    北阿塞拜疆土耳其语, 阿塞拜疆
bak_Cyrl,    巴什基尔语, 俄罗斯
bam_Latn,    班巴拉语, 马里
ban_Latn,    巴厘语, 印度尼西亚
bel_Cyrl,    白俄罗斯语, 白俄罗斯
bem_Latn,    本巴语, 赞比亚
ben_Beng,    孟加拉语, 孟加拉国/印度
bho_Deva,    博杰普尔语, 印度/尼泊尔
bjn_Arab,    班贾尔语（阿拉伯字母）, 印度尼西亚
bjn_Latn,    班贾尔语（拉丁字母）, 印度尼西亚
bos_Latn,    波斯尼亚语, 波斯尼亚和黑塞哥维那
bug_Latn,    布吉语, 印度尼西亚
bul_Cyrl,    保加利亚语, 保加利亚
cat_Latn,    加泰罗尼亚语, 西班牙
ceb_Latn,    宿务语, 菲律宾
ces_Latn,    捷克语, 捷克
cjk_Latn,    查姆语, 越南/柬埔寨
ckb_Arab,    库尔德语（索拉尼）, 伊拉克/伊朗
crh_Latn,    克里米亚鞑靼语, 乌克兰
cym_Latn,    威尔士语, 英国
dan_Latn,    丹麦语, 丹麦
deu_Latn,    德语, 德国/奥地利/瑞士
dik_Latn,    丁卡语, 南苏丹
dyu_Latn,    迪乌拉语, 布基纳法索/科特迪瓦
dzo_Tibt,    宗卡语, 不丹
ell_Grek,    希腊语, 希腊
epo_Latn,    世界语, 国际
est_Latn,    爱沙尼亚语, 爱沙尼亚
eus_Latn,    巴斯克语, 西班牙/法国
ewe_Latn,    埃维语, 多哥/加纳
fao_Latn,    法罗语, 法罗群岛
pes_Arab,    伊朗波斯语, 伊朗
fij_Latn,    斐济语, 斐济
fin_Latn,    芬兰语, 芬兰
fon_Latn,    丰语, 贝宁
fra_Latn,    法语, 法国/比利时/加拿大
fur_Latn,    弗留利语, 意大利
fuv_Latn,    富拉尼语, 尼日利亚/西非
gla_Latn,    苏格兰盖尔语, 英国
gle_Latn,    爱尔兰语, 爱尔兰
glg_Latn,    加利西亚语, 西班牙
grn_Latn,    瓜拉尼语, 巴拉圭
guj_Gujr,    古吉拉特语, 印度
hat_Latn,    海地克里奥尔语, 海地
hau_Latn,    豪萨语, 尼日利亚
heb_Hebr,    希伯来语, 以色列
hin_Deva,    印地语, 印度
hne_Deva,    查蒂斯加尔语, 印度
hrv_Latn,    克罗地亚语, 克罗地亚
hun_Latn,    匈牙利语, 匈牙利
hye_Armn,    亚美尼亚语, 亚美尼亚
ibo_Latn,    伊博语, 尼日利亚
ilo_Latn,    伊洛卡诺语, 菲律宾
ind_Latn,    印度尼西亚语, 印度尼西亚
isl_Latn,    冰岛语, 冰岛
ita_Latn,    意大利语, 意大利
jav_Latn,    爪哇语, 印度尼西亚
kab_Latn,    卡拜尔语, 阿尔及利亚
kac_Latn,    卡钦语, 缅甸
kam_Latn,    卡姆巴语, 肯尼亚
kan_Knda,    卡纳达语, 印度
kas_Arab,    克什米尔语（阿拉伯字母）, 印度/巴基斯坦
kas_Deva,    克什米尔语（天城文）, 印度
kat_Geor,    格鲁吉亚语, 格鲁吉亚
knc_Arab,    卡努里语（阿拉伯字母）, 尼日利亚
knc_Latn,    卡努里语（拉丁字母）, 尼日利亚
kaz_Cyrl,    哈萨克语, 哈萨克斯坦
kbp_Latn,    卡比耶语, 多哥
kea_Latn,    佛得角克里奥尔语, 佛得角
khm_Khmr,    高棉语, 柬埔寨
kik_Latn,    基库尤语, 肯尼亚
kin_Latn,    卢旺达语, 卢旺达
kir_Cyrl,    吉尔吉斯语, 吉尔吉斯斯坦
kmb_Latn,    金邦杜语, 安哥拉
kon_Latn,    刚果语, 刚果
kmr_Latn,    库尔德语（库尔曼吉）, 土耳其/叙利亚/伊拉克
lao_Laoo,    老挝语, 老挝
lvs_Latn,    拉脱维亚语, 拉脱维亚
lij_Latn,    利古里亚语, 意大利
lim_Latn,    林堡语, 荷兰/比利时
lin_Latn,    林加拉语, 刚果
lit_Latn,    立陶宛语, 立陶宛
lmo_Latn,    伦巴第语, 意大利
ltg_Latn,    拉脱加莱语, 拉脱维亚
ltz_Latn,    卢森堡语, 卢森堡
lua_Latn,    卢巴-卢卢亚语, 刚果
lug_Latn,    卢干达语, 乌干达
luo_Latn,    卢奥语, 肯尼亚/坦桑尼亚
lus_Latn,    卢晒语, 印度
mag_Deva,    马加伊语, 印度
mai_Deva,    迈蒂利语, 印度/尼泊尔
mal_Mlym,    马拉雅拉姆语, 印度
mar_Deva,    马拉地语, 印度
min_Latn,    米南卡保语, 印度尼西亚
mkd_Cyrl,    马其顿语, 北马其顿
plt_Latn,    毛里求斯克里奥尔语, 毛里求斯
mlt_Latn,    马耳他语, 马耳他
mni_Beng,    曼尼普尔语, 印度
khk_Cyrl,    哈卡斯语, 俄罗斯
mos_Latn,    莫西语, 布基纳法索
mri_Latn,    毛利语, 新西兰
zsm_Latn,    马来语, 马来西亚
mya_Mymr,    缅甸语, 缅甸
nld_Latn,    荷兰语, 荷兰/比利时
nno_Latn,    挪威尼诺斯克语, 挪威
nob_Latn,    挪威博克马尔语, 挪威
npi_Deva,    尼泊尔语, 尼泊尔
nso_Latn,    北索托语, 南非
nus_Latn,    努埃尔语, 南苏丹
nya_Latn,    齐切瓦语, 马拉维/赞比亚
oci_Latn,    奥克西唐语, 法国
gaz_Latn,    奥罗莫语, 埃塞俄比亚/肯尼亚
ory_Orya,    奥里亚语, 印度
pag_Latn,    潘加西南语, 菲律宾
pan_Guru,    旁遮普语, 印度/巴基斯坦
pap_Latn,    帕皮阿门托语, 阿鲁巴/库拉索
pol_Latn,    波兰语, 波兰
por_Latn,    葡萄牙语, 葡萄牙/巴西
prs_Arab,    达里语, 阿富汗
pbt_Arab,    巴基斯坦普什图语, 巴基斯坦
quy_Latn,    南克丘亚语, 秘鲁
ron_Latn,    罗马尼亚语, 罗马尼亚
run_Latn,    卢旺达语, 布隆迪
rus_Cyrl,    俄语, 俄罗斯
sag_Latn,    桑戈语, 中非
san_Deva,    梵语, 印度
sat_Beng,    桑塔利语, 印度
scn_Latn,    西西里语, 意大利
shn_Mymr,    掸语, 缅甸
sin_Sinh,    僧伽罗语, 斯里兰卡
slk_Latn,    斯洛伐克语, 斯洛伐克
slv_Latn,    斯洛文尼亚语, 斯洛文尼亚
smo_Latn,    萨摩亚语, 萨摩亚
sna_Latn,    修纳语, 津巴布韦
snd_Arab,    信德语, 巴基斯坦
som_Latn,    索马里语, 索马里
sot_Latn,    南索托语, 南非/莱索托
spa_Latn,    西班牙语, 西班牙/拉美
als_Latn,    阿尔萨斯语, 法国
srd_Latn,    撒丁语, 意大利
srp_Cyrl,    塞尔维亚语, 塞尔维亚
ssw_Latn,    斯瓦蒂语, 斯威士兰/南非
sun_Latn,    巽他语, 印度尼西亚
swe_Latn,    瑞典语, 瑞典
swh_Latn,    斯瓦希里语, 东非
szl_Latn,    西里西亚语, 波兰
tam_Taml,    泰米尔语, 印度/斯里兰卡
tat_Cyrl,    鞑靼语, 俄罗斯
tel_Telu,    泰卢固语, 印度
tgk_Cyrl,    塔吉克语, 塔吉克斯坦
tgl_Latn,    塔加洛语, 菲律宾
tha_Thai,    泰语, 泰国
tir_Ethi,    提格利尼亚语, 厄立特里亚/埃塞俄比亚
taq_Latn,    塔马奇克语（拉丁字母）, 马里/尼日尔
taq_Tfng,    塔马奇克语（提非纳字母）, 马里/尼日尔
tpi_Latn,    托克皮辛语, 巴布亚新几内亚
tsn_Latn,    茨瓦纳语, 博茨瓦纳/南非
tso_Latn,    宗加语, 南非/津巴布韦
tuk_Latn,    土库曼语, 土库曼斯坦
tum_Latn,    通布卡语, 马拉维
tur_Latn,    土耳其语, 土耳其
twi_Latn,    契维语, 加纳
tzm_Tfng,    中阿特拉斯塔马齐格特语, 摩洛哥
ukr_Cyrl,    乌克兰语, 乌克兰
umb_Latn,    姆本杜语, 安哥拉
urd_Arab,    乌尔都语, 巴基斯坦/印度
uzn_Latn,    乌兹别克语, 乌兹别克斯坦
vec_Latn,    威尼斯语, 意大利
vie_Latn,    越南语, 越南
war_Latn,    瓦赖语, 菲律宾
wol_Latn,    沃洛夫语, 塞内加尔
xho_Latn,    科萨语, 南非
ydd_Hebr,    意第绪语, 东欧/以色列
yor_Latn,    约鲁巴语, 尼日利亚
zul_Latn,    祖鲁语, 南非
```

## 🆘 常见问题
---
### 模型加载失败
```bash
# 重新尝试自动下载模式
python translate.py -i input.srt --auto-download
```

### 内存不足
- 尝试使用OPUS-MT模型

### 翻译质量不佳
- 尝试使用NLLB模型
- 调整max-length参数
- 检查输入文本格式

## 📝 更新日志

- **v1.0**: 新增翻译脚本 `translate.py`

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 联系我
   julong[at]111.com

### 打赏支持 👍

如果我的项目帮到你的话就 **"打赏"** 一下吧~🎉✨

![微信赞赏](微信赞赏码.jpg)

****
## 📄 许可证

MIT License
