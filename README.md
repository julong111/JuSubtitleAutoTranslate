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

![微信赞赏]:data:image/jpeg;base64,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AKKKKACiiigAooooAKKKKACiiigApKWigAooooASkIyCPw4p1FAHw54rs75PFupW93FJ9ra7kypU5Ylz09ua+uPhdoDeGfAul6bMnlzpF5ky9w7fM36k10MmnWUlyLmSzt2nHSVolLD8cZqzzQAtFFFADT1618N+MLk3XirVbgjBku5Wx6fOa+45VLIwBwSOCOMGvjXxB4C8SWviq500aTeTyvOwjdYiVkBPDbhxjv2oA+lPgdb/AGb4XaGMg+ZC0nHu5NdxWP4P0k6J4V0zTJABJa20cT46bgoB/WtkUAFNbocdf604UhGeKAPh7xqJV8Za0sz+ZIL2YFvX5zX1Z8Fr17/4ZaLNKSXWExZY5ztYgfoK8D+MHgnWrL4galNa6bc3FrfzGeKSCEspDcleO4PUV738GdEvfD/w906w1JWjucPI0bHmLc2QuPxzQB21FH0ooAK+Ufj7f62vxGvY7qa4it4tv2QK5CBNo5XHvnPvX1dVW6srW7dWubWCZkOVMkYbH0JFMDmfhBPqdx8PtJl1syG8MWC0pJcrk7S2eemK7CkUBVAAwAMUtIAooooAKKKKYC0UlLSAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBB0paQdKWgD//W9/HSigdKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAEpaKKACiiigBKKKKACiiigAooooAKKKKACiiigAooooAWikooAWikooAWikooAWikooAWikooAWikooAWikooAWikooAB0paQdKWgD/9f3okg4HapB0FRt941Iv3RQAuKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAGKMUUUAUriV0mZVYgCo/Pl/vmlu/+Phvw/lUVAH//2Q==

****
## 📄 许可证

MIT License
