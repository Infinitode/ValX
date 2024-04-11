from valx import load_profanity_words, detect_profanity, remove_profanity

def main():
    sample_text = [
        "This is a sample text containing some profanity like porn, fuck, and asshole.",
        "This line doesn't contain any profanity.",
        "But this one has another, just in another language: oslošoust."
    ]

    # Detect profanity
    num_profanities = detect_profanity(sample_text, language='English')

    print(f"Number of profanities detected: {num_profanities}")

    removed = remove_profanity(sample_text, "text_cleaned.txt", language="English")

if __name__ == "__main__":
    main()
