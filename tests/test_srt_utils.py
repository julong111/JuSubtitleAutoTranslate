import pytest
from src.srt_utils import get_output_filename


@pytest.mark.parametrize(
    "input_filename, output_lang, expected_filename",
    [
        # 基础测试：文件名不带语言代码
        ("movie_title.srt", "zh-cn", "movie_title.zh-cn.srt"),
        # 文件名带有旧语言代码，使用横杠
        ("movie_title-en.srt", "zh-cn", "movie_title.zh-cn.srt"),
        # 文件名带有旧语言代码，使用下划线
        ("movie_title_en.srt", "zh-cn", "movie_title.zh-cn.srt"),
        # 文件名带有旧语言代码，使用点
        ("movie_title.en.srt", "zh-cn", "movie_title.zh-cn.srt"),
        # 转换到其他语言
        ("movie_title.zh-tw.srt", "en", "movie_title.en.srt"),
        # 多个后缀，只替换语言代码
        ("movie_title.part1.eng.srt", "zh-cn", "movie_title.part1.zh-cn.srt"),
        # 复杂文件名，不含语言代码
        ("s01e01.the_show_name.srt", "fr", "s01e01.the_show_name.fr.srt"),
        # NLLB格式语言代码
        ("movie_title.eng_Latn.srt", "zh-cn", "movie_title.zh-cn.srt"),
        # NLLB格式语言代码转换到NLLB格式语言代码
        ("movie_title.eng_Latn.srt", "zho_Hans", "movie_title.zho_Hans.srt"),
    ],
)
def test_get_output_filename(tmp_path, input_filename, output_lang, expected_filename):
    # 使用 pytest 内置的临时目录 fixture
    temp_dir = tmp_path

    # 创建一个虚拟输入文件
    input_path = temp_dir / input_filename
    input_path.touch()

    # 调用函数并检查结果
    output_path = get_output_filename(input_path, output_lang)
    expected_path = temp_dir / expected_filename

    assert output_path == expected_path, (
        f"输入: {input_filename}, 目标: {output_lang}, 预期: {expected_path}, 实际: {output_path}"
    )
