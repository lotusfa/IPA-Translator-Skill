# IPA Translator Skill

Convert text to International Phonetic Alphabet (IPA) transcriptions for multiple languages.

## Quick Start

```bash
# Basic translation
uv run skills/ipa-translator/scripts/ipa-translator.py "hello" --lang en_US

# Cantonese
uv run scripts/ipa-translator.py "你好" --lang yue

# With word form display
uv run scripts/ipa-translator.py "hello world" --lang en_US --show-word-form

# Jyutping format (Cantonese)
uv run scripts/ipa-translator.py "謝謝" --lang yue --format Jyutping
```

## Available Languages

| Code | Language | Notes |
|------|----------|-------|
| `yue` | Cantonese | Full character + word search |
| `en_US` | English (US) | Word-based lookup |
| `en_UK` | English (UK) | Word-based lookup |
| `zh_hans` | Mandarin (Simplified) | Character + word search |
| `zh_hant` | Mandarin (Traditional) | Character + word search |
| `ja` | Japanese | Character lookup |
| `eo` | Esperanto | Word lookup |
| `fr_FR` | French (FR) | Word lookup |
| `fr_QC` | French (QC) | Word lookup |
| `es_ES` | Spanish (ES) | Word lookup |
| `es_MX` | Spanish (MX) | Word lookup |
| `fa` | Persian | Word lookup |

## Output Formats

| Format | Description |
|--------|-------------|
| `org` | Original IPA with tone marks (default) |
| `num` | Numeric tone representation |
| `Jyutping` | Cantonese Jyutping system |

## Usage

### Help

```bash
uv run scripts/ipa-translator.py --help
```

### Examples

```bash
# English
uv run scripts/ipa-translator.py "hello world" --lang en_US
# Output: /hɛloʊ/ /wɜrld/

# Cantonese with word form
uv run scripts/ipa-translator.py "你好" --lang yue --show-word-form
# Output: 你/ŋ̍˧˥/ 好/hɔː˧˥/

# Jyutping format
uv run scripts/ipa-translator.py "謝謝" --lang yue --format Jyutping
# Output: /he6/ /he6/

# Mandarin
uv run scripts/ipa-translator.py "你好" --lang zh_hans
# Output: /ni˥˩/ /xɤ˥˩/
```

## Configuration

See `config.json` for available languages and default settings.

## Implementation

This skill uses standalone Python scripts with no external dependencies. IPA dictionaries are loaded from JSON files in the `data/` directory.

### File Structure

```
skills/ipa-translator/
├── README.md              # This file
├── SKILL.md               # Agent instructions
├── config.json            # Configuration
├── scripts/
│   └── ipa-translator.py # Main translation script
└── data/                  # IPA dictionary JSON files
    ├── yue.json
    ├── en_US.json
    ├── en_UK.json
    └── ...
```

## Testing

Run the test suite to verify functionality:

```bash
uv run scripts/test_ipa_translator.py
```

## References

- Reference implementation: `/Users/FJ/.openclaw/skills/ipa-translator/reference/openapi-server/`
- IPA dictionary data source: https://open-dict-data.github.io/
- Original JS implementation: https://toolbox.lotusfa.com/ipa/cantonese/index.html
