# ValX
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
[![Code Size](https://img.shields.io/github/languages/code-size/infinitode/valx)](https://github.com/infinitode/valx)
![Downloads](https://pepy.tech/badge/valx)
![License Compliance](https://img.shields.io/badge/license-compliance-brightgreen.svg)
![PyPI Version](https://img.shields.io/pypi/v/valx)

An open-source Python library for data cleaning tasks. Includes profanity detection, and removal. It also now provides detection and removal of personal information. Now includes hate speech and offensive language detection using AI.

> [!IMPORTANT]
> Please downgrade to `numpy` version `1.26.4`. Our ValX **DecisionTreeClassifier** AI model, relies on lower versions of `numpy`, because it was trained on these versions.
> For more information see: https://techoverflow.net/2024/07/23/how-to-fix-numpy-dtype-size-changed-may-indicate-binary-incompatibility-expected-96-from-c-header-got-88-from-pyobject/

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

### Detect Profanity

```python
from valx import detect_profanity

# Detect profanity
results = detect_profanity(sample_text, language='English')
print("Profanity Evaluation Results", results)
```

### Remove Profanity

```python
from valx import remove_profanity

# Remove profanity
removed = remove_profanity(sample_text, "text_cleaned.txt", language="English")
```

### Detect Sensitive Information

```python
from valx import detect_sensitive_information

# Detect sensitive information
detected_sensitive_info = detect_sensitive_information(sample_text)
```

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
