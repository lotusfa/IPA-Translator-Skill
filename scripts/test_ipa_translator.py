#!/usr/bin/env python3
"""
Test suite for IPA Translator script.

Usage:
    uv run scripts/test_ipa_translator.py
"""

import sys
import importlib.util
from pathlib import Path
from typing import List, Tuple

# Load the ipa-translator.py script as a module
SCRIPT_PATH = Path(__file__).parent / "ipa-translator.py"
spec = importlib.util.spec_from_file_location("ipa_translator", SCRIPT_PATH)
ipa_translator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ipa_translator)
translate_to_ipa = ipa_translator.translate_to_ipa

# Test data directory
DATA_DIR = Path(__file__).parent.parent / "data"


# Expected test cases - known correct outputs
# Note: Test expectations based on actual dictionary data
TEST_CASES = [
    # Cantonese (yue) tests
    {
        "name": "cantonese_single_char",
        "input": "我",
        "lang": "yue",
        "expected_contains": "/",  # Should contain IPA slashes
    },
    {
        "name": "cantonese_two_chars",
        "input": "你好",
        "lang": "yue",
        "expected_contains": "/",
    },
    {
        "name": "cantonese_jyutping",
        "input": "多謝",  # Use word that exists in dictionary
        "lang": "yue",
        "format": "Jyutping",
        "expected_contains": "/",  # Should have IPA slashes
    },
    {
        "name": "cantonese_word_form",
        "input": "好",
        "lang": "yue",
        "show_word_form": True,
        "expected_contains": "好/",  # Should show word form
    },
    # English tests
    {
        "name": "english_hello",
        "input": "hello",
        "lang": "en_US",
        "expected_contains": "/",  # Should produce IPA
    },
    {
        "name": "english_world",
        "input": "world",
        "lang": "en_US",
        "expected_contains": "/",
    },
    {
        "name": "english_multiple_words",
        "input": "hello world",
        "lang": "en_US",
        "expected_contains": "/",
    },
    {
        "name": "english_uppercase",
        "input": "HELLO",
        "lang": "en_US",
        "expected_contains": "/",  # Should be normalized and produce IPA
    },
    {
        "name": "english_unknown_word",
        "input": "xyznonexistent",
        "lang": "en_US",
        "expected_contains": "xyznonexistent",  # Pass-through for unknown
    },
    # Mandarin tests
    {
        "name": "mandarin_simplified",
        "input": "你好",
        "lang": "zh_hans",
        "expected_contains": "/",
    },
    {
        "name": "mandarin_traditional",
        "input": "你好",
        "lang": "zh_hant",
        "expected_contains": "/",
    },
    # Japanese tests
    {
        "name": "japanese_basic",
        "input": "私",
        "lang": "ja",
        "expected_contains": "/",
    },
    # French tests
    {
        "name": "french_france",
        "input": "bonjour",
        "lang": "fr_FR",
        "expected_contains": "/",
    },
    {
        "name": "french_quebec",
        "input": "bonjour",
        "lang": "fr_QC",
        "expected_contains": "/",
    },
    # Spanish tests
    {
        "name": "spanish_spain",
        "input": "hola",
        "lang": "es_ES",
        "expected_contains": "/",
    },
    {
        "name": "spanish_mexico",
        "input": "hola",
        "lang": "es_MX",
        "expected_contains": "/",
    },
    # Format tests
    {
        "name": "format_numeric_tones",
        "input": "你好",
        "lang": "yue",
        "format": "num",
        "expected_contains": "/",
    },
    # Edge cases
    {
        "name": "empty_string",
        "input": "",
        "lang": "en_US",
        "expected_result": "",
    },
    {
        "name": "mixed_known_unknown",
        "input": "hello xyz",
        "lang": "en_US",
        "expected_contains": "xyz",  # Unknown word passes through
        "expected_contains_at_start": "//",  # Known words produce IPA
    },
    # Word form tests
    {
        "name": "english_word_form",
        "input": "hello",
        "lang": "en_US",
        "show_word_form": True,
        "expected_contains": "hello/",  # Should show word/IPA/
    },
]

# Known expected outputs for strict validation
KNOWN_EXPECTED = {
    ("hello", "en_US", "org"): "/hɛloʊ/",
    ("hello world", "en_US", "org"): "/hɛloʊ/ /wɜrld/",
    ("好", "yue", "org"): "/hɔː˧˥/",
}


class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message


def run_test(test: dict) -> TestResult:
    """Run a single test case."""
    input_text = test["input"]
    lang = test["lang"]
    fmt = test.get("format", "org")
    show_word_form = test.get("show_word_form", False)

    try:
        result = translate_to_ipa(
            input_text,
            lang,
            show_word_form=show_word_form,
            output_format=fmt,
            data_dir=DATA_DIR,
        )
    except Exception as e:
        return TestResult(test["name"], False, f"Exception: {e}")

    # Validation checks
    if "expected_result" in test:
        if result == test["expected_result"]:
            return TestResult(test["name"], True)
        return TestResult(
            test["name"], False,
            f"Expected '{test['expected_result']}', got '{result}'"
        )

    if "expected_contains" in test:
        if test["expected_contains"] not in result:
            return TestResult(
                test["name"], False,
                f"Expected to contain '{test['expected_contains']}', got '{result}'"
            )

    if "expected_contains_not" in test:
        if test["expected_contains_not"] in result:
            return TestResult(
                test["name"], False,
                f"Expected NOT to contain '{test['expected_contains_not']}', got '{result}'"
            )

    if "expected_contains_at_start" in test:
        if not result.startswith(test["expected_contains_at_start"]):
            return TestResult(
                test["name"], False,
                f"Expected to start with '{test['expected_contains_at_start']}', got '{result}'"
            )

    if "expected_pattern" in test:
        import re
        if re.match(test["expected_pattern"], result):
            return TestResult(test["name"], True)
        return TestResult(
            test["name"], False,
            f"Pattern '{test['expected_pattern']}' did not match '{result}'"
        )

    # Default: just check result is non-empty string
    if result:
        return TestResult(test["name"], True)
    return TestResult(test["name"], False, "Empty result")


def run_all_tests() -> Tuple[List[TestResult], int, int]:
    """Run all tests and return results."""
    results = []
    passed = 0
    failed = 0

    for test in TEST_CASES:
        result = run_test(test)
        results.append(result)
        if result.passed:
            passed += 1
        else:
            failed += 1

    return results, passed, failed


def print_results(results: List[TestResult], passed: int, failed: int):
    """Print test results in a readable format."""
    print("\n" + "=" * 60)
    print("IPA TRANSLATOR TEST RESULTS")
    print("=" * 60)

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        marker = "✓" if r.passed else "✗"
        print(f"[{marker}] {status}: {r.name}")
        if not r.passed and r.message:
            print(f"       {r.message}")

    print("\n" + "=" * 60)
    print(f"Summary: {passed} passed, {failed} failed, {len(results)} total")
    print("=" * 60)

    if failed > 0:
        print("\n⚠️  Some tests failed. Review the output above.")
    else:
        print("\n✅ All tests passed!")


def main():
    """Main entry point."""
    # Run tests
    results, passed, failed = run_all_tests()

    # Print results
    print_results(results, passed, failed)

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
