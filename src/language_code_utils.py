#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/16
# @Author : julong@111.com
# @File : language_code_utils.py
# @Description : ISO标准语言代码通用转换工具

_nllb_language_codes = [
    "ace_Arab",
    "ace_Latn",
    "acm_Arab",
    "acq_Arab",
    "aeb_Arab",
    "afr_Latn",
    "ajp_Arab",
    "aka_Latn",
    "amh_Ethi",
    "apc_Arab",
    "arb_Arab",
    "ars_Arab",
    "ary_Arab",
    "arz_Arab",
    "asm_Beng",
    "ast_Latn",
    "awa_Deva",
    "ayr_Latn",
    "azb_Arab",
    "azj_Latn",
    "bak_Cyrl",
    "bam_Latn",
    "ban_Latn",
    "bel_Cyrl",
    "bem_Latn",
    "ben_Beng",
    "bho_Deva",
    "bjn_Arab",
    "bjn_Latn",
    "bod_Tibt",
    "bos_Latn",
    "bug_Latn",
    "bul_Cyrl",
    "cat_Latn",
    "ceb_Latn",
    "ces_Latn",
    "cjk_Latn",
    "ckb_Arab",
    "crh_Latn",
    "cym_Latn",
    "dan_Latn",
    "deu_Latn",
    "dik_Latn",
    "dyu_Latn",
    "dzo_Tibt",
    "ell_Grek",
    "eng_Latn",
    "epo_Latn",
    "est_Latn",
    "eus_Latn",
    "ewe_Latn",
    "fao_Latn",
    "pes_Arab",
    "fij_Latn",
    "fin_Latn",
    "fon_Latn",
    "fra_Latn",
    "fur_Latn",
    "fuv_Latn",
    "gla_Latn",
    "gle_Latn",
    "glg_Latn",
    "grn_Latn",
    "guj_Gujr",
    "hat_Latn",
    "hau_Latn",
    "heb_Hebr",
    "hin_Deva",
    "hne_Deva",
    "hrv_Latn",
    "hun_Latn",
    "hye_Armn",
    "ibo_Latn",
    "ilo_Latn",
    "ind_Latn",
    "isl_Latn",
    "ita_Latn",
    "jav_Latn",
    "jpn_Jpan",
    "kab_Latn",
    "kac_Latn",
    "kam_Latn",
    "kan_Knda",
    "kas_Arab",
    "kas_Deva",
    "kat_Geor",
    "knc_Arab",
    "knc_Latn",
    "kaz_Cyrl",
    "kbp_Latn",
    "kea_Latn",
    "khm_Khmr",
    "kik_Latn",
    "kin_Latn",
    "kir_Cyrl",
    "kmb_Latn",
    "kon_Latn",
    "kor_Hang",
    "kmr_Latn",
    "lao_Laoo",
    "lvs_Latn",
    "lij_Latn",
    "lim_Latn",
    "lin_Latn",
    "lit_Latn",
    "lmo_Latn",
    "ltg_Latn",
    "ltz_Latn",
    "lua_Latn",
    "lug_Latn",
    "luo_Latn",
    "lus_Latn",
    "mag_Deva",
    "mai_Deva",
    "mal_Mlym",
    "mar_Deva",
    "min_Latn",
    "mkd_Cyrl",
    "plt_Latn",
    "mlt_Latn",
    "mni_Beng",
    "khk_Cyrl",
    "mos_Latn",
    "mri_Latn",
    "zsm_Latn",
    "mya_Mymr",
    "nld_Latn",
    "nno_Latn",
    "nob_Latn",
    "npi_Deva",
    "nso_Latn",
    "nus_Latn",
    "nya_Latn",
    "oci_Latn",
    "gaz_Latn",
    "ory_Orya",
    "pag_Latn",
    "pan_Guru",
    "pap_Latn",
    "pol_Latn",
    "por_Latn",
    "prs_Arab",
    "pbt_Arab",
    "quy_Latn",
    "ron_Latn",
    "run_Latn",
    "rus_Cyrl",
    "sag_Latn",
    "san_Deva",
    "sat_Beng",
    "scn_Latn",
    "shn_Mymr",
    "sin_Sinh",
    "slk_Latn",
    "slv_Latn",
    "smo_Latn",
    "sna_Latn",
    "snd_Arab",
    "som_Latn",
    "sot_Latn",
    "spa_Latn",
    "als_Latn",
    "srd_Latn",
    "srp_Cyrl",
    "ssw_Latn",
    "sun_Latn",
    "swe_Latn",
    "swh_Latn",
    "szl_Latn",
    "tam_Taml",
    "tat_Cyrl",
    "tel_Telu",
    "tgk_Cyrl",
    "tgl_Latn",
    "tha_Thai",
    "tir_Ethi",
    "taq_Latn",
    "taq_Tfng",
    "tpi_Latn",
    "tsn_Latn",
    "tso_Latn",
    "tuk_Latn",
    "tum_Latn",
    "tur_Latn",
    "twi_Latn",
    "tzm_Tfng",
    "uig_Arab",
    "ukr_Cyrl",
    "umb_Latn",
    "urd_Arab",
    "uzn_Latn",
    "vec_Latn",
    "vie_Latn",
    "war_Latn",
    "wol_Latn",
    "xho_Latn",
    "ydd_Hebr",
    "yor_Latn",
    "yue_Hant",
    "zho_Hans",
    "zho_Hant",
    "zul_Latn",
]

nllb_language_codes = [code.lower() for code in _nllb_language_codes]

