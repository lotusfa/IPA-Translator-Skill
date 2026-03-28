#!/usr/bin/env python3
"""
IPA Translator - Standalone command-line tool for converting text to IPA.

Usage:
    uv run scripts/ipa-translator.py "hello" --lang en_US
    uv run scripts/ipa-translator.py "你好" --lang yue --show-word-form
    uv run scripts/ipa-translator.py "謝謝" --lang yue --format Jyutping
"""

import argparse
import json
from pathlib import Path
from typing import Dict


def _load_ipa_dict(lang_code: str, data_dir: Path) -> Dict[str, str]:
    """Load IPA dictionary for the given language code."""
    # Map language codes to their JSON files
    lang_files = {
        "yue": "yue.json",
        "en_UK": "en_UK.json",
        "en_US": "en_US.json",
        "eo": "eo.json",
        "fr_FR": "fr_FR.json",
        "fr_QC": "fr_QC.json",
        "ja": "ja.json",
        "zh_hans": "zh_hans.json",
        "zh_hant": "zh_hant.json",
        "fa": "fa.json",
        "es_ES": "es_ES.json",
        "es_MX": "es_MX.json",
    }

    if lang_code not in lang_files:
        available = ", ".join(lang_files.keys())
        raise ValueError(f'Unsupported language code: "{lang_code}". Available: {available}')

    json_path = data_dir / lang_files[lang_code]
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)


def _preprocess_eng(text: str) -> str:
    """
    Preprocess English text:
    - Convert A-Z to lowercase a-z
    - Remove '.', ',', and newline characters
    """
    text = text.translate(str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz"
    ))
    for ch in ".\n,":
        text = text.replace(ch, "")
    return text


def _format_ipa_num(txt: str) -> str:
    """Replace tone symbols with numeric tones."""
    return (
        txt.replace("\u0265", "5")   # ˥
           .replace("\u0267", "3")   # ˧
           .replace("\u0268", "2")   # ˨
           .replace("\u0261", "1")   # ˩
           .replace(":", "")
    )


def _format_jyutping(txt: str) -> str:
    """Convert Cantonese tone marks to Jyutping numbers."""
    replacements = [
        ("\u0265\u026d", "1"),  # ˥˧
        ("\u0265\u0265", "1"),  # ˥˥
        ("\u0267\u0265", "2"),  # ˧˥
        ("\u0267\u0267", "3"),  # ˧˧
        ("\u0268\u0261", "4"),  # ˨˩
        ("\u0261\u0261", "4"),  # ˩˩
        ("\u0261\u0267", "5"),  # ˩˧
        ("\u0268\u0267", "5"),  # ˨˧
        ("\u0268\u0268", "6"),  # ˨˨
        ("k\u0265", "k7"),
        ("k\u0267", "k8"),
        ("k\u0268", "k9"),
        ("t\u0265", "t7"),
        ("t\u0267", "t8"),
        ("t\u0268", "t9"),
        ("p\u0265", "p7"),
        ("p\u0267", "p8"),
        ("p\u0268", "p9"),
        ("\u0265", "1"),
        ("\u0267", "3"),
        ("\u0268", "6"),
        (":", ""),
    ]
    for old, new in replacements:
        txt = txt.replace(old, new)
    return txt


def _translate_to_ipa_en(
    input_string: str,
    lang_code: str,
    show_word_form: bool = False,
    data_dir: Path = None,
) -> str:
    """
    Translate English input string to IPA.

    1. Split input into words
    2. Preprocess each word (lowercase, strip punctuation)
    3. Look up in IPA dictionary
    4. Return IPA transcription or original word
    """
    ipa_dict = _load_ipa_dict(lang_code, data_dir)
    words = input_string.split()
    result_parts = []

    for word in words:
        if not word:
            continue

        t_word = _preprocess_eng(word)

        if t_word in ipa_dict:
            ipa = ipa_dict[t_word]
            if show_word_form:
                result_parts.append(f"{t_word}/{ipa}/")
            else:
                result_parts.append(f"/{ipa}/")
        else:
            result_parts.append(word)

    return " ".join(result_parts)


