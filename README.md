# IPA Translator

An IPA translation **Skill designed for LLM agents** (Claude Code, etc.). Agents use this skill to translate text to International Phonetic Alphabet (IPA) and romanization formats across 24 languages including Cantonese, Mandarin, English, Japanese, Korean, Vietnamese, French, Spanish, and German.

## Usage

Agents navigate to the web interface with query parameters:

```
https://toolbox.lotusfa.com/ipa/agent.html?language=<code>&input=<text>[&format=<format>][&variant=<variant>]
```

Optional params: `format` (e.g. Jyutping, Pinyin), `variant` (e.g. US/UK, hans/hant).

## Examples

Click to see results:

| Language | Output | Link |
|----------|--------|------|
| Cantonese | Jyutping | [你好 → ngaai5 hou2](https://toolbox.lotusfa.com/ipa/agent.html?language=cantonese&format=Jyutping&input=%E4%BD%A0%E5%A5%BD) |
| Cantonese | IPA | [你好](https://toolbox.lotusfa.com/ipa/agent.html?language=cantonese&input=%E4%BD%A0%E5%A5%BD) |
| Mandarin | Pinyin | [你好 → nǐ hǎo](https://toolbox.lotusfa.com/ipa/agent.html?language=mandarin&variant=hans&format=Pinyin&input=%E4%BD%A0%E5%A5%BD) |
| Mandarin | IPA | [你好](https://toolbox.lotusfa.com/ipa/agent.html?language=mandarin&input=%E4%BD%A0%E5%A5%BD) |
| English (US) | IPA | [hello world](https://toolbox.lotusfa.com/ipa/agent.html?language=english&variant=US&input=hello%20world) |
| English (UK) | IPA | [hello world](https://toolbox.lotusfa.com/ipa/agent.html?language=english&variant=UK&input=hello%20world) |
| Japanese | IPA | [こんにちは](https://toolbox.lotusfa.com/ipa/agent.html?language=japanese&input=%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%81%AF) |
| Korean | IPA | [안녕하세요](https://toolbox.lotusfa.com/ipa/agent.html?language=korean&input=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94) |
| Vietnamese | IPA | [Xin chào](https://toolbox.lotusfa.com/ipa/agent.html?language=vietnamese&variant=S&input=Xin%20chao) |
| German | IPA | [Hallo Welt](https://toolbox.lotusfa.com/ipa/agent.html?language=german&input=Hallo%20Welt) |
| French (FR) | IPA | [Bonjour le monde](https://toolbox.lotusfa.com/ipa/agent.html?language=french&variant=FR&input=Bonjour%20le%20monde) |
| Spanish (ES) | IPA | [Hola mundo](https://toolbox.lotusfa.com/ipa/agent.html?language=spanish&variant=ES&input=Hola%20mundo) |

## Notes

- The page runs entirely client-side (JavaScript). Do not use curl — use a browser tool or WebFetch.
- Non-ASCII input must be URL-encoded.
- See [SKILL.md](SKILL.md) for the full agent interface spec (all language codes, formats, and variants).
