
"""
Program: Safe File Processor with Custom Exception Hierarchy
Author: Saurav 241492

Description:
Processes a text file safely using custom exceptions,
exception handling, traceback logging, and resource cleanup.

Input: A file path containing one integer per line.
Output: Parsed integers, processing status, and error logs.
"""

import logging
import traceback


# Configure error logging
logging.basicConfig(
    filename="file_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Custom exception hierarchy
class FileProcessorError(Exception):
    """Base exception for file processing errors."""
    pass


class InvalidFileFormatError(FileProcessorError):
    """Raised when file content has an invalid format."""
    pass


class EmptyFileError(FileProcessorError):
    """Raised when the input file is empty."""
    pass


class SafeFileProcessor:
    def __init__(self, filename):
        self.filename = filename

    def process_file(self):
        file = None

        try:
            file = open(self.filename, "r", encoding="utf-8")

            lines = file.readlines()

            if not lines:
                raise EmptyFileError("The input file is empty.")

            numbers = []

            for line_number, line in enumerate(lines, start=1):
                value = line.strip()

                # Ignore blank lines.
                if not value:
                    continue

                try:
                    numbers.append(int(value))
                except ValueError as exc:
                    raise InvalidFileFormatError(
                        f"Invalid integer on line {line_number}: {value!r}"
                    ) from exc

            if not numbers:
                raise EmptyFileError(
                    "The file contains no valid data."
                )

        except FileProcessorError:
            logging.error(
                "File processing failed:\n%s",
                traceback.format_exc()
            )
            print("Processing error occurred. See file_errors.log.")

        except OSError:
            logging.error(
                "File access error:\n%s",
                traceback.format_exc()
            )
            print("Unable to access the file. See file_errors.log.")

        else:
            print("File processed successfully.")
            print("Numbers:", numbers)
            print("Total:", sum(numbers))
            print("Average:", sum(numbers) / len(numbers))

        finally:
            if file is not None and not file.closed:
                file.close()

            print("File cleanup completed.")


# Main program
if __name__ == "__main__":
    filename = input("Enter file path: ").strip().strip('"')

    processor = SafeFileProcessor(filename)
    processor.process_file()
