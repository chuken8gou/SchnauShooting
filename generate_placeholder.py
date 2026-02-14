#!/usr/bin/env python3
"""
Generate cute player images (64x64 PNG) for SchnauShooting game
Top-down view: 2-head-tall deformed miniature schnauzer
Superman pose with Takecopter on head
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
GRAY = (180, 180, 180, 255)
DARK_GRAY = (100, 100, 100, 255)
CYAN = (79, 195, 247, 255)
BLUE = (33, 150, 243, 255)
BLACK = (0, 0, 0, 255)

def draw_schnauzer_top_view(draw):
    """
    Draw miniature schnauzer from top-down view
    2-head proportion: head is about same size as body
    Superman flying pose: arms stretched forward
    """

    # === BODY (lower, smaller oval) ===
    # Body positioned lower, slightly smaller than head
    body_x1, body_y1 = 24, 36
    body_x2, body_y2 = 40, 54
    draw.ellipse([body_x1, body_y1, body_x2, body_y2], fill=WHITE, outline=DARK_GRAY)

    # === ARMS (stretched forward like Superman) ===
    # Left arm (stretched upward on screen = forward in 3D)
    draw.ellipse([20, 28, 26, 38], fill=WHITE, outline=DARK_GRAY)
    # Left paw (small circle)
    draw.ellipse([19, 25, 24, 30], fill=GRAY)

    # Right arm (stretched upward on screen = forward in 3D)
    draw.ellipse([38, 28, 44, 38], fill=WHITE, outline=DARK_GRAY)
    # Right paw (small circle)
    draw.ellipse([40, 25, 45, 30], fill=GRAY)

    # === LEGS (visible at bottom, slightly bent) ===
    # Back left leg
    draw.ellipse([24, 50, 29, 58], fill=WHITE, outline=DARK_GRAY)
    # Back right leg
    draw.ellipse([35, 50, 40, 58], fill=WHITE, outline=DARK_GRAY)

    # === HEAD (upper, larger) ===
    # Main head (round, fluffy schnauzer face)
    head_x1, head_y1 = 22, 20
    head_x2, head_y2 = 42, 40
    draw.ellipse([head_x1, head_y1, head_x2, head_y2], fill=WHITE, outline=DARK_GRAY)

    # Schnauzer's signature beard/muzzle (rectangle protruding down)
    muzzle_x1, muzzle_y1 = 26, 36
    muzzle_x2, muzzle_y2 = 38, 44
    draw.rectangle([muzzle_x1, muzzle_y1, muzzle_x2, muzzle_y2], fill=GRAY, outline=DARK_GRAY)

    # Nose (small black triangle/circle at tip of muzzle)
    draw.ellipse([30, 42, 34, 46], fill=BLACK)

    # Ears (small rounded rectangles on sides)
    # Left ear
    draw.ellipse([20, 24, 24, 32], fill=GRAY, outline=DARK_GRAY)
    # Right ear
    draw.ellipse([40, 24, 44, 32], fill=GRAY, outline=DARK_GRAY)

    # Eyes (small black dots)
    # Left eye
    draw.ellipse([27, 28, 30, 31], fill=BLACK)
    # Right eye
    draw.ellipse([34, 28, 37, 31], fill=BLACK)

def draw_takecopter(draw, frame):
    """
    Draw Takecopter (Doraemon's bamboo copter) on top of head
    4-frame rotation animation
    """
    # Propeller center position (top of head)
    cx, cy = 32, 16

    # Base/mount (small gray circle)
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=DARK_GRAY, outline=BLACK)

    # Propeller blades - rotate based on frame
    # Frame 0: horizontal —
    # Frame 1: diagonal /
    # Frame 2: vertical |
    # Frame 3: diagonal \

    blade_length = 14
    blade_width = 3

    if frame == 0:  # Horizontal —
        draw.rectangle([cx-blade_length, cy-blade_width//2,
                       cx+blade_length, cy+blade_width//2+blade_width],
                      fill=CYAN, outline=BLUE)
        # Highlight on blades
        draw.rectangle([cx-blade_length, cy-blade_width//2,
                       cx-blade_length+4, cy+blade_width//2+blade_width],
                      fill=BLUE)
        draw.rectangle([cx+blade_length-4, cy-blade_width//2,
                       cx+blade_length, cy+blade_width//2+blade_width],
                      fill=BLUE)

    elif frame == 1:  # Diagonal / (thin line)
        # Draw as thin rotated rectangle (approximate with ellipse)
        draw.line([cx-10, cy+8, cx+10, cy-8], fill=CYAN, width=4)
        draw.line([cx-10+1, cy+8, cx+10+1, cy-8], fill=BLUE, width=2)

    elif frame == 2:  # Vertical |
        draw.rectangle([cx-blade_width//2, cy-blade_length,
                       cx+blade_width//2+blade_width, cy+blade_length],
                      fill=CYAN, outline=BLUE)
        # Highlight
        draw.rectangle([cx-blade_width//2, cy-blade_length,
                       cx+blade_width//2+blade_width, cy-blade_length+4],
                      fill=BLUE)
        draw.rectangle([cx-blade_width//2, cy+blade_length-4,
                       cx+blade_width//2+blade_width, cy+blade_length],
                      fill=BLUE)

    elif frame == 3:  # Diagonal \ (thin line)
        draw.line([cx-10, cy-8, cx+10, cy+8], fill=CYAN, width=4)
        draw.line([cx-10+1, cy-8, cx+10+1, cy+8], fill=BLUE, width=2)

# Generate 4 frames
for i in range(4):
    img = Image.new('RGBA', (SIZE, SIZE), BG_TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Draw Takecopter first (background layer)
    draw_takecopter(draw, i)

    # Draw schnauzer on top
    draw_schnauzer_top_view(draw)

    # Save
    filename = f'images/player_{i+1}.png'
    img.save(filename)
    print(f'✅ Generated {filename}')

print('\n🎉 All 4 frames generated successfully!')
print('📁 Images saved in ./images/ folder')
print('🐕 Top-down view, 2-head deformed, Superman pose')
print('🚁 Takecopter rotating animation')
