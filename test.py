from valx import load_profanity_words, detect_profanity, remove_profanity, detect_sensitive_information, remove_sensitive_information

def main():
    sample_text = [
        "This is a sample text containing some profanity like porn, fuck, and asshole.",
        "This line doesn't contain any profanity.",
        "But this one has another, just in another language: oslošoust."
    ]

    # Detect profanity
    num_profanities = detect_profanity(sample_text, language='All')

    print(f"Number of profanities detected: {num_profanities}")

    removed = remove_profanity(sample_text, "text_cleaned.txt", language="All")


    # Example usage:
    sample_text2 = [
        "Please contact john.doe@example.com or call 555-123-4567 for more information.",
        "We will need your credit card number to complete the transaction: 1234-5678-9012-3456.",
        "My social security number is 123-45-6789 and my ID number is AB123456.",
        "Our office address is 123 Main St, Anytown, USA. Please visit us!",
        "Your IP address is 192.168.1.1. Please don't share it with anyone."
    ]
    
    # Detect sensitive information
    detected_sensitive_info = detect_sensitive_information(sample_text2)
    print("Detected sensitive information:")
    for line_num, col_num, info_type, info in detected_sensitive_info:
        print(f"Line {line_num}, Column {col_num}: {info_type} - {info}")
    
    # Remove sensitive information
    cleaned_text = remove_sensitive_information(sample_text2)
    print("\nCleaned text:")
    for line in cleaned_text:
        print(line)
    
if __name__ == "__main__":
    main()
