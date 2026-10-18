
"""
Program: Digital Image Filter and Color Converter Utility
Author: Saurav 241492

Description:
Processes JPEG and PNG images using RGB pixel manipulation.
Applies grayscale conversion, binary thresholding, and blur filters.

Input: Image file path and selected filter.
Output: Processed image saved in the output directory.
"""

from PIL import Image, ImageFilter
import os


# Function to convert image to grayscale
def grayscale_image(image):
    return image.convert("L")


# Function to convert image to black and white
def threshold_image(image, threshold=128):
    gray = image.convert("L")
    return gray.point(
        lambda pixel: 255 if pixel >= threshold else 0
    )


# Function to apply blur filter
def blur_image(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))


# Function to adjust RGB color channels
def adjust_rgb(image, red=1.0, green=1.0, blue=1.0):
    image = image.convert("RGB")
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            pixels[x, y] = (
                max(0, min(255, int(r * red))),
                max(0, min(255, int(g * green))),
                max(0, min(255, int(b * blue)))
            )

    return image


# Main program
if __name__ == "__main__":
    file_path = input("Enter image path: ").strip().strip('"')

    if not os.path.isfile(file_path):
        print("Error: Image file not found.")
    else:
        try:
            with Image.open(file_path) as source:
                image = source.convert("RGB")

            print("\n1. Grayscale")
            print("2. Black and White")
            print("3. Blur")
            print("4. Adjust RGB")

            choice = input("Select filter (1-4): ")

            if choice == "1":
                result = grayscale_image(image)
                suffix = "grayscale"

            elif choice == "2":
                threshold = int(input("Enter threshold (0-255): "))
                if not 0 <= threshold <= 255:
                    raise ValueError("Threshold must be between 0 and 255.")
                result = threshold_image(image, threshold)
                suffix = "black_white"

            elif choice == "3":
                radius = float(input("Enter blur radius (0 or greater): "))
                if radius < 0:
                    raise ValueError("Blur radius cannot be negative.")
                result = blur_image(image, radius)
                suffix = "blurred"

            elif choice == "4":
                red = float(input("Red factor: "))
                green = float(input("Green factor: "))
                blue = float(input("Blue factor: "))
                result = adjust_rgb(image, red, green, blue)
                suffix = "rgb_adjusted"

            else:
                print("Invalid choice.")
                raise SystemExit

            name, _ = os.path.splitext(file_path)
            output_path = f"{name}_{suffix}.png"
            result.save(output_path)

            print("Processed image saved to:", output_path)

        except (OSError, ValueError) as error:
            print("Error:", error)
