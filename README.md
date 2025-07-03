# ValX
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
[![Code Size](https://img.shields.io/github/languages/code-size/infinitode/valx)](https://github.com/infinitode/valx)
![Downloads](https://pepy.tech/badge/valx)
![License Compliance](https://img.shields.io/badge/license-compliance-brightgreen.svg)
![PyPI Version](https://img.shields.io/pypi/v/valx)

An open-source Python library for data cleaning tasks. It includes functions for profanity detection, and removal, and detection and removal of personal information. Also includes hate speech and offensive language detection and removal, using AI.

> [!IMPORTANT]
> If you are using `scikit-learn` versions older than version `1.3.0`, please also downgrade your version of `numpy` as stated below. Otherwise, you can continue to use your preferred version of `scikit-learn` without downgrading `numpy`.
>
> Please downgrade to `numpy` version `1.26.4`. Our ValX **DecisionTreeClassifier** AI model, relies on lower versions of `numpy`, because it was trained on these versions.
> For more information see: https://techoverflow.net/2024/07/23/how-to-fix-numpy-dtype-size-changed-may-indicate-binary-incompatibility-expected-96-from-c-header-got-88-from-pyobject/

> [!NOTE]
> ValX will automatically install a version of `scikit-learn` that is compatible with your device if you don't have one already.

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

ValX supports the following Python versions:

- Python 3.6
- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11/Later (Preferred)

Please ensure that you have one of these Python versions installed before using ValX. ValX may not work as expected on lower versions of Python than the supported.

## Features

- **Profanity Detection**: Detect profane and NSFW words or terms.
- **Remove Profanity**: Remove profane and NSFW words or terms.
- **Detect Sensitive Information**: Detect sensitive information in text data.
- **Remove Sensitive Information**: Remove sensitive information from text data.
- **Detect Hate Speech**: Detect hate speech or offensive speech in text, using AI.
- **Remove Hate Speech**: Remove hate speech or offensive speech in text, using AI.

### List of supported languages for profanity detection and removal
Below is a complete list of all the available supported languages for ValX's profanity detection and removal functions which are valid values for `language`:

- **All**
- Arabic
- Czech
- Danish
- German
- English
- Esperanto
- Persian
- Finnish
- Filipino
- French
- French (CA)
- Hindi
- Hungarian
- Italian
- Japanese
- Kabyle
- Korean
- Dutch
- Norwegian
- Polish
- Portuguese
- Russian
- Swedish
- Thai
- Klingon
- Turkish
- Chinese

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
#   {'Line': 1, 'Column': 43, 'Word': 'asshole', 'Language': 'Custom + English'}
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

The `detect_profanity` function returns a list of dictionaries. Each dictionary includes:
- `"Line"`: The line number (1-indexed).
- `"Column"`: The column number (1-indexed) where the profanity starts.
- `"Word"`: The detected profanity word.
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

### Detect Sensitive Information

```python
from valx import detect_sensitive_information

# Detect sensitive information
detected_sensitive_info = detect_sensitive_information(sample_text)
```

> [!NOTE]
> We have updated this function, and it now includes an optional argument for `info_type`, which can be used to detect only specific types of sensitive information. It was also added to `remove_sensitive_information`.

### Remove Sensitive Information

```python
from valx import remove_sensitive_information

# Remove sensitive information
cleaned_text = remove_sensitive_information(sample_text2)
```

### Detect Hate Speech And Offensive Language

```python
from valx import detect_hate_speech

# Detect hate speech or offensive language
outcome_of_detection = detect_hate_speech("You are stupid.")
```

> [!IMPORTANT]
> The model's possible outputs are:
> - `['Hate Speech']`: The text was flagged and contained hate speech.
> - `['Offensive Speech']`: The text was flagged and contained offensive speech.
> - `['No Hate and Offensive Speech']`: The text was not flagged for any hate speech or offensive speech.

> [!NOTE]
> See our [official documentation](https://infinitode-docs.gitbook.io/documentation/package-documentation/valx-package-documentation) for more examples on how to use **ValX**.

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
