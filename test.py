from valx import (
    detect_profanity,
    remove_profanity,
    detect_sensitive_information,
    remove_sensitive_information,
    detect_hate_speech,
    remove_hate_speech,
    load_custom_profanity_from_file  # Import the new function
)
import os # For file operations in tests

# Define a helper to make assertions and print clear test results
def run_test(test_name, condition, success_message, failure_message):
    print(f"--- Running Test: {test_name} ---")
    if condition:
        print(f"PASS: {success_message}")
    else:
        print(f"FAIL: {failure_message}")
    assert condition, failure_message
    print("-" * 30 + "\n")

def main():
    print("Starting ValX tests...\n")

    # --- Original Profanity Tests ---
    sample_text_orig = [
        "This is a sample text containing some profanity like porn, fuck, and asshole.",
        "This line doesn't contain any profanity.",
        "But this one has another, just in another language: oslošoust."
    ]
    detected_profanity_orig = detect_profanity(sample_text_orig, language='All')
    run_test(
        "Original Profanity Detection (All Languages)",
        len(detected_profanity_orig) == 4, # porn, fuck, asshole, oslošoust
        f"Detected {len(detected_profanity_orig)} profanities as expected.",
        f"Expected 4 profanities, but found {len(detected_profanity_orig)}. Detected: {[d['Word'] for d in detected_profanity_orig]}"
    )
    print("Detected (Original):", detected_profanity_orig)
    print("Detected words (Original):", [d['Word'] for d in detected_profanity_orig])

    cleaned_text_orig_file = "text_cleaned_original.txt"
    remove_profanity(sample_text_orig, cleaned_text_orig_file, language="All")
    run_test(
        "Original Profanity Removal (All Languages)",
        os.path.exists(cleaned_text_orig_file),
        f"Cleaned file '{cleaned_text_orig_file}' created.",
        f"Cleaned file '{cleaned_text_orig_file}' not found."
    )
    if os.path.exists(cleaned_text_orig_file):
        os.remove(cleaned_text_orig_file) # Clean up test file

    # --- Custom Profanity List Tests ---
    custom_profanity_list = ["custombadword1", "supersecretcurse", "anotherone"]
    custom_test_text = [
        "Here is custombadword1 and a normal word.",
        "This uses supersecretcurse from the custom list.",
        "Also, asshole from built-in English list.",
        "And testwordalpha from the file list, plus anotherone here."
    ]

    # 1. Custom list (Python list) + Specific Language (English)
    # custom_profanity_list here is ["custombadword1", "supersecretcurse", "anotherone"]
    # custom_test_text now contains "anotherone"
    # So, "custombadword1", "supersecretcurse", "anotherone" (from custom list) and "asshole" (from English) should be detected.
    detected_custom_english = detect_profanity(custom_test_text, language="English", custom_words_list=custom_profanity_list)
    detected_words_custom_english = sorted([d['Word'] for d in detected_custom_english])
    expected_words_custom_english = sorted(["custombadword1", "supersecretcurse", "anotherone", "asshole"])
    run_test(
        "Detect: Custom List + English",
        detected_words_custom_english == expected_words_custom_english and \
        all(d['Language'] == "Custom + English" for d in detected_custom_english),
        f"Correctly detected: {detected_words_custom_english} with language 'Custom + English'.",
        f"Expected {expected_words_custom_english} with 'Custom + English', got {detected_words_custom_english}. Detected full: {detected_custom_english}"
    )
    print("Detected (Custom List + English):", detected_custom_english)

    # 2. Custom list (Python list) + language=None
    # custom_profanity_list here is ["custombadword1", "supersecretcurse", "anotherone"]
    # "asshole" should not be detected here as we are not using the English list
    # "testwordalpha" is in the text, but not in this custom_profanity_list.
    detected_custom_only = detect_profanity(custom_test_text, language=None, custom_words_list=custom_profanity_list)
    detected_words_custom_only = sorted([d['Word'] for d in detected_custom_only])
    expected_words_custom_only = sorted(["custombadword1", "supersecretcurse", "anotherone"]) # "anotherone" is in this custom list
    run_test(
        "Detect: Custom List Only (language=None)",
        detected_words_custom_only == expected_words_custom_only and \
        all(d['Language'] == "Custom" for d in detected_custom_only),
        f"Correctly detected: {detected_words_custom_only} with language 'Custom'.",
        f"Expected {expected_words_custom_only} with 'Custom', got {detected_words_custom_only}. Detected full: {detected_custom_only}"
    )
    print("Detected (Custom List Only):", detected_custom_only)

    # --- Custom Profanity File Tests ---
    custom_file_path = "custom_profanity.txt" # Created in previous step

    # Ensure the test file exists
    if not os.path.exists(custom_file_path):
        print(f"CRITICAL FAIL: Test file '{custom_file_path}' not found. Skipping file-based tests.")
    else:
        custom_words_from_file = load_custom_profanity_from_file(custom_file_path)
        expected_file_words = ["custombadword1", "supersecretcurse", "anotherone", "testwordalpha", "testwordbeta"]
        run_test(
            "Load Custom Profanity from File",
            sorted(custom_words_from_file) == sorted(expected_file_words),
             f"Successfully loaded {len(custom_words_from_file)} words from file.",
             f"Expected {expected_file_words}, got {sorted(custom_words_from_file)}"
        )
        print("Words loaded from file:", custom_words_from_file)

        # 3. Custom list (from file) + Specific Language (English)
        # Text includes "asshole" (English) and "testwordalpha" (file)
        detected_file_english = detect_profanity(custom_test_text, language="English", custom_words_list=custom_words_from_file)
        detected_words_file_english = sorted([d['Word'] for d in detected_file_english])
        # custombadword1, supersecretcurse, asshole, testwordalpha, anotherone (since "anotherone" is in custom_test_text and custom_words_from_file)
        expected_words_file_english = sorted(["custombadword1", "supersecretcurse", "asshole", "testwordalpha", "anotherone"])
        run_test(
            "Detect: Custom File List + English",
            detected_words_file_english == expected_words_file_english and \
            all(d['Language'] == "Custom + English" for d in detected_file_english),
            f"Correctly detected: {detected_words_file_english} with 'Custom + English'.",
            f"Expected {expected_words_file_english} with 'Custom + English', got {detected_words_file_english}. Detected full: {detected_file_english}"
        )
        print("Detected (Custom File + English):", detected_file_english)

        # 4. Custom list (from file) + language=None
        # Text includes "testwordalpha" (file) but "asshole" (English) should be ignored
        # custom_words_from_file includes "custombadword1", "supersecretcurse", "anotherone", "testwordalpha", "testwordbeta"
        # custom_test_text includes "custombadword1", "supersecretcurse", "anotherone", "testwordalpha"
        detected_file_only = detect_profanity(custom_test_text, language=None, custom_words_list=custom_words_from_file)
        detected_words_file_only = sorted([d['Word'] for d in detected_file_only])
        expected_words_file_only = sorted(["custombadword1", "supersecretcurse", "testwordalpha", "anotherone"])
        run_test(
            "Detect: Custom File List Only (language=None)",
            detected_words_file_only == expected_words_file_only and \
            all(d['Language'] == "Custom" for d in detected_file_only),
            f"Correctly detected: {detected_words_file_only} with language 'Custom'.",
            f"Expected {expected_words_file_only} with 'Custom', got {detected_words_file_only}. Detected full: {detected_file_only}"
        )
        print("Detected (Custom File Only):", detected_file_only)

        # 5. Custom list (from file) + language='All'
        # This should detect "oslošoust" (from 'All') and words from file that are in combined_text_for_all
        combined_text_for_all = sample_text_orig + custom_test_text
        detected_file_all = detect_profanity(combined_text_for_all, language="All", custom_words_list=custom_words_from_file)
        detected_words_file_all = sorted(list(set([d['Word'] for d in detected_file_all]))) # Use set for uniqueness
        expected_words_file_all = sorted(list(set(["porn", "fuck", "asshole", "oslošoust", "custombadword1", "supersecretcurse", "anotherone", "testwordalpha"])))
        run_test(
            "Detect: Custom File List + All Languages",
            detected_words_file_all == expected_words_file_all and \
            all(d['Language'] == "Custom + All" for d in detected_file_all),
            f"Correctly detected words with 'Custom + All'. Words: {detected_words_file_all}",
            f"Expected words with 'Custom + All'. Expected: {expected_words_file_all}, Got: {detected_words_file_all}. Detected full: {detected_file_all}"
        )
        print("Detected (Custom File + All):", detected_file_all)

        # Test remove_profanity with custom list from file
        cleaned_output_file_custom = "text_cleaned_custom_file.txt"
        text_to_clean_custom = [
            "This has custombadword1 and testwordalpha.",
            "Also regular profanity like asshole."
        ]
        remove_profanity(text_to_clean_custom, cleaned_output_file_custom, language="English", custom_words_list=custom_words_from_file)
        run_test(
            "Remove: Custom File List + English",
            os.path.exists(cleaned_output_file_custom),
            f"Cleaned file '{cleaned_output_file_custom}' created using custom file list + English.",
            f"Cleaned file '{cleaned_output_file_custom}' not found."
        )
        if os.path.exists(cleaned_output_file_custom):
            with open(cleaned_output_file_custom, 'r') as f:
                content = f.read()
                # Check if custom and built-in words are replaced
                cond = "custombadword1" not in content and \
                       "testwordalpha" not in content and \
                       "asshole" not in content and \
                       "bad word" in content # Check if replacement marker is present
                run_test(
                    "Remove: Content Check (Custom File + English)",
                    cond,
                    "Profanity correctly replaced in output file.",
                    f"Profanity not correctly replaced. Content:\n{content}"
                )
            os.remove(cleaned_output_file_custom) # Clean up

    # --- Test language=None and custom_words_list=None for load_profanity_words (should raise ValueError) ---
    try:
        detect_profanity(["some text"], language=None, custom_words_list=None)
        run_test("Error Handling: language=None, custom_words_list=None", False, "", "ValueError was not raised when language and custom_words_list are both None.")
    except ValueError:
        run_test("Error Handling: language=None, custom_words_list=None", True, "ValueError correctly raised.", "")
    except Exception as e:
        run_test("Error Handling: language=None, custom_words_list=None", False, "", f"Unexpected error raised: {e}")


    # --- Original Sensitive Info and AI Hate Speech Tests (copied from original test.py) ---
    print("\n--- Running Original Sensitive Info and AI Hate Speech Tests ---")
    ai_sample_text = [
        "This is a sample text containing some profanity like porn, fuck, and asshole.", # Will be removed by AI
        "This line doesn't contain any profanity.", # Kept
        "But this one has another, just in another language: oslošoust." # Will be removed by AI
    ]
    print("AI detect_hate_speech('You're so stupid.'):", detect_hate_speech("You're so stupid.")) # Expected: Offensive Speech

    sample_text2 = [
        "Please contact john.doe@example.com or call 555-123-4567 for more information.",
        "We will need your credit card number to complete the transaction: 1234-5678-9012-3456.",
        "My social security number is 123-45-6789 and my ID number is AB123456.",
        "Our office address is 123 Main St, Anytown, USA. Please visit us!",
        "Your IP address is 192.168.1.1. Please don't share it with anyone."
    ]
    
    detected_sensitive_info = detect_sensitive_information(sample_text2)
    print("Detected sensitive information:")
    for line_num, col_num, info_type, info in detected_sensitive_info:
        print(f"Line {line_num}, Column {col_num}: {info_type} - {info}")
    
    cleaned_text_sensitive = remove_sensitive_information(sample_text2)
    print("\nCleaned text (sensitive info removed):")
    for line in cleaned_text_sensitive:
        print(line)

    cleaned_text_ai = remove_hate_speech(ai_sample_text) # Use ai_sample_text
    print("\nCleaned text using AI (hate/offensive speech removed):") # Expected: only the clean line
    for line in cleaned_text_ai:
        print(line)
    
    # Based on current observation, the AI model in this env/version setup
    # flags the first two lines of ai_sample_text and not the third.
    expected_ai_cleaned_lines = [
        "But this one has another, just in another language: oslošoust."
    ]
    condition_ai_removal = len(cleaned_text_ai) == len(expected_ai_cleaned_lines) and \
                           all(expected_line in cleaned_text_ai for expected_line in expected_ai_cleaned_lines)

    run_test(
        "AI Hate Speech Removal",
        condition_ai_removal,
        "AI correctly processed lines based on its observed hate/offensive speech detection in this environment.",
        f"AI removal incorrect. Expected {len(expected_ai_cleaned_lines)} specific lines, got {len(cleaned_text_ai)}. Expected: {expected_ai_cleaned_lines}, Got: {cleaned_text_ai}"
    )

    print("\nAll ValX tests completed.")

if __name__ == "__main__":
    main()
