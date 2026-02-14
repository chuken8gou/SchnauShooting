#!/usr/bin/env python3
"""
Process spritesheet:
- Remove magenta (#FF00FF) grid lines
- Make green (#00FF00) background transparent
"""

from PIL import Image

def process_spritesheet(input_path, output_path):
    print(f"Loading image: {input_path}")
    img = Image.open(input_path)
    img = img.convert("RGBA")

    width, height = img.size
    print(f"Image size: {width}x{height}")

    pixels = img.load()

    # Define color ranges for detection
    # Magenta: RGB(255, 0, 255) with tolerance
    # Green: RGB(0, 255, 0) with tolerance
    magenta_tolerance = 30
    green_tolerance = 30

    transparent_count = 0

    print("Processing pixels...")
    for y in range(height):
        if y % 100 == 0:
            print(f"  Row {y}/{height}")
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Check if pixel is magenta (grid line)
            is_magenta = (
                abs(r - 255) < magenta_tolerance and
                abs(g - 0) < magenta_tolerance and
                abs(b - 255) < magenta_tolerance
            )

            # Check if pixel is green (background)
            is_green = (
                abs(r - 0) < green_tolerance and
                abs(g - 255) < green_tolerance and
                abs(b - 0) < green_tolerance
            )

            # Make magenta and green pixels transparent
            if is_magenta or is_green:
                pixels[x, y] = (r, g, b, 0)
                transparent_count += 1

    print(f"Made {transparent_count} pixels transparent")
    print(f"Saving processed image to: {output_path}")
    img.save(output_path, "PNG")
    print("Done!")

if __name__ == "__main__":
    process_spritesheet(
        "1771081958996.png",
        "images/player_spritesheet.png"
    )
