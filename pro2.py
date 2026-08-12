import string
def analyze_text(text):
    text = text.lower()
    # Remove punctuation such as . , ! ? : ; etc.
    text = text.translate(str.maketrans("", "", string.punctuation))
    # split() automatically removes extra spaces, tabs and newlines
    words = text.split()
    total_words = len(words)
    # Create a frequency table using a dictionary.
    frequency = {}
    for word in words:
        # If the word already exists, increase its count.
        # Otherwise, start its count at 1.
        frequency[word] = frequency.get(word, 0) + 1
    palindromes = []
    for word in frequency:
        # A palindrome reads the same forwards and backwards.
        if len(word) > 1 and word == word[::-1]:
            palindromes.append(word)
    return total_words, frequency, palindromes

choice = input("Enter F to read a file or M for multiline text: ").upper()
if choice == "F":
    filename = input("Enter the file name: ")
    try:
        # encoding="utf-8" allows normal text files with common characters.
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
        total_words, frequency, palindromes = analyze_text(text)

    except FileNotFoundError:
        print("Error: File not found.")
        exit()
elif choice == "M":
    print("Enter your text.")
    print("Type END on a separate line to finish:")
    lines = []
    while True:
        line = input()
        # END tells the program that multiline input is complete.
        if line == "END":
            break
        lines.append(line)
    # join() combines all entered lines into one string.
    text = "\n".join(lines)
    total_words, frequency, palindromes = analyze_text(text)
else:
    print("Invalid choice.")
    exit()

# Display the analytical report
print("\n========== TEXT ANALYSIS REPORT ==========")
print("Total Words:", total_words)
print("\nWord Frequency:")

# sorted() displays the words alphabetically.
for word in sorted(frequency):
    print(word, ":", frequency[word])
print("\nPalindromes:")

if palindromes:
    print(", ".join(sorted(palindromes)))
else:
    print("No palindromes found.")
print("==========================================")