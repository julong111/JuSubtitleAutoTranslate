import pytest
from pathlib import Path

from language_code_utils import (
    ISO_639_2T_to_ISO_639_1,
    ISO_15924_to_ISO_3166_1,
    ISO_639_2T_ISO_15924_to_ISO_639_1_ISO_3166_1,
    ISO_639_1_to_ISO_639_2T,
    ISO_3166_1_to_ISO_15924,
    ISO_639_1_ISO_3166_1_to_ISO_639_2T_ISO_15924,
)

from srt_utils import get_output_file


# 测试 ISO_639_2T_to_ISO_639_1 函数
@pytest.mark.parametrize(
    "input_code, expected_code",
    [
        ("zho", "zh"),
        ("eng", "en"),
        ("fra", "fr"),
        ("jpn", "ja"),
        ("kor", "ko"),
        ("ger", "de"),
        ("xyz", None),  # 测试不存在的代码
        ("", None),  # 测试空字符串
    ],
)
def test_iso_639_2t_to_iso_639_1(input_code, expected_code):
    assert ISO_639_2T_to_ISO_639_1(input_code) == expected_code


# 测试 ISO_15924_to_ISO_3166_1 函数
@pytest.mark.parametrize(
    "input_code, expected_code",
    [
        ("Hans", "cn"),
        ("Hant", "tw"),
        ("Latn", "us"),
        ("Cyrl", "ru"),
        ("Jpan", "jp"),
        ("Hang", "kr"),
        ("Xyz", None),  # 测试不存在的代码
        ("", None),  # 测试空字符串
    ],
)
def test_iso_15924_to_iso_3166_1(input_code, expected_code):
    assert ISO_15924_to_ISO_3166_1(input_code) == expected_code


# 测试 ISO_639_2T_ISO_15924_to_ISO_639_1_ISO_3166_1 函数
@pytest.mark.parametrize(
    "input_tag, expected_tag",
    [
        ("zho_Hans", "zh-cn"),
        ("zho_Hant", "zh-tw"),
        ("eng_Latn", "en-us"),
        ("rus_Cyrl", "ru-ru"),
        ("jpn_Jpan", "ja-jp"),
        # 测试无效或不存在的输入
        ("zho_Arab", None),
        ("zho", None),
        ("eng_latn", "en-us"),  # 确保小写也能正常处理
        ("xyz_Xyz", None),
        ("", None),
    ],
)
def test_full_conversion(input_tag, expected_tag):
    assert ISO_639_2T_ISO_15924_to_ISO_639_1_ISO_3166_1(input_tag) == expected_tag


# 测试 ISO_639_1_to_ISO_639_2T 函数
@pytest.mark.parametrize(
    "input_code, expected_code",
    [
        ("zh", "zho"),
        ("ZH", "zho"),  # 测试大写
        ("en", "eng"),
        ("EN", "eng"),
        ("fr", "fra"),
        ("ja", "jpn"),
        ("ko", "kor"),
        ("de", "ger"),
        ("xx", None),  # 测试不存在的代码
        ("", None),  # 测试空字符串
    ],
)
def test_iso_639_1_to_iso_639_2t(input_code, expected_code):
    assert ISO_639_1_to_ISO_639_2T(input_code) == expected_code


# 测试 ISO_3166_1_to_ISO_15924 函数
@pytest.mark.parametrize(
    "input_code, expected_code",
    [
        ("cn", "Hans"),
        ("CN", "Hans"),
        ("tw", "Hant"),
        ("us", "Latn"),
        ("ru", "Cyrl"),
        ("jp", "Jpan"),
        ("kr", "Hang"),
        ("xx", None),  # 测试不存在的代码
        ("", None),  # 测试空字符串
    ],
)
def test_iso_3166_1_to_iso_15924(input_code, expected_code):
    assert ISO_3166_1_to_ISO_15924(input_code) == expected_code


# 测试 ISO_639_1_ISO_3166_1_to_ISO_639_2T_ISO_15924 函数
@pytest.mark.parametrize(
    "input_tag, expected_tag",
    [
        ("zh-cn", "zho_Hans"),
        ("zh-tw", "zho_Hant"),
        ("en-us", "eng_Latn"),
        ("ru-ru", "rus_Cyrl"),
        ("ja-jp", "jpn_Jpan"),
        # 测试大小写
        ("ZH-CN", "zho_Hans"),
        ("en_US", "eng_Latn"),
        # 测试无效或不存在的输入
        ("zh-xx", None),
        ("xx-cn", None),
        ("zh-", None),
        ("", None),
    ],
)
def test_reverse_full_conversion(input_tag, expected_tag):
    assert ISO_639_1_ISO_3166_1_to_ISO_639_2T_ISO_15924(input_tag) == expected_tag


@pytest.mark.parametrize(
    "input_path, output_arg, expected_output",
    [
        # 场景 1: output_arg 为 None
        ("test/movie_title.srt", None, "test/movie_title.translated.srt"),
        # 场景 2: output_arg 是一个目录 (相对路径)
        (
            "test/movie_title.srt",
            "translated_dir",
            "translated_dir/movie_title.translated.srt",
        ),
        # 场景 3: output_arg 是一个完整的文件名 (相对路径)
        ("test/movie_title.srt", "test/final_output.srt", "test/final_output.srt"),
    ],
)
def test_get_output_file(tmp_path: Path, input_path, output_arg, expected_output):
    """
    使用简化的路径测试 get_output_file 函数。
    """
    # 1. 在 tmp_path 下模拟输入文件
    temp_input_path = tmp_path / input_path
    temp_input_path.parent.mkdir(parents=True, exist_ok=True)
    temp_input_path.touch()

    # 2. 模拟 output_arg 的目录（如果需要）
    test_output_arg = None
    if output_arg is not None:
        # 将所有 output_arg 都作为 tmp_path 的子路径处理
        output_path_obj = tmp_path / output_arg
        # 如果 output_arg 是一个目录，则创建它
        if not output_path_obj.suffix:
            output_path_obj.mkdir(parents=True, exist_ok=True)
        test_output_arg = str(output_path_obj)

    # 3. 调用函数
    result = get_output_file(temp_input_path, output=test_output_arg)

    # 4. 构建预期的输出路径
    final_expected_output = tmp_path / expected_output

    # 5. 断言
    assert result == final_expected_output
    assert isinstance(result, Path)
