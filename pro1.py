import sys


class CaesarCipher:
    def __init__(self, shift: int):
        self.shift = shift % 26

    def encode(self, text: str) -> str:
        return self._transform(text, self.shift)

    def decode(self, text: str) -> str:
        return self._transform(text, -self.shift)

    @staticmethod
    def _transform(text: str, shift: int) -> str:
        result = []

        for char in text:
            if char.isupper():
                result.append(
                    chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                )
            elif char.islower():
                result.append(
                    chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                )
            else:
                # Keep spaces, numbers, and special symbols unchanged
                result.append(char)

        return ''.join(result)


def main():
    # Accept input through command-line arguments when available
    if len(sys.argv) >= 4:
        operation = sys.argv[1].lower()
        text = sys.argv[2]

        try:
            shift = int(sys.argv[3])
        except ValueError:
            print("Error: shift key must be an integer.")
            return
    else:
        print("=== Caesar Cipher Tool ===")

        operation = input("Enter operation (encode/decode): ").strip().lower()
        text = input("Enter text: ")

        shift_input = input("Enter shift key: ").strip()

        if not shift_input.lstrip("-").isdigit():
            print("Error: shift key must be an integer.")
            return

        shift = int(shift_input)

    if operation not in ("encode", "decode"):
        print("Error: operation must be 'encode' or 'decode'.")
        return

    if not isinstance(text, str):
        print("Error: text must be a string.")
        return

    cipher = CaesarCipher(shift)

    if operation == "encode":
        result = cipher.encode(text)
    else:
        result = cipher.decode(text)

    print("Result:", result)


if __name__ == "__main__":
    main()