# 映射表：ISO 639-2/T 到 ISO 639-1 的语言代码映射
LANG_2_TO_1_MAP = {
    "zho": "zh",
    "eng": "en",
    "fra": "fr",
    "spa": "es",
    "rus": "ru",
    "jpn": "ja",
    "kor": "ko",
    "ger": "de",  # 添加德语
    # 可以根据需要添加更多映射
}
# 新增：ISO 639-1 到 ISO 639-2/T 的反向映射
# 从 LANG_2_TO_1_MAP 自动生成
LANG_1_TO_2_MAP = {v: k for k, v in LANG_2_TO_1_MAP.items()}

# 映射表：ISO 15924 脚本代码到 ISO 3166-1 地区代码的映射
# 这通常用于将脚本代码映射到最常见的地区用法
SCRIPT_TO_REGION_MAP = {
    "Hans": "cn",  # 简体中文 -> 中国大陆
    "Hant": "tw",  # 繁体中文 -> 台湾
    "Latn": "us",  # 拉丁字母 -> 美国
    "Cyrl": "ru",  # 西里尔字母 -> 俄罗斯
    "Jpan": "jp",  # 日文 -> 日本
    "Hang": "kr",  # 韩文 -> 韩国
    # 可以根据需要添加更多映射
}

# 映射表：ISO 3166-1 地区代码到 ISO 15924 脚本代码的反向映射
# 从上面的 SCRIPT_TO_REGION_MAP 自动生成
REGION_TO_SCRIPT_MAP = {v: k for k, v in SCRIPT_TO_REGION_MAP.items()}


# 通用的不区分大小写的查找辅助函数
def find_value_case_insensitive(d: dict, key: str) -> any:
    """
    在字典中进行不区分大小写的键查找。

    Args:
        d (dict): 要查找的字典。
        key (str): 要查找的键。

    Returns:
        any: 如果找到匹配的值，则返回该值；否则返回 None。
    """
    if key is None:
        return None
    for k, v in d.items():
        if k.lower() == key.lower():
            return v
    return None


def ISO_639_2T_to_ISO_639_1(lang_2_code: str) -> str or None:
    """将 ISO 639-2/T 语言代码转换为 ISO 639-1 语言代码。"""
    return find_value_case_insensitive(LANG_2_TO_1_MAP, lang_2_code)


def ISO_15924_to_ISO_3166_1(script_code: str) -> str or None:
    """将 ISO 15924 脚本代码转换为 ISO 3166-1 地区代码。"""
    return find_value_case_insensitive(SCRIPT_TO_REGION_MAP, script_code)


def ISO_639_2T_ISO_15924_to_ISO_639_1_ISO_3166_1(tag: str) -> str or None:
    """
    将 ISO 639-2/T + ISO 15924 格式的语言标签转换为 ISO 639-1 + ISO 3166-1 格式。

    Args:
        tag (str): ISO 639-2/T + ISO 15924 格式的语言标签，例如 'zho_Hans'。

    Returns:
        str or None: 转换后的 ISO 639-1 + ISO 3166-1 格式标签，例如 'zh-cn'。
                     如果无法转换，则返回 None。
    """
    parts = tag.replace("-", "_").split("_")
    if len(parts) != 2:
        return None

    lang_2_code = parts[0]
    script_code = parts[1]

    lang_1_code = ISO_639_2T_to_ISO_639_1(lang_2_code)
    region_code = ISO_15924_to_ISO_3166_1(script_code)

    if lang_1_code and region_code:
        return f"{lang_1_code}-{region_code}"
    return None


# 新函数 1: 转换 ISO 639-1 语言代码到 ISO 639-2/T
def ISO_639_1_to_ISO_639_2T(lang_1_code: str) -> str or None:
    """
    将 ISO 639-1 语言代码转换为 ISO 639-2/T 语言代码，不区分大小写。
    """
    return find_value_case_insensitive(LANG_1_TO_2_MAP, lang_1_code)


# 新函数 2: 转换 ISO 3166-1 地区代码到 ISO 15924 脚本代码
def ISO_3166_1_to_ISO_15924(region_code: str) -> str or None:
    """
    将 ISO 3166-1 地区代码转换为 ISO 15924 脚本代码，不区分大小写。
    """
    return find_value_case_insensitive(REGION_TO_SCRIPT_MAP, region_code)


# 新函数 3: 转换 ISO 639-1 + ISO 3166-1 格式到 ISO 639-2T + ISO 15924 格式
def ISO_639_1_ISO_3166_1_to_ISO_639_2T_ISO_15924(tag: str) -> str or None:
    """
    将 ISO 639-1 + ISO 3166-1 格式的语言标签转换为 ISO 639-2T + ISO 15924 格式。

    Args:
        tag (str): ISO 639-1 + ISO 3166-1 格式的语言标签，例如 'zh-cn'。

    Returns:
        str or None: 转换后的 ISO 639-2T + ISO 15924 格式标签，例如 'zho_Hans'。
                     如果无法转换，则返回 None。
    """
    if not isinstance(tag, str):
        return None

    parts = tag.replace("_", "-").lower().split("-")
    if len(parts) != 2:
        return None

    lang_1_code = parts[0]
    region_code = parts[1]

    lang_2_code = ISO_639_1_to_ISO_639_2T(lang_1_code)
    script_code = ISO_3166_1_to_ISO_15924(region_code)

    if lang_2_code and script_code:
        return f"{lang_2_code}_{script_code}"

    return None
