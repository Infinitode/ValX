import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import valx


class ProfanityTests(unittest.TestCase):
    def test_language_names_and_codes_are_case_insensitive(self):
        for language, word in (
            ("enGliSh", "porn"), ("eN", "porn"), ("ES", "gilipollas"),
            ("Finnish", "perkele"), ("fI", "perkele"),
        ):
            with self.subTest(language=language):
                self.assertEqual(
                    valx.detect_profanity([word], language),
                    [{"Line": 1, "Column": 1, "Word": word, "Language": language}],
                )

    def test_all_languages(self):
        lines = ["Some words: porn, asshole.", "Another language: oslošoust."]
        matches = valx.detect_profanity(lines, "All")
        self.assertEqual([match["Word"] for match in matches], ["porn", "asshole", "oslošoust"])
        self.assertEqual(
            valx.remove_profanity(lines, language="All"),
            ["Some words: bad word, bad word.", "Another language: bad word."],
        )

    def test_custom_lists_alone_or_combined(self):
        lines = ["Before BLOCKED and porn.", "blocked again, unblocked is fine."]
        words = [" blocked ", "blocked"]
        for language, label, expected in (
            (None, "Custom", [(1, 8, "BLOCKED"), (2, 1, "blocked")]),
            ("EN", "Custom + EN", [(1, 8, "BLOCKED"), (1, 20, "porn"), (2, 1, "blocked")]),
            ("All", "Custom + All", [(1, 8, "BLOCKED"), (1, 20, "porn"), (2, 1, "blocked")]),
        ):
            with self.subTest(language=language):
                self.assertEqual(
                    valx.detect_profanity(lines, language, words),
                    [dict(Line=line, Column=col, Word=word, Language=label)
                     for line, col, word in expected],
                )

    def test_punctuation_and_longest_match(self):
        lines = ["dummy phrase, #TAG, C++ and C++17."]
        words = ["dummy", "dummy phrase", "#tag", "C++", "word"]
        matches = valx.detect_profanity(lines, None, words)
        self.assertEqual([match["Word"] for match in matches], ["dummy phrase", "#TAG", "C++"])
        self.assertEqual(
            valx.remove_profanity(lines, language=None, custom_words_list=words),
            ["bad word, bad word, bad word and C++17."],
        )

    def test_dollar_delimited_input_is_not_dropped(self):
        lines = ["$notes$", "$blocked$", ""]
        words = ["blocked"]
        self.assertEqual(
            valx.detect_profanity(lines, None, words),
            [{"Line": 2, "Column": 2, "Word": "blocked", "Language": "Custom"}],
        )
        self.assertEqual(
            valx.remove_profanity(lines, language=None, custom_words_list=words),
            ["$notes$", "$bad word$", ""],
        )

    def test_custom_wordlist_validation(self):
        for words in (None, [], ["", "  "]):
            with self.subTest(words=words), self.assertRaises(ValueError):
                valx.load_profanity_words(None, words)
        self.assertEqual(valx.detect_profanity(["hello"], custom_words_list=[""]), [])
        with self.assertRaises(TypeError):
            valx.load_profanity_words(None, "blocked")

    def test_returned_wordlist_can_be_modified_without_affecting_other_calls(self):
        words = valx.load_profanity_words("FI")
        self.assertIn("perkele", words)
        words.clear()
        self.assertIn("perkele", valx.load_profanity_words("Finnish"))

    def test_load_custom_file_and_write_cleaned_text(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "custom.txt"
            source.write_text("# comment\n\n  café\n  # other comment\n  two words\n", encoding="utf-8-sig")
            words = valx.load_custom_profanity_from_file(source)
            self.assertEqual(words, ["café", "two words"])
            output = Path(temp) / "cleaned.txt"
            self.assertEqual(valx.remove_profanity(["CAFÉ!"], output, None, words), ["bad word!"])
            self.assertEqual(output.read_text(encoding="utf-8"), "bad word!")
            with self.assertRaises(FileNotFoundError):
                valx.load_custom_profanity_from_file(Path(temp) / "missing.txt")


class SensitiveInformationTests(unittest.TestCase):
    def test_detect_specific_type_and_preserve_zero_based_column(self):
        self.assertEqual(
            valx.detect_sensitive_information(["No contact", "Contact x@example.com or (555) 123-4567."], "email"),
            [(2, 8, "Email", "x@example.com")],
        )

    def test_phone_with_parentheses_is_fully_redacted(self):
        lines = ["Call (555) 123-4567.", "Call(555) 123-4567."]
        self.assertEqual(
            valx.detect_sensitive_information(lines, "phone"),
            [(1, 5, "Phone", "(555) 123-4567"), (2, 4, "Phone", "(555) 123-4567")],
        )
        self.assertEqual(
            valx.remove_sensitive_information(lines, info_type="phone"),
            ["Call [SENSITIVE].", "Call[SENSITIVE]."],
        )

    def test_negative_coordinates_include_the_sign(self):
        lines = ["Site: -25.7, +28.2."]
        self.assertEqual(valx.detect_sensitive_information(lines, "geo_coords"), [(1, 6, "Geo_coords", "-25.7, +28.2")])
        self.assertEqual(valx.remove_sensitive_information(lines, info_type="geo_coords"), ["Site: [SENSITIVE]."])
        self.assertEqual(valx.detect_sensitive_information(["91.1, 18", "25, 180.1"], "geo_coords"), [])

    def test_redacts_only_matched_spans_even_with_an_iterator(self):
        lines = ["ID 123-45-6789, not X123-45-6789Y.", "X123-45-6789Y", "123-45-6789"]
        expected = ["ID [SENSITIVE], not X123-45-6789Y.", "X123-45-6789Y", "[SENSITIVE]"]
        for text_data in (lines, iter(lines)):
            self.assertEqual(valx.remove_sensitive_information(text_data, info_type="ssn"), expected)

    def test_overlapping_matches_are_redacted_once_in_either_type_order(self):
        for info_type in (["username", "email"], ["email", "username"]):
            with self.subTest(info_type=info_type):
                self.assertEqual(
                    valx.remove_sensitive_information(["Mail me@example.com or ping @help."], info_type=info_type),
                    ["Mail [SENSITIVE] or ping [SENSITIVE]."],
                )

    def test_partly_overlapping_matches_redact_their_union(self):
        self.assertEqual(
            valx.remove_sensitive_information(["1234 5678 9012 345 678 9012"], info_type=["credit_card", "phone"]),
            ["[SENSITIVE]"],
        )

    def test_default_patterns_do_not_treat_email_parts_as_file_paths(self):
        lines = ["Mail first.last@example.com, then call (555) 123-4567."]
        self.assertEqual(valx.detect_sensitive_information(lines, "file_path"), [])
        self.assertEqual(valx.remove_sensitive_information(lines), ["Mail [SENSITIVE], then call [SENSITIVE]."])

    def test_file_paths_and_output_file(self):
        lines = [r"Open /var/log/app.log and C:\Program Files\Reports\report.txt or report.csv."]
        expected = ["Open [SENSITIVE] and [SENSITIVE] or [SENSITIVE]."]
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "redacted.txt"
            self.assertEqual(valx.remove_sensitive_information(lines, output, "file_path"), expected)
            self.assertEqual(output.read_text(encoding="utf-8"), expected[0])


class HateSpeechTests(unittest.TestCase):
    def test_text_filters_do_not_import_sklearn(self):
        subprocess.run(
            [sys.executable, "-c", "import sys, valx; valx.detect_profanity(['hello']); "
             "assert 'sklearn' not in sys.modules"],
            cwd=Path(valx.__file__).resolve().parent.parent,
            check=True,
        )

    def test_bundled_model_prediction_and_filtering(self):
        offensive = "You're so stupid."
        clean = "Good morning, have a nice day."
        self.assertEqual(valx.detect_hate_speech(offensive).tolist(), ["Offensive Speech"])
        self.assertEqual(valx.detect_hate_speech(clean).tolist(), ["No Hate and Offensive Speech"])
        self.assertEqual(valx.remove_hate_speech([offensive, clean]), [clean])
        self.assertEqual(valx.remove_hate_speech([]), [])


if __name__ == "__main__":
    unittest.main()
