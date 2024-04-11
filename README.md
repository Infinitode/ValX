# ValX
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
[![Code Size](https://img.shields.io/github/languages/code-size/infinitode/valx)](https://github.com/infinitode/valx)
![Downloads](https://pepy.tech/badge/valx)
![License Compliance](https://img.shields.io/badge/license-compliance-brightgreen.svg)
![PyPI Version](https://img.shields.io/pypi/v/valx)

An open-source Python library for data cleaning tasks. Includes profanity detection, and removal.

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

## Usage

### Detect Profanity

```python
from valx import detect_profanity

# Detect profanity
num_profanities = detect_profanity(sample_text, language='English')
```

### Remove Profanity

```python
from valx import remove_profanity

# Remove profanity
removed = remove_profanity(sample_text, "text_cleaned.txt", language="English")
```

## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or want to contribute to ValX, please open an issue or submit a pull request on [GitHub](https://github.com/infinitode/valx).

## License

PyWebScrapr is released under the terms of the **MIT License (Modified)**. Please see the [LICENSE](https://github.com/infinitode/pywebscrapr/blob/main/LICENSE) file for the full text.

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
