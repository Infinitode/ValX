# ValX

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)
[![Code Size](https://img.shields.io/github/languages/code-size/infinitode/valx)](https://github.com/infinitode/valx)
![Downloads](https://pepy.tech/badge/valx)
![License Compliance](https://img.shields.io/badge/license-compliance-brightgreen.svg)
![PyPI Version](https://img.shields.io/pypi/v/valx)
[![PyPI provenance](https://img.shields.io/badge/PyPI-view%20provenance-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/valx/#security)

An open-source Python library for data cleaning tasks. It includes functions for profanity detection, and removal, and detection and removal of personal information. Also includes hate speech and offensive language detection and removal, using AI.

## Changes in 0.2.7

- Sensitive information redaction now uses exact match positions on each line and merges overlaps, so it won't redact unrelated copies of a substring or leave part of an overlapping match exposed. Parenthesized phone area codes and signed coordinates are included in the matches.
- Profanity filtering supports the documented Finnish `FI` alias and punctuation in custom terms. Detections are in text order and the `Word` value preserves the original casing. Lines surrounded by `$` are no longer silently dropped.
- The bundled hate-speech models load on first use instead of at import time. This release requires Python 3.10 or newer.
- The release workflow builds and tests the wheel and source distribution before publishing both to PyPI with signed attestations.

## Changes in 0.2.6

ValX v0.2.6 fixes a major bug, view the issue here: https://github.com/Infinitode/ValX/issues/4, where profanity lists for multiple languages were missing, under wrong languages, or simply incomplete.

Version 0.2.6 introduces fixes for this using the original language lists data, and includes new handling for languages, including:

- Case insensitivity for language selection: "English", "EN", "en", or variants like "enGliSh" will all work for language selection in the `detect_profanity` and `remove_profanity` functions.

## Changes in 0.2.5

ValX v0.2.5 introduces enhanced flexibility for profanity filtering by adding support for custom profanity lists:

- **Custom Profanity Word Lists**: Users can now provide their own lists of profane words directly as Python lists to the `detect_profanity` and `remove_profanity` functions via the new `custom_words_list` parameter.
- **Standalone Custom Lists**: Utilize your custom profanity list exclusively by setting the `language` parameter to `None`. ValX will then only use the words provided in `custom_words_list`.
- **Combined Lists**: Use a custom list in conjunction with ValX's built-in language-specific wordlists. Simply provide both a `language` (e.g., "English") and your `custom_words_list`. ValX will use the combined set of words.
- **Loading Custom Lists from File**: A new helper function, `load_custom_profanity_from_file(filepath)`, allows you to easily load custom profanity words from a text file.
  - **File Format**: The file should contain one profanity word per line.
  - Lines starting with a hash symbol (`#`) are treated as comments and ignored.
  - Empty lines or lines containing only whitespace are also ignored.
- **Updated Detection Reporting**: The `detect_profanity` function's output now specifies the source of detected profanity more clearly (e.g., "Custom", "Custom + English").

These features give users greater control over the profanity filtering process, allowing for more tailored and specific use cases.

## Changes in 0.2.4

Fixed a major incompatibility issue with `scikit-learn` due to version changes in `scikit-learn v1.3.0` which causes compatibility issues with versions later than `1.2.2`. ValX can now be used with `scikit-learn` versions earlier and later than `1.3.0`!

We've also removed `scikit-learn==1.2.2` as a dependency, as most versions of `scikit-learn` will now work.

## Changes in 0.2.3

We have introduced a new optional `info_type` parameter into our `detect_sensitive_information`, and `remove_sensitive_information` functions, to allow you to have fine-grained control over what sensitive information you want to detect or remove.

Also introduced more detection patterns for other types of sensitive information, including:

- `"iban"`: International Bank Account Number.
- `"mrn"`: Medical Record Number (may not work correctly, depending on provider and country).
- `"icd10"`: International Classification of Diseases, Tenth Revision.
- `"geo_coords"`: Geo-coordinates (latitude and longitude in decimal degrees format).
- `"username"`: Username handles (@username).
- `"file_path"`: File paths (general patterns for both Windows and Unix paths).
- `"bitcoin_wallet"`: Cryptocurrency wallet address.
- `"ethereum_wallet"`: Cryptocurrency wallet addresses.

## Changes in 0.2.2

We have refactored and changed the `detect_profanity` function:

- Removed unnecessary printing
- Now returns more information about each found profanity, including `Line`, `Column`, `Word`, and `Language`.

> [!NOTE]
> You can view [ValX's package documentation](https://infinitode-docs.gitbook.io/documentation/package-documentation/valx-package-documentation) for more information on changes.

## Changes in 0.2.1

Using the AI models in ValX, you can now automatically remove hate speech, or offensive speech from your text data, without needing to run detection and write your own custom implementation method.

## Installation

You can install ValX using pip:

```bash
pip install valx
```

## Supported Python Versions

ValX requires Python 3.10 or newer. CI covers Python 3.10 through 3.14.

## Features

- **Profanity Detection**: Detect profane and NSFW words or terms.
- **Remove Profanity**: Remove profane and NSFW words or terms.
- **Detect Sensitive Information**: Detect sensitive information in text data.
- **Remove Sensitive Information**: Remove sensitive information from text data.
- **Detect Hate Speech**: Detect hate speech or offensive speech in text, using AI.
- **Remove Hate Speech**: Remove hate speech or offensive speech in text, using AI.

### List of supported languages for profanity detection and removal

Pass a language name or code from the table as `language`. Both are case-insensitive. Use `All` to combine all built-in lists.

| Language name | Code |
| --- | --- |
| Arabic | `AR` |
| Czech | `CS` |
| Danish | `DA` |
| German | `DE` |
| English | `EN` |
| Esperanto | `EO` |
| Persian | `FA` |
| Finnish | `FI` |
| Filipino | `FIL` |
| French | `FR` |
| French (CA) | `FR-CA-U-SD-CAQC` |
| Hindi | `HI` |
| Hungarian | `HU` |
| Italian | `IT` |
| Japanese | `JA` |
| Kabyle | `KAB` |
| Korean | `KO` |
| Dutch | `NL` |
| Norwegian | `NO` |
| Polish | `PL` |
| Portuguese | `PT` |
| Russian | `RU` |
| Spanish | `ES` |
| Swedish | `SV` |
| Thai | `TH` |
| Klingon | `TLH` |
| Turkish | `TR` |
| Chinese | `ZH` |

## Usage

### Profanity Detection and Removal

ValX allows for flexible profanity filtering using built-in language lists, custom word lists (provided as Python lists or loaded from files), or a combination of both.

**1. Basic Profanity Detection (Built-in Language)**

```python
from valx import detect_profanity

sample_text = ["This is some fuck and porn text."]
# Detect profanity using the English list
results = detect_profanity(sample_text, language='English')
# results will be:
# [
#   {'Line': 1, 'Column': 14, 'Word': 'fuck', 'Language': 'English'},
#   {'Line': 1, 'Column': 23, 'Word': 'porn', 'Language': 'English'}
# ]
print(results)
```

**2. Profanity Detection with a Custom Word List (Python List)**

You can provide your own list of words to filter.

```python
from valx import detect_profanity

sample_text = ["This contains custombadword1 and also asshole from English list."]
my_custom_words = ["custombadword1", "anothercustom"]

# Option A: Custom list ONLY (language=None)
results_custom_only = detect_profanity(sample_text, language=None, custom_words_list=my_custom_words)
# results_custom_only will detect "custombadword1" with Language: "Custom"
# [{'Line': 1, 'Column': 15, 'Word': 'custombadword1', 'Language': 'Custom'}]
print(results_custom_only)

# Option B: Custom list COMBINED with a built-in language
results_custom_plus_english = detect_profanity(sample_text, language="English", custom_words_list=my_custom_words)
# results_custom_plus_english will detect "custombadword1" and "asshole"
# Language will be "Custom + English"
# [
#   {'Line': 1, 'Column': 15, 'Word': 'custombadword1', 'Language': 'Custom + English'},
#   {'Line': 1, 'Column': 39, 'Word': 'asshole', 'Language': 'Custom + English'}
# ]
print(results_custom_plus_english)
```

**3. Loading Custom Profanity Words from a File**

ValX provides a helper function to load words from a text file (one word per line, '#' for comments).

```python
from valx import detect_profanity, load_custom_profanity_from_file

# Assume 'my_profanity_file.txt' contains:
# customfileword1
# # this is a comment
# customfileword2

custom_words_from_file = load_custom_profanity_from_file("my_profanity_file.txt")
# custom_words_from_file will be: ['customfileword1', 'customfileword2']

sample_text_for_file = ["Text with customfileword1 and built-in shit."]

# Use file-loaded list with English built-in list
results_file_plus_english = detect_profanity(
    sample_text_for_file,
    language="English",
    custom_words_list=custom_words_from_file
)
# Detects "customfileword1" and "shit", Language: "Custom + English"
print(results_file_plus_english)

# Use file-loaded list ONLY
results_file_only = detect_profanity(
    sample_text_for_file,
    language=None, # Important: set language to None
    custom_words_list=custom_words_from_file
)
# Detects only "customfileword1", Language: "Custom"
print(results_file_only)
```

**Output Format for `detect_profanity`**

The `detect_profanity` function returns non-overlapping matches in text order. When two terms match at the same position, the longer one wins. Each dictionary includes:

- `"Line"`: The line number (1-indexed).
- `"Column"`: The column number (1-indexed) where the profanity starts.
- `"Word"`: The exact text that matched, with its original casing.
- `"Language"`: Indicates the source of the word list:
  - `<LanguageName>` (e.g., "English"): If only a built-in language list was used.
  - `"Custom"`: If `language=None` and only a `custom_words_list` was used.
  - `"Custom + <LanguageName>"` (e.g., "Custom + English"): If both a built-in list and `custom_words_list` were used.
  - `"Custom + All"`: If `language='All'` and `custom_words_list` were used.

**4. Removing Profanity**

`remove_profanity` works similarly, accepting `language` and `custom_words_list` parameters.

```python
from valx import remove_profanity, load_custom_profanity_from_file

sample_text = ["This is fuck, custombadword1, and text with customfileword1."]
my_custom_words = ["custombadword1"]
custom_words_from_file = load_custom_profanity_from_file("my_profanity_file.txt") # Assuming it contains 'customfileword1'

# Remove profanity using English built-in + my_custom_words + custom_words_from_file
all_custom_words = list(set(my_custom_words + custom_words_from_file)) # Combine and unique

cleaned_text = remove_profanity(
    sample_text,
    output_file="cleaned_output.txt", # Optional: saves to file
    language="English",
    custom_words_list=all_custom_words
)
# cleaned_text will have "fuck", "custombadword1", and "customfileword1" replaced with "bad word".
# e.g., ["This is bad word, bad word, and text with bad word."]
print(cleaned_text)
```

The `load_profanity_words` function (used internally) also accepts `language` and `custom_words_list` if you need direct access to the word lists.

### Detect and Remove Sensitive Information

```python
from valx import detect_sensitive_information, remove_sensitive_information

lines = ["Contact help@example.com or call (555) 123-4567."]
print(detect_sensitive_information(lines, info_type="email"))
# [(1, 8, 'Email', 'help@example.com')]

print(remove_sensitive_information(lines, info_type=["email", "phone"]))
# ['Contact [SENSITIVE] or call [SENSITIVE].']
```

Pass one type, a list of types, or omit `info_type` to scan for all types. Detection reports a one-based line number and a **zero-based** column. Removal merges overlapping matches before inserting `[SENSITIVE]`.

> [!IMPORTANT]
> These are pattern-based filters, not a guarantee of anonymization. They can miss sensitive values or flag ordinary text. For example, `file_path` looks for filenames with an extension and can miss filenames containing spaces. Review redacted text before sharing it.

### Detect Hate Speech And Offensive Language

```python
from valx import detect_hate_speech

# Detect hate speech or offensive language
outcome_of_detection = detect_hate_speech("You are stupid.")
```

> [!IMPORTANT]
> The model's possible outputs are:
>
> - `['Hate Speech']`: The text was flagged and contained hate speech.
> - `['Offensive Speech']`: The text was flagged and contained offensive speech.
> - `['No Hate and Offensive Speech']`: The text was not flagged for any hate speech or offensive speech.

> [!NOTE]
> See our [official documentation](https://infinitode-docs.gitbook.io/documentation/package-documentation/valx-package-documentation) for more examples on how to use **ValX**.

### Model compatibility

Only the hate-speech functions load the bundled scikit-learn models. Scikit-learn can warn when loading a model saved with a different version, and compatibility across versions is not guaranteed. If you use scikit-learn 1.2.2, use NumPy 1.x with it. The rule-based profanity and sensitive-information filters do not load either model.

## PyPI provenance

Releases published by the Trusted Publishing workflow attach a [PEP 740 publish attestation](https://docs.pypi.org/attestations/publish/v1/) to each distribution file. The [PyPI Security tab](https://pypi.org/project/valx/#security) shows the status and lets you inspect the wheel and source archive separately. Older uploads are not retroactively attested.

For setup and verification steps, see the [maintainer release guide](https://github.com/Infinitode/ValX/blob/main/CONTRIBUTING.md#releasing-to-pypi).

## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or want to contribute to ValX, please open an issue or submit a pull request on [GitHub](https://github.com/infinitode/valx).

## License

ValX is released under the terms of the **MIT License (Modified)**. Please see the [LICENSE](https://github.com/infinitode/valx/blob/main/LICENSE) file for the full text.

### Derived licenses

---

ValX uses data from this GitHub repository:
https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/
© 2012-2020 Shutterstock, Inc.

Creative Commons Attribution 4.0 International License:
https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/LICENSE

---

**Modified License Clause**

The modified license clause grants users the permission to make derivative works based on the ValX software. However, it requires any substantial changes to the software to be clearly distinguished from the original work and distributed under a different name.
