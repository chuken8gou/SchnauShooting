#!/usr/bin/env python3
"""
Extract sprites from grid and make green background transparent
"""

from PIL import Image

def is_green(r, g, b):
    """Check if pixel is green background"""
    return r < 150 and g > 170 and b < 150

def is_magenta(r, g, b):
    """Check if pixel is magenta grid line"""
    return r > 180 and g < 80 and b > 180

def find_grid_boundaries(img):
    """Find exact grid line positions"""
    width, height = img.size
    pixels = img.load()

    # Find vertical boundaries (columns of magenta)
    v_bounds = []
    x = 0
    while x < width:
        # Check if this column is magenta
        r, g, b, a = pixels[x, 10]
        if is_magenta(r, g, b):
            # Found start of grid line, skip it
            line_start = x
            while x < width:
                r, g, b, a = pixels[x, 10]
                if not is_magenta(r, g, b):
                    break
                x += 1
            v_bounds.append((line_start, x))
        else:
            x += 1

    # Find horizontal boundaries (rows of magenta)
    h_bounds = []
    y = 0
    while y < height:
        # Check if this row is magenta
        r, g, b, a = pixels[10, y]
        if is_magenta(r, g, b):
            # Found start of grid line, skip it
            line_start = y
            while y < height:
                r, g, b, a = pixels[10, y]
                if not is_magenta(r, g, b):
                    break
                y += 1
            h_bounds.append((line_start, y))
        else:
            y += 1

    return v_bounds, h_bounds

def extract_sprites(input_path, output_path):
    print(f"Loading image: {input_path}")
    img = Image.open(input_path)
    img = img.convert("RGBA")

    width, height = img.size
    print(f"Image size: {width}x{height}")

    # Find grid boundaries
    print("Finding grid boundaries...")
    v_bounds, h_bounds = find_grid_boundaries(img)

    print(f"Found {len(v_bounds)} vertical boundaries")
    print(f"Found {len(h_bounds)} horizontal boundaries")

    # Calculate grid cells (between boundaries)
    COLS = len(v_bounds) - 1
    ROWS = len(h_bounds) - 1

    print(f"Grid: {COLS} columns x {ROWS} rows = {COLS * ROWS} sprites")

    # Calculate sprite dimensions from first cell
    if COLS > 0 and ROWS > 0:
        sprite_w = v_bounds[1][0] - v_bounds[0][1]
        sprite_h = h_bounds[1][0] - h_bounds[0][1]
        print(f"Sprite dimensions: {sprite_w}x{sprite_h}")
    else:
        print("Error: Could not determine grid")
        return

    # Create new spritesheet without grid lines
    FINAL_ROWS = 8  # Pad to 8 rows for consistency
    new_width = sprite_w * COLS
    new_height = sprite_h * FINAL_ROWS
    new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

    print(f"Creating new spritesheet: {new_width}x{new_height}")
    print(f"Processing sprites...")

    sprite_count = 0
    for row in range(ROWS):
        for col in range(COLS):
            # Calculate source position (between grid lines)
            src_x = v_bounds[col][1]  # Right edge of left grid line
            src_y = h_bounds[row][1]  # Bottom edge of top grid line

            # Extract sprite
            sprite = img.crop((src_x, src_y, src_x + sprite_w, src_y + sprite_h))

            # Make green background and magenta grid lines transparent
            pixels = sprite.load()
            for y in range(sprite_h):
                for x in range(sprite_w):
                    r, g, b, a = pixels[x, y]
                    if is_green(r, g, b) or is_magenta(r, g, b):
                        pixels[x, y] = (r, g, b, 0)

            # Paste into new spritesheet
            dest_x = col * sprite_w
            dest_y = row * sprite_h
            new_img.paste(sprite, (dest_x, dest_y))

            sprite_count += 1
            if sprite_count % 16 == 0:
                print(f"  Processed {sprite_count}/{COLS * ROWS} sprites")

    print(f"Processed {sprite_count} sprites total")
    print(f"Saving to: {output_path}")
    new_img.save(output_path, "PNG")
    print("Done!")

if __name__ == "__main__":
    extract_sprites(
        "1771081958996.png",
        "images/player_spritesheet.png"
    )
