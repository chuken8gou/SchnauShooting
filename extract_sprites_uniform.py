#!/usr/bin/env python3
"""
Extract sprites from 16x8 grid, using only first 6 rows
"""

from PIL import Image

def is_green(r, g, b):
    """Check if pixel is green background"""
    return r < 150 and g > 170 and b < 150

def is_magenta(r, g, b):
    """Check if pixel is magenta grid line"""
    return r > 180 and g < 80 and b > 180

def extract_sprites_uniform(input_path, output_path):
    print(f"Loading image: {input_path}")
    img = Image.open(input_path)
    img = img.convert("RGBA")

    width, height = img.size
    print(f"Image size: {width}x{height}")

    # Grid structure: 16 columns x 8 rows, use only first 1 row
    TOTAL_COLS = 16
    TOTAL_ROWS = 8
    USE_ROWS = 1  # Only use first row (clean and aligned)

    # Calculate cell size (including grid lines)
    cell_w = width // TOTAL_COLS
    cell_h = height // TOTAL_ROWS

    print(f"Cell size (with grid): {cell_w}x{cell_h}")

    # Detect grid line width by sampling
    pixels = img.load()

    # Find vertical grid line width (sample from top-left)
    grid_line_v = 0
    for x in range(cell_w):
        r, g, b, a = pixels[x, 10]
        if is_magenta(r, g, b):
            grid_line_v += 1
        else:
            break

    # Find horizontal grid line width
    grid_line_h = 0
    for y in range(cell_h):
        r, g, b, a = pixels[10, y]
        if is_magenta(r, g, b):
            grid_line_h += 1
        else:
            break

    print(f"Detected grid line width: vertical={grid_line_v}px, horizontal={grid_line_h}px")

    # Calculate sprite dimensions (cell - grid line)
    # Add extra pixels at bottom to show full character feet
    BOTTOM_EXTENSION = 15
    sprite_w = cell_w - grid_line_v
    sprite_h = cell_h - grid_line_h + BOTTOM_EXTENSION

    print(f"Sprite dimensions (before trimming): {sprite_w}x{sprite_h} (bottom extended by {BOTTOM_EXTENSION}px)")

    # Trim from edges to remove grid line remnants
    # Horizontal: 5% from each side
    # Vertical: 0% from both sides (to show full character)
    TRIM_PERCENT_H = 0.05
    TRIM_PERCENT_V_TOP = 0.00
    TRIM_PERCENT_V_BOTTOM = 0.00

    trim_x = int(sprite_w * TRIM_PERCENT_H)
    trim_y_top = int(sprite_h * TRIM_PERCENT_V_TOP)
    trim_y_bottom = int(sprite_h * TRIM_PERCENT_V_BOTTOM)

    # Final sprite size after trimming
    final_w = sprite_w - 2 * trim_x
    final_h = sprite_h - trim_y_top - trim_y_bottom

    print(f"Trimming: horizontal {TRIM_PERCENT_H*100}% ({trim_x}px), top {TRIM_PERCENT_V_TOP*100}% ({trim_y_top}px), bottom {TRIM_PERCENT_V_BOTTOM*100}% ({trim_y_bottom}px)")
    print(f"Final sprite dimensions: {final_w}x{final_h}")

    # Create new spritesheet for specified rows
    new_width = final_w * TOTAL_COLS
    new_height = final_h * USE_ROWS
    new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

    print(f"Creating new spritesheet: {new_width}x{new_height}")
    print(f"Processing {TOTAL_COLS * USE_ROWS} sprites (rows 0-{USE_ROWS-1})...")

    sprite_count = 0
    for row in range(USE_ROWS):
        for col in range(TOTAL_COLS):
            # Calculate source position
            # Each cell starts at (col * cell_w, row * cell_h)
            # Skip grid lines at the beginning of each cell
            src_x = col * cell_w + grid_line_v
            src_y = row * cell_h + grid_line_h

            # Extract sprite
            sprite = img.crop((src_x, src_y, src_x + sprite_w, src_y + sprite_h))

            # Make green background and magenta grid lines transparent
            sprite_pixels = sprite.load()
            for y in range(sprite_h):
                for x in range(sprite_w):
                    r, g, b, a = sprite_pixels[x, y]
                    if is_green(r, g, b) or is_magenta(r, g, b):
                        sprite_pixels[x, y] = (r, g, b, 0)

            # Trim edges: 5% left/right, 5% top, 2% bottom
            trimmed_sprite = sprite.crop((trim_x, trim_y_top,
                                         sprite_w - trim_x,
                                         sprite_h - trim_y_bottom))

            # Paste into new spritesheet
            dest_x = col * final_w
            dest_y = row * final_h
            new_img.paste(trimmed_sprite, (dest_x, dest_y))

            sprite_count += 1
            if sprite_count % 16 == 0:
                print(f"  Processed row {row + 1}/{USE_ROWS} ({sprite_count} sprites)")

    print(f"Processed {sprite_count} sprites total")
    print(f"Saving to: {output_path}")
    new_img.save(output_path, "PNG")
    print("Done!")

if __name__ == "__main__":
    extract_sprites_uniform(
        "1771081958996.png",
        "images/player_spritesheet.png"
    )
