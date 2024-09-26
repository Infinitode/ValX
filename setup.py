from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='valx',
    version='{{VERSION_PLACEHOLDER}}',
    author='Infinitode Pty Ltd',
    author_email='infinitode.ltd@gmail.com',
    description='An open-source Python library for data cleaning tasks. Includes profanity detection, and removal. Now includes offensive language and hate speech detection using an AI model.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/infinitode/valx',
    packages=find_packages(),
    package_data={'valx': ['models/*']},
    install_requires=[
        'scikit-learn==1.2.2'  # for the AI to function properly
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
)
