
"""
Program: Text Anagram and Pattern Matcher Tool
Author: Saurav 241492

Description:
Identifies anagrams by normalizing text and comparing sorted characters.
Uses dictionaries and tuple keys to group words with matching patterns.

Input: Words or textual phrases.
Output: Anagram status and groups of matching anagrams.
"""

from typing import List, Dict, Tuple
from collections import defaultdict


# Function to normalize text
def clean_text(text: str) -> str:
    return "".join(
        filter(str.isalnum, text.lower())
    )


# Function to check whether two texts are anagrams
def are_anagrams(text1: str, text2: str) -> bool:
    return sorted(clean_text(text1)) == sorted(clean_text(text2))


# Function to group anagrams using tuple keys
def group_anagrams(words: List[str]) -> Dict[Tuple[str, ...], List[str]]:
    groups = defaultdict(list)

    for word in words:
        key = tuple(sorted(clean_text(word)))
        groups[key].append(word)

    return dict(groups)


# Main program
if __name__ == "__main__":
    text1 = input("Enter first word or phrase: ")
    text2 = input("Enter second word or phrase: ")

    if are_anagrams(text1, text2):
        print("The texts are anagrams.")
    else:
        print("The texts are not anagrams.")

    words = ["listen", "silent", "enlist", "hello", "below", "elbow"]

    print("\nOriginal Words:", words)
    print("Anagram Groups:")

    for group in group_anagrams(words).values():
        print(group)