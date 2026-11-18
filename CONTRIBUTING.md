# Contributing to ValX

Thank you for considering contributing to **ValX**! Contributions, whether they are bug fixes, new features, or improvements to the documentation, are always welcome. Before contributing, please read the following guidelines to ensure smooth collaboration.

## Getting Started

1. **Fork the Repository**  
   Create a fork of this repository to your GitHub account and clone it locally.

2. **Set Up the Environment**  
   Use Python 3.9 or newer. In a virtual environment, install ValX for development and run its tests:

   ```bash
   python -m pip install -r requirements.txt
   python -m unittest discover -v
   ```

## How to Contribute

1. **Report Issues**  
   Use the [GitHub Issues page](https://github.com/Infinitode/ValX/issues) to report bugs or suggest features. Please include:
   - A clear description of the issue or suggestion.
   - Steps to reproduce (for bugs).

2. **Make Changes**  
   - Use clear and descriptive commit messages.
   - Add regression tests for bug fixes and tests for new behavior.
   - Ensure the code is **readable**. You can learn more about Python code readability here: https://peps.python.org/pep-0008/.

3. **Submit a Pull Request**  
   - Push your changes to a feature branch in your fork.
   - Submit a pull request with a detailed explanation of what you've changed or added.
   - Ensure your PR passes all automated tests and adheres to the contribution guidelines.

## Releasing to PyPI

Register a GitHub Actions Trusted Publisher under **Publishing** in [ValX's PyPI project settings](https://pypi.org/manage/projects/):

| PyPI field | Value |
| --- | --- |
| Owner | `Infinitode` |
| Repository name | `ValX` |
| Workflow name | `build_and_publish.yml` |
| Environment name | **Leave blank** (do not enter `None` or `pypi`) |

The publish job deliberately has no GitHub environment and uses OIDC rather than a `PYPI_API_TOKEN`. Limit who can create or change release tags with a GitHub tag ruleset, since there is no environment approval gate.

1. Set the version in `pyproject.toml`, update the README change notes, and merge the reviewed changes.
2. Tag the merged commit and push the tag, for example `git tag v0.2.7` followed by `git push origin v0.2.7`. Use a final `X.Y.Z` or `vX.Y.Z` tag matching the package version.
3. Once the workflow succeeds, open the release's **Security** tab on PyPI. Confirm there is a publish attestation for both the wheel and the source distribution from `Infinitode/ValX` and `build_and_publish.yml`. Avoid separate manual uploads, which would not inherit those attestations.

To verify the signatures against this repository, use `pypi-attestations` after the release is live (substitute the actual version):

```bash
python -m pip install pypi-attestations
pypi-attestations verify pypi --repository https://github.com/Infinitode/ValX pypi:valx-0.2.7-py3-none-any.whl
pypi-attestations verify pypi --repository https://github.com/Infinitode/ValX pypi:valx-0.2.7.tar.gz
```

After the first verified OIDC release, remove the unused `PYPI_API_TOKEN` secret from GitHub and revoke the old token on PyPI if nothing else uses it.

## Community Guidelines

To maintain a positive and collaborative community, we ask that all contributors adhere to the following principles:

1. **Be Respectful**  
   Treat others with respect, regardless of their background or expertise. 

2. **Provide Constructive Feedback**  
   Offer helpful and actionable suggestions during code reviews.

3. **Follow Licensing Requirements**  
   Ensure that any derivative works comply with the [license](https://github.com/infinitode/ValX/blob/main/LICENSE).

By contributing, you agree to abide by these guidelines and this project's [license](https://github.com/infinitode/ValX/blob/main/LICENSE). Thank you for helping make **ValX** better!
