# IPA Translator

Translate text to International Phonetic Alphabet (IPA) and romanization formats for 24 languages.

Supported languages include Cantonese, Mandarin, English, Japanese, Korean, Vietnamese, French, Spanish, German, and more.

## Usage

Open the web interface with query parameters:

```
https://toolbox.lotusfa.com/ipa/agent.html?language=<code>&input=<text>
```

Optional params: `format` (e.g. Jyutping, Pinyin), `variant` (e.g. US/UK, hans/hant).

## Examples

- Cantonese → Jyutping: `?language=cantonese&format=Jyutping&input=%E4%BD%A0%E5%A5%BD`
- Mandarin → Pinyin: `?language=mandarin&variant=hans&format=Pinyin&input=%E4%BD%A0%E5%A5%BD`
- German IPA: `?language=german&input=Hallo%20Welt`

## Notes

- The page runs entirely client-side (JavaScript). Do not use curl — use a browser tool or WebFetch.
- Non-ASCII input must be URL-encoded.
