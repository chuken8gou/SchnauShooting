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

    # Define color ranges for detection based on actual pixel analysis
    # Actual magenta: RGB(226, 24, 230) - expanded range to catch all variations
    # Actual green: RGB(116, 187, 111) - expanded range
    # Magenta: high R (>180), low G (<80), high B (>180)
    # Green: low R (<150), high G (>170), low B (<150)

    transparent_count = 0

    print("Processing pixels...")
    for y in range(height):
        if y % 100 == 0:
            print(f"  Row {y}/{height}")
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Check if pixel is magenta-like (grid line)
            # High red and blue, low green
            is_magenta = (
                r > 180 and
                g < 80 and
                b > 180
            )

            # Check if pixel is green-like (background)
            # Low red, high green, low blue
            is_green = (
                r < 150 and
                g > 170 and
                b < 150
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
