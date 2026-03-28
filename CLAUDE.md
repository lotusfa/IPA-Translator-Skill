# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

IPA Translator is a standalone command-line tool that converts text to International Phonetic Alphabet (IPA) transcriptions for multiple languages. Part of the OpenClaw skills ecosystem.

## Usage

```bash
# Basic translation
uv run scripts/ipa-translator.py "hello" --lang en_US

# Cantonese with Jyutping format
uv run scripts/ipa-translator.py "謝謝" --lang yue --format Jyutping

# Show word forms
uv run scripts/ipa-translator.py "你好" --lang yue --show-word-form

# Help
uv run scripts/ipa-translator.py --help
```

## Language Support

| Code | Language | Mode | Notes |
|------|----------|------|-------|
| `yue` | Cantonese | Character + word search | Supports multi-character lookup |
| `zh_hans` | Mandarin (Simplified) | Character + word search | |
| `zh_hant` | Mandarin (Traditional) | Character + word search | |
| `en_US` | English (US) | Word lookup | Punctuation stripped |
| `en_UK` | English (UK) | Word lookup | |
| `ja` | Japanese | Character lookup | |
| `eo` | Esperanto | Word lookup | |
| `fr_FR` | French (FR) | Word lookup | |
| `fr_QC` | French (QC) | Word lookup | |
| `es_ES` | Spanish (ES) | Word lookup | |
| `es_MX` | Spanish (MX) | Word lookup | |
| `fa` | Persian | Word lookup | |

## Output Formats

| Format | Description |
|--------|-------------|
| `org` (default) | Original IPA with tone marks |
| `num` | Numeric tone representation |
| `Jyutping` | Cantonese Jyutping system |

## Architecture

Single-file implementation with no external Python dependencies:

- **`scripts/ipa-translator.py`**: Main script with translation logic
  - `_load_ipa_dict()` - Loads language-specific IPA dictionaries from JSON
  - `_translate_to_ipa_en()` - Word-based translation for English and similar languages
  - `_translate_to_ipa_zh()` - Character-based translation with multi-word search for Chinese/Cantonese
  - `_format_ipa_num()` - Converts tone symbols to numeric representation
  - `_format_jyutping()` - Converts to Cantonese Jyutping format
  - `translate_to_ipa()` - Main entry point, routes to language-specific handlers
  - `main()` - CLI argument parsing

- **`data/`**: IPA dictionary JSON files (one per language)
  - Format: `{word/character: ipa_transcription}`

- **`config.json`**: Configuration for default language, formats, and language mappings

## Key Design Patterns

1. **Language routing**: Chinese languages (`yue`, `zh_hans`, `zh_hant`) use character-based translation with multi-character word search (up to 6 chars); all others use word-based
2. **Fallback behavior**: Unknown words/characters pass through unchanged
3. **Preprocessing**: English text is lowercased and stripped of punctuation (`.`, `,`, `\n`) before lookup
4. **Longest-match-first**: For Chinese, tries multi-character words up to 6 characters, preferring longest matches

## Testing

Run these manual tests to verify functionality:

```bash
# Test English
uv run scripts/ipa-translator.py "hello world" --lang en_US

# Test Cantonese
uv run scripts/ipa-translator.py "你好" --lang yue

# Test Cantonese with word forms
uv run scripts/ipa-translator.py "你好" --lang yue --show-word-form

# Test Jyutping format
uv run scripts/ipa-translator.py "謝謝" --lang yue --format Jyutping

# Test Mandarin
uv run scripts/ipa-translator.py "你好" --lang zh_hans

# Test unsupported word (should pass through)
uv run scripts/ipa-translator.py "xyznonexistent" --lang en_US
```

## Reference

- Reference implementation: `reference/openapi-server/` (FastAPI version)
- IPA dictionary data source: https://open-dict-data.github.io/
- Original JS implementation: https://toolbox.lotusfa.com/ipa/cantonese/index.html
