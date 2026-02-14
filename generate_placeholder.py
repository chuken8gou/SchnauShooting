#!/usr/bin/env python3
"""
Generate placeholder player images (64x64 PNG) for SchnauShooting game
Simple pixel-art style miniature schnauzer with propeller hat
"""

from PIL import Image, ImageDraw
import os

# Create images directory
os.makedirs('images', exist_ok=True)

# Image size
SIZE = 64

# Colors
BG_TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255, 255)
CYAN = (79, 195, 247, 255)
GRAY = (128, 128, 128, 255)

def draw_schnauzer_base(draw):
    """Draw basic schnauzer body (white)"""
    # Head (square-ish)
    draw.rectangle([20, 25, 44, 45], fill=WHITE)

    # Snout/beard (signature schnauzer feature)
    draw.rectangle([18, 35, 46, 48], fill=WHITE)

    # Ears
    draw.rectangle([18, 25, 22, 35], fill=WHITE)
    draw.rectangle([42, 25, 46, 35], fill=WHITE)

    # Body
    draw.ellipse([22, 45, 42, 58], fill=WHITE)

    # Eyes (black dots)
    draw.rectangle([26, 32, 28, 34], fill=(0, 0, 0, 255))
    draw.rectangle([36, 32, 38, 34], fill=(0, 0, 0, 255))

    # Nose
    draw.rectangle([31, 40, 33, 42], fill=(0, 0, 0, 255))

def draw_propeller(draw, frame):
    """Draw propeller (Takecopter) with rotation animation"""
    # Base (gray circle on top of head)
    draw.ellipse([28, 18, 36, 26], fill=GRAY)

    # Propeller blades (rotate based on frame)
    angles = [0, 45, 90, 135]  # Different angle per frame
    angle = angles[frame]

    if angle == 0 or angle == 90:
        # Horizontal blade
        draw.rectangle([20, 20, 44, 22], fill=CYAN)

    if angle == 45 or angle == 135:
        # Diagonal blade (simplified as horizontal for pixel art)
        draw.rectangle([22, 19, 42, 21], fill=CYAN)

# Generate 4 frames
for i in range(4):
    img = Image.new('RGBA', (SIZE, SIZE), BG_TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Draw character
    draw_schnauzer_base(draw)
    draw_propeller(draw, i)

    # Save
    filename = f'images/player_{i+1}.png'
    img.save(filename)
    print(f'Generated {filename}')

print('\n✅ All 4 frames generated successfully!')
print('Images are in ./images/ folder')
