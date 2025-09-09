[中文](README.md)| [English](#)

# JuSubtitleAutoTranslate

AI Automatic File Translation Script

An automatic translation tool for SRT subtitle files that supports multiple AI translation models.
Supports two machine translation models: **Helsinki-NLP/opus-mt-en-zh** and **facebook/nllb**.

## 📋 Features

- 🎯 **Unified Interface**: One script supports multiple translation models
- 🚀 **OPUS-MT**: Fast, average quality, suitable for real-time translation
- 🎨 **NLLB**: High quality, slow speed, suitable for high-quality translation
- 📁 **Smart Naming**: Automatically generates output filenames with model identifiers
- ⏱️ **Performance Statistics**: Displays translation speed and time taken
- 🔧 **Flexible Configuration**: Supports custom model paths and parameters

## 📁 Use Cases
- Quickly translate English subtitles
- Batch process multiple subtitle files
- Translate other text formats like srt, txt, md

---

## 📊 Performance Comparison

| Model    | Speed   | Quality   | Memory Usage | Use Case   |
|---------|--------|--------|----------|------------|
| OPUS-MT | ⚡⚡⚡   | ⭐⭐    | 💾💾     | Fast     |
| NLLB    | ⚡     | ⭐⭐⭐⭐⭐ | 💾💾💾   | High-quality translation |

---

## 🚨 Important Notes
Auto-download may fail with a poor network connection. It is recommended to download the models manually.
1. **NLLB Model** approx. 3.2GB   https://huggingface.co/facebook/nllb-200-distilled-600M
2. **OPUS-MT Model** approx. 1.3GB  https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
3. **Memory Requirements**: The OPUS-MT model requires less memory and is faster. The NLLB model requires more memory and is slower.
4. **Network Requirements**: A stable network connection is required for auto-download mode.


## 🚀 Quick Start

### 🛠️ Initialize and Install Dependencies

This project uses uv for management. Please install the uv tool first.
```bash
uv init
uv run translate.py -i sample-eng.srt -m opus --model_path /user/path 
or
python3 translate.py -i sample-eng.srt -m opus --model_path /user/path
```
To exit the venv, use the command: deactivate

### Model Location and Download Methods

1. **Manually Specify Model Path**  
   ```bash
   python3 translate.py -i sample-eng.srt -m opus --model_path /user/path 
   ```
2. **Manual Download and Create Symlink**  
   If you have a slow network connection for auto-downloading in your region, first download the translation model manually, then create a symbolic link:
   ```bash
   ln -s /user/opus-mt-en-zh ./models/opus-mt-en-zh
   python3 translate.py -i sample-eng.srt -m opus
   ```
3. **Fully Automatic Download** (for fast network speeds)  
   ```bash
   python3 translate.py -i sample-eng.srt
   ```



## 📖 Detailed Usage
```bash
python translate.py [options]

Options:
  -i, --input_file        Input SRT file path (single file mode)
  -di, --input_dir        Input SRT folder path (batch mode)
  -o, --output            Output file path (optional, for single file mode only)
  -do, --output_dir       Output folder path (optional, for batch mode only)
  -m, --model             Choose translation model: opus(fast) or nllb(high quality) [Default: opus]
  --model_path            Model path (optional, uses default path if not provided)
  --auto-download         If the local model does not exist, automatically download it from Hugging Face (default: False)
  --source_lang           Source language code (NLLB model only, default: eng_Latn English)
  --target_lang           Target language code (NLLB model only, default: zho_Hans Simplified Chinese)
  --max_length            Maximum input length [Default: 512]
```

```bash
# Basic Usage (single file)
python translate.py -i input.srt --model_path /user/opus-modelpath

# Batch Processing
python translate.py -di /inputdir -do /outputdir --model_path /user/opus-modelpath

# Use OPUS-MT model (fast, average quality)
python translate.py -i input.srt -m opus

# Use NLLB model (high quality, slow)
python translate.py -i input.srt -m nllb

# Specify output file
python translate.py -i input.srt -o output.srt

# Auto-download model
python translate.py -i input.srt -m nllb --auto-download
 
# Auto-download model to a specific path
python translate.py -i input.srt -m nllb --auto-download --model_path /user/opus-modelpath

# Custom output and parameters
python translate.py -i input.srt -o translated.srt -m nllb --model_path /user/opus-modelpath --source_lang eng_Latn --target_lang zho_Hans --max_length 1024

# View help
python translate.py --help
```

## 🔧 Default Model Configuration

### OPUS-MT Model
- **Default Path**: `/models/models--Helsinki-NLP--opus-mt-en-zh/snapshots/408d9bc410a388e1d9aef112a2daba955b945255`
- **Features**: Fast, average quality, suitable for daily use
- **Supported Languages**: English → Chinese. Language parameters are not supported (unidirectional English to Chinese, to be optimized later).

### NLLB Model
- **Default Path**: `/models/models--facebook--nllb-200-distilled-600M/snapshots/f8d333a098d19b4fd9a8b18f94170487ad3f821d`
- **Features**: High quality, slow speed, suitable for high-quality requirements
- **Supported Languages**: Multi-language support, default is English → Chinese. See the table below for language codes. 
         `source_lang` default: `eng_Latn` (English)  
         `target_lang` default: `zho_Hans` (Simplified Chinese)


## NLLB Supported Language Codes

The following is a complete list of language codes supported by NLLB.

```

*eng_Latn,    English, UK/USA/Global*

*zho_Hans,    Chinese (Simplified), Mainland China/Singapore*
*zho_Hant,    Chinese (Traditional), Taiwan/Hong Kong/Macau*
*yue_Hant,    Cantonese (Traditional), Hong Kong/Guangdong*
*bod_Tibt,    Tibetan, China/India/Nepal*
*uig_Arab,    Uyghur, China*

*kor_Hang,    Korean, South Korea*
*jpn_Jpan,    Japanese, Japan*

ace_Arab,    Acehnese (Arabic script), Indonesia
ace_Latn,    Acehnese (Latin script), Indonesia
acm_Arab,    Iraqi Arabic, Iraq
acq_Arab,    Ta'izzi-Adeni Arabic, Yemen
aeb_Arab,    Tunisian Arabic, Tunisia
afr_Latn,    Afrikaans, South Africa/Namibia
ajp_Arab,    South Levantine Arabic, Syria
aka_Latn,    Akan, Ghana
amh_Ethi,    Amharic, Ethiopia
apc_Arab,    North Levantine Arabic, Lebanon/Syria
arb_Arab,    Modern Standard Arabic, Arab countries
ars_Arab,    Najdi Arabic, Saudi Arabia
ary_Arab,    Moroccan Arabic, Morocco
arz_Arab,    Egyptian Arabic, Egypt
asm_Beng,    Assamese, India
ast_Latn,    Asturian, Spain
awa_Deva,    Awadhi, India
ayr_Latn,    Central Aymara, Bolivia/Peru
azb_Arab,    South Azerbaijani, Iran
azj_Latn,    North Azerbaijani, Azerbaijan
bak_Cyrl,    Bashkir, Russia
bam_Latn,    Bambara, Mali
ban_Latn,    Balinese, Indonesia
bel_Cyrl,    Belarusian, Belarus
bem_Latn,    Bemba, Zambia
ben_Beng,    Bengali, Bangladesh/India
bho_Deva,    Bhojpuri, India/Nepal
bjn_Arab,    Banjar (Arabic script), Indonesia
bjn_Latn,    Banjar (Latin script), Indonesia
bos_Latn,    Bosnian, Bosnia and Herzegovina
bug_Latn,    Buginese, Indonesia
bul_Cyrl,    Bulgarian, Bulgaria
cat_Latn,    Catalan, Spain
ceb_Latn,    Cebuano, Philippines
ces_Latn,    Czech, Czechia
cjk_Latn,    Chokwe, Angola/Congo
ckb_Arab,    Central Kurdish, Iraq/Iran
crh_Latn,    Crimean Tatar, Ukraine
cym_Latn,    Welsh, UK
dan_Latn,    Danish, Denmark
deu_Latn,    German, Germany/Austria/Switzerland
dik_Latn,    Dinka, South Sudan
dyu_Latn,    Dyula, Burkina Faso/Côte d'Ivoire
dzo_Tibt,    Dzongkha, Bhutan
ell_Grek,    Greek, Greece
epo_Latn,    Esperanto, International
est_Latn,    Estonian, Estonia
eus_Latn,    Basque, Spain/France
ewe_Latn,    Ewe, Togo/Ghana
fao_Latn,    Faroese, Faroe Islands
pes_Arab,    Western Farsi, Iran
fij_Latn,    Fijian, Fiji
fin_Latn,    Finnish, Finland
fon_Latn,    Fon, Benin
fra_Latn,    French, France/Belgium/Canada
fur_Latn,    Friulian, Italy
fuv_Latn,    Nigerian Fulfulde, Nigeria/West Africa
gla_Latn,    Scottish Gaelic, UK
gle_Latn,    Irish, Ireland
glg_Latn,    Galician, Spain
grn_Latn,    Guarani, Paraguay
guj_Gujr,    Gujarati, India
hat_Latn,    Haitian Creole, Haiti
hau_Latn,    Hausa, Nigeria
heb_Hebr,    Hebrew, Israel
hin_Deva,    Hindi, India
hne_Deva,    Chhattisgarhi, India
hrv_Latn,    Croatian, Croatia
hun_Latn,    Hungarian, Hungary
hye_Armn,    Armenian, Armenia
ibo_Latn,    Igbo, Nigeria
ilo_Latn,    Ilocano, Philippines
ind_Latn,    Indonesian, Indonesia
isl_Latn,    Icelandic, Iceland
ita_Latn,    Italian, Italy
jav_Latn,    Javanese, Indonesia
kab_Latn,    Kabyle, Algeria
kac_Latn,    Jingpho, Myanmar
kam_Latn,    Kamba, Kenya
kan_Knda,    Kannada, India
kas_Arab,    Kashmiri (Arabic script), India/Pakistan
kas_Deva,    Kashmiri (Devanagari script), India
kat_Geor,    Georgian, Georgia
knc_Arab,    Central Kanuri (Arabic script), Nigeria
knc_Latn,    Central Kanuri (Latin script), Nigeria
kaz_Cyrl,    Kazakh, Kazakhstan
kbp_Latn,    Kabiye, Togo
kea_Latn,    Kabuverdianu, Cabo Verde
khm_Khmr,    Khmer, Cambodia
kik_Latn,    Kikuyu, Kenya
kin_Latn,    Kinyarwanda, Rwanda
kir_Cyrl,    Kyrgyz, Kyrgyzstan
kmb_Latn,    Kimbundu, Angola
kon_Latn,    Kongo, Congo
kmr_Latn,    Northern Kurdish, Turkey/Syria/Iraq
lao_Laoo,    Lao, Laos
lvs_Latn,    Standard Latvian, Latvia
lij_Latn,    Ligurian, Italy
lim_Latn,    Limburgish, Netherlands/Belgium
lin_Latn,    Lingala, Congo
lit_Latn,    Lithuanian, Lithuania
lmo_Latn,    Lombard, Italy
ltg_Latn,    Latgalian, Latvia
ltz_Latn,    Luxembourgish, Luxembourg
lua_Latn,    Luba-Kasai, Congo
lug_Latn,    Ganda, Uganda
luo_Latn,    Luo, Kenya/Tanzania
lus_Latn,    Mizo, India
mag_Deva,    Magahi, India
mai_Deva,    Maithili, India/Nepal
mal_Mlym,    Malayalam, India
mar_Deva,    Marathi, India
min_Latn,    Minangkabau, Indonesia
mkd_Cyrl,    Macedonian, North Macedonia
plt_Latn,    Plateau Malagasy, Madagascar
mlt_Latn,    Maltese, Malta
mni_Beng,    Meitei, India
khk_Cyrl,    Halh Mongolian, Mongolia
mos_Latn,    Mossi, Burkina Faso
mri_Latn,    Māori, New Zealand
zsm_Latn,    Standard Malay, Malaysia
mya_Mymr,    Burmese, Myanmar
nld_Latn,    Dutch, Netherlands/Belgium
nno_Latn,    Norwegian Nynorsk, Norway
nob_Latn,    Norwegian Bokmål, Norway
npi_Deva,    Nepali, Nepal
nso_Latn,    Northern Sotho, South Africa
nus_Latn,    Nuer, South Sudan
nya_Latn,    Nyanja, Malawi/Zambia
oci_Latn,    Occitan, France
gaz_Latn,    West Central Oromo, Ethiopia/Kenya
ory_Orya,    Odia, India
pag_Latn,    Pangasinan, Philippines
pan_Guru,    Eastern Panjabi, India/Pakistan
pap_Latn,    Papiamento, Aruba/Curaçao
pol_Latn,    Polish, Poland
por_Latn,    Portuguese, Portugal/Brazil
prs_Arab,    Dari, Afghanistan
pbt_Arab,    Southern Pashto, Pakistan
quy_Latn,    Ayacucho Quechua, Peru
ron_Latn,    Romanian, Romania
run_Latn,    Rundi, Burundi
rus_Cyrl,    Russian, Russia
sag_Latn,    Sango, Central African Republic
san_Deva,    Sanskrit, India
sat_Beng,    Santali, India
scn_Latn,    Sicilian, Italy
shn_Mymr,    Shan, Myanmar
sin_Sinh,    Sinhala, Sri Lanka
slk_Latn,    Slovak, Slovakia
slv_Latn,    Slovenian, Slovenia
smo_Latn,    Samoan, Samoa
sna_Latn,    Shona, Zimbabwe
snd_Arab,    Sindhi, Pakistan
som_Latn,    Somali, Somalia
sot_Latn,    Southern Sotho, South Africa/Lesotho
spa_Latn,    Spanish, Spain/Latin America
als_Latn,    Tosk Albanian, Albania
srd_Latn,    Sardinian, Italy
srp_Cyrl,    Serbian, Serbia
ssw_Latn,    Swati, Eswatini/South Africa
sun_Latn,    Sundanese, Indonesia
swe_Latn,    Swedish, Sweden
swh_Latn,    Swahili, East Africa
szl_Latn,    Silesian, Poland
tam_Taml,    Tamil, India/Sri Lanka
tat_Cyrl,    Tatar, Russia
tel_Telu,    Telugu, India
tgk_Cyrl,    Tajik, Tajikistan
tgl_Latn,    Tagalog, Philippines
tha_Thai,    Thai, Thailand
tir_Ethi,    Tigrinya, Eritrea/Ethiopia
taq_Latn,    Tamasheq (Latin script), Mali/Niger
taq_Tfng,    Tamasheq (Tifinagh script), Mali/Niger
tpi_Latn,    Tok Pisin, Papua New Guinea
tsn_Latn,    Tswana, Botswana/South Africa
tso_Latn,    Tsonga, South Africa/Zimbabwe
tuk_Latn,    Turkmen, Turkmenistan
tum_Latn,    Tumbuka, Malawi
tur_Latn,    Turkish, Turkey
twi_Latn,    Twi, Ghana
tzm_Tfng,    Central Atlas Tamazight, Morocco
ukr_Cyrl,    Ukrainian, Ukraine
umb_Latn,    Umbundu, Angola
urd_Arab,    Urdu, Pakistan/India
uzn_Latn,    Northern Uzbek, Uzbekistan
vec_Latn,    Venetian, Italy
vie_Latn,    Vietnamese, Vietnam
war_Latn,    Waray, Philippines
wol_Latn,    Wolof, Senegal
xho_Latn,    Xhosa, South Africa
ydd_Hebr,    Eastern Yiddish, Eastern Europe/Israel
yor_Latn,    Yoruba, Nigeria
zul_Latn,    Zulu, South Africa
```

## 🆘 FAQ
---
### Model Loading Failed
```bash
# Retry with auto-download mode
python translate.py -i input.srt --auto-download
```

### Insufficient Memory
- Try using the OPUS-MT model

### Poor Translation Quality
- Try using the NLLB model
- Adjust the max-length parameter
- Check the input text format

## 📝 Changelog

- **v1.0**: Added translation script `translate.py`

## 🤝 Contributing

Feel free to submit Issues and Pull Requests to improve this tool!

## Contact Me
   julong[at]111.com

### Support with a Donation 👍
This project is maintained by an individual. If you find this script helpful, please consider making a donation by scanning the WeChat QR code. Thank you for your support!

![WeChat Reward Code](WeChat_Reward_Code.png)

****
## 📄 License

MIT License