def _translate_to_ipa_zh(
    input_string: str,
    lang_code: str,
    show_word_form: bool = False,
    output_format: str = "org",
    data_dir: Path = None,
) -> str:
    """
    Translate Chinese/Cantonese input to IPA.

    Supports:
    - Direct character lookup
    - Multi-character word search (up to 6 characters)
    - Output formats: org, num, Jyutping
    """
    ipa_dict = _load_ipa_dict(lang_code, data_dir)

    chars = list(input_string)
    i = 0
    result_parts = []

    while i < len(chars):
        ch = chars[i]

        # Direct character lookup
        if ch in ipa_dict:
            ipa = ipa_dict[ch]
            if show_word_form:
                result_parts.append(f"{ch}/{ipa}/")
            else:
                result_parts.append(f"/{ipa}/")
            i += 1
            continue

        # Try multi-character word search (up to 6 characters)
        candidates = ["".join(chars[i:i+L]) for L in range(1, 7) if i + L <= len(chars)]
        match = None
        for cand in reversed(candidates):  # longest first
            if cand in ipa_dict:
                match = cand
                break

        if match:
            ipa = ipa_dict[match]
            if show_word_form:
                result_parts.append(f"{match}/{ipa}/")
            else:
                result_parts.append(f"/{ipa}/")
            i += len(match)
            continue

        # No match - copy original character
        result_parts.append(ch)
        i += 1

    raw_result = "".join(result_parts)

    # Apply output format
    if output_format == "num":
        return _format_ipa_num(raw_result)
    elif output_format == "Jyutping":
        return _format_jyutping(raw_result)
    else:
        return raw_result


def translate_to_ipa(
    input_string: str,
    lang_code: str,
    show_word_form: bool = False,
    output_format: str = "org",
    data_dir: Path = None,
) -> str:
    """
    Main translation function. Routes to language-specific handlers.

    Languages that use character-based translation:
    - yue (Cantonese)
    - zh_hans (Mandarin Simplified)
    - zh_hant (Mandarin Traditional)

    All other languages use word-based translation.
    """
    if data_dir is None:
        # Default to data directory relative to this script
        data_dir = Path(__file__).parent.parent / "data"

    zh_languages = ["zh_hans", "zh_hant", "yue"]

    if lang_code in zh_languages:
        return _translate_to_ipa_zh(
            input_string, lang_code, show_word_form, output_format, data_dir
        )
    else:
        return _translate_to_ipa_en(
            input_string, lang_code, show_word_form, data_dir
        )


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to International Phonetic Alphabet (IPA)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "hello" --lang en_US
  %(prog)s "你好" --lang yue
  %(prog)s "謝謝" --lang yue --format Jyutping
  %(prog)s "hello world" --lang en_UK --show-word-form

Available languages:
  yue, en_US, en_UK, eo, fr_FR, fr_QC, ja,
  zh_hans, zh_hant, fa, es_ES, es_MX

Available formats:
  org (default) - Original IPA with tone marks
  num - Numeric tone representation
  Jyutping - Cantonese Jyutping system
        """
    )

    parser.add_argument(
        "text",
        help="Text to translate to IPA"
    )
    parser.add_argument(
        "--lang", "-l",
        required=True,
        help="Language code (e.g., yue, en_US, zh_hans)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["org", "num", "Jyutping"],
        default="org",
        help="Output format (default: org)"
    )
    parser.add_argument(
        "--show-word-form", "-w",
        action="store_true",
        help="Show word form along with IPA (e.g., word/IPA/)"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Path to IPA dictionary data directory"
    )

    args = parser.parse_args()

    data_dir = args.data_dir
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"

    try:
        result = translate_to_ipa(
            args.text,
            args.lang,
            show_word_form=args.show_word_form,
            output_format=args.format,
            data_dir=data_dir,
        )
        print(result)
    except ValueError as e:
        import sys
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
