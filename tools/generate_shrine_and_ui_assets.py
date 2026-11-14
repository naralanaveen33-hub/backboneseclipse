#!/usr/bin/env python3
"""
Generate pixel-art assets for Ruined Shrines and Rebound UI.
"""
from PIL import Image, ImageDraw
import math
import os

def create_rebound_fill():
    w, h = 176, 20
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    for y in range(h):
        # Vertical gradient from electric amber/gold to deep crimson gold
        ratio = y / float(h)
        r = int(255)
        g = int(180 + 70 * (1.0 - ratio))
        b = int(20 + 40 * (1.0 - ratio))
        # Top highlight
        if y < 3:
            g = min(255, g + 50)
            b = min(255, b + 80)
        draw.line([(0, y), (w - 1, y)], fill=(r, g, b, 255))
    # Border
    draw.rectangle([0, 0, w - 1, h - 1], outline=(255, 230, 100, 255))
    im.save("assets/ui/rebound_fill.png")
    print("Created assets/ui/rebound_fill.png")

def create_shrine_dormant():
    w, h = 32, 48
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Base pedestal: x: 4 to 27, y: 38 to 47
    draw.rectangle([2, 42, 29, 47], fill=(50, 52, 58, 255), outline=(35, 36, 40, 255))
    draw.rectangle([5, 36, 26, 42], fill=(62, 65, 72, 255), outline=(45, 47, 52, 255))
    
    # Pillar shaft: x: 8 to 23, y: 16 to 36
    draw.rectangle([8, 16, 23, 36], fill=(70, 74, 82, 255), outline=(48, 50, 56, 255))
    
    # Weathered cracks / dormant dark runes
    draw.line([(12, 19), (14, 25), (13, 31)], fill=(38, 40, 44, 255), width=1)
    draw.line([(19, 21), (18, 27), (20, 33)], fill=(38, 40, 44, 255), width=1)
    draw.line([(10, 26), (16, 26)], fill=(38, 40, 44, 255), width=1)
    
    # Capital (top): x: 5 to 26, y: 10 to 16
    draw.rectangle([5, 10, 26, 16], fill=(62, 65, 72, 255), outline=(45, 47, 52, 255))
    
    # Dormant orb: x: 11 to 20, y: 1 to 10
    draw.ellipse([11, 2, 20, 9], fill=(60, 70, 80, 255), outline=(40, 48, 56, 255))
    # Dim glint
    draw.point((13, 4), fill=(100, 115, 130, 255))
    
    im.save("assets/tiles/shrine_dormant.png")
    print("Created assets/tiles/shrine_dormant.png")

def create_shrine_active():
    w, h = 32, 48
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Glow aura behind orb
    for r in range(8, 0, -1):
        alpha = int(70 * (1.0 - r / 8.0))
        draw.ellipse([16 - r - 4, 6 - r, 16 + r + 4, 6 + r], fill=(0, 255, 230, alpha))
        
    # Base pedestal: x: 4 to 27, y: 38 to 47
    draw.rectangle([2, 42, 29, 47], fill=(80, 95, 105, 255), outline=(55, 68, 76, 255))
    draw.rectangle([5, 36, 26, 42], fill=(95, 112, 124, 255), outline=(68, 82, 92, 255))
    
    # Pillar shaft: x: 8 to 23, y: 16 to 36
    draw.rectangle([8, 16, 23, 36], fill=(110, 130, 145, 255), outline=(75, 90, 102, 255))
    
    # Radiant glowing runes (cyan & gold)
    draw.line([(12, 19), (14, 25), (13, 31)], fill=(0, 255, 240, 255), width=2)
    draw.line([(19, 21), (18, 27), (20, 33)], fill=(255, 230, 50, 255), width=2)
    draw.line([(10, 26), (21, 26)], fill=(120, 255, 255, 255), width=2)
    
    # Capital (top): x: 5 to 26, y: 10 to 16
    draw.rectangle([5, 10, 26, 16], fill=(95, 112, 124, 255), outline=(68, 82, 92, 255))
    
    # Radiant crystal orb: glowing cyan & solar gold
    draw.ellipse([10, 1, 21, 10], fill=(255, 245, 180, 255), outline=(0, 240, 255, 255))
    draw.ellipse([12, 3, 19, 8], fill=(255, 255, 255, 255))
    
    im.save("assets/tiles/shrine_active.png")
    print("Created assets/tiles/shrine_active.png")

if __name__ == "__main__":
    create_rebound_fill()
    create_shrine_dormant()
    create_shrine_active()
