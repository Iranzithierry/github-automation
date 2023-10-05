import sys
import re

def remove_words_in_brackets(text):
    brackets_pattern = r"\s*\(https:[^)]*\)"

    text_without_brackets = re.sub(brackets_pattern, "", text)

    return text_without_brackets

remove = remove_words_in_brackets("""""")
print(remove)