import os
import re

'''
ValX uses data from this GitHub repository:
https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/
© 2012-2020 Shutterstock, Inc.

Creative Commons Attribution 4.0 International License:
https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/LICENSE
'''


def load_profanity_words(language='English'):
    """
    Load profanity words from the local text file.

    Args:
        language (str): The language for which to load profanity words. Defaults to 'English'.

    Returns:
        list: A list of profanity words for the specified language, or all languages if 'All' is specified.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'profanity_words.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            profanity_lists = {}
            current_language = None
            current_words = []
            for line in file:
                line = line.strip()
                if line.startswith("$") and line.endswith("$"):
                    if current_language:
                        profanity_lists[current_language] = current_words
                        current_words = []
                    current_language = line.strip("$")
                else:
                    current_words.append(line)
            if current_language:
                profanity_lists[current_language] = current_words

            if language == 'All':
                all_profanity_words = []
                for words in profanity_lists.values():
                    all_profanity_words.extend(words)
                return all_profanity_words
            else:
                return profanity_lists.get(language, [])
    except FileNotFoundError:
        print("Failed to load profanity words file. Using default list.")
        return [
            'profane_word1',
            'profane_word2',
            'profane_word3'
        ]


def detect_profanity(text_data, language='English', allowed_languages=None):
    """
    Detect profanity in text data using regex.

    Args:
        text_data (list): A list of strings representing the text data to analyze.
        language (str): The language for which to detect profanity. Defaults to 'English'.
        allowed_languages (list): A list of languages to allow for detection. If provided, only profanity words for these languages will be considered.

    Returns:
        int: The total number of profanity detections.
    """
    profanity_keywords = load_profanity_words(language)
    detected = set()  # Use a set to store unique occurrences

    for i, line in enumerate(text_data):
        # Skip lines with language markers
        if line.startswith("$") and line.endswith("$"):
            continue

        # Detect profanity
        for profanity in profanity_keywords:
            matches = re.finditer(r'\b{}\b'.format(re.escape(profanity)), line, flags=re.IGNORECASE)
            for match in matches:
                detected.add((i + 1, match.start() + 1, language, profanity))  # Add to set

    if detected:
        print(f"Profanity detected:")
        for line_num, col_num, lang, word in detected:
            print(f"Language: {lang}, Line {line_num}, Column {col_num}: '{word}'")

    return len(detected)


def remove_profanity(text_data, output_file=None, language='English'):
    """
    Remove profanity from text data.

    Args:
        text_data (list): A list of strings representing the text data to clean.
        output_file (str): The file path to write the cleaned data. If None, cleaned data is not written to a file.
        language (str): The language for which to remove profanity. Defaults to 'English'.

    Returns:
        list: A list of strings representing the cleaned text data.
    """
    profanity_keywords = load_profanity_words(language)
    cleaned_data = []

    for line in text_data:
        # Skip lines with language markers
        if line.startswith("$") and line.endswith("$"):
            continue

        # Remove profanity
        cleaned_line = line
        for profanity in profanity_keywords:
            cleaned_line = re.sub(r'\b{}\b'.format(re.escape(profanity)), 'bad word', cleaned_line, flags=re.IGNORECASE)
        cleaned_data.append(cleaned_line)

    # Write cleaned data to output file if provided
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(cleaned_data))

    return cleaned_data
