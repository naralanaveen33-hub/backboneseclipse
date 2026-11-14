import os
from PIL import Image, ImageDraw

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def gen_platforms():
    tile_dir = "assets/tiles"
    ensure_dir(f"{tile_dir}/platform_forest_160.png")
    
    # 1. Forest Platform 160x32
    im = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Dirt base
    d.rectangle([0, 6, 159, 31], fill=(95, 60, 38, 255))
    # Mossy rock accents
    d.rectangle([20, 14, 50, 24], fill=(70, 75, 70, 255))
    d.rectangle([90, 16, 130, 26], fill=(70, 75, 70, 255))
    # Grass layer
    d.rectangle([0, 0, 159, 8], fill=(60, 165, 60, 255))
    d.rectangle([0, 0, 159, 3], fill=(110, 220, 85, 255))
    # Grass blades
    for x in range(0, 160, 4):
        d.line([(x, 8), (x + 2, 12)], fill=(40, 120, 40, 255), width=1)
    im.save(f"{tile_dir}/platform_forest_160.png")

    # 2. Forest Platform 80x24 (Floating Moss Block)
    im = Image.new("RGBA", (80, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(4, 23), (75, 23), (79, 4), (0, 4)], fill=(80, 52, 34, 255))
    d.rectangle([0, 0, 79, 6], fill=(65, 175, 65, 255))
    d.rectangle([0, 0, 79, 2], fill=(120, 230, 90, 255))
    # Hanging vines underneath
    d.line([(16, 20), (16, 23)], fill=(50, 150, 50, 255), width=2)
    d.line([(45, 20), (45, 24)], fill=(50, 150, 50, 255), width=2)
    im.save(f"{tile_dir}/platform_forest_80.png")

    # 3. Castle Platform 160x32 (Gothic Carved Stone)
    im = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 159, 31], fill=(50, 45, 60, 255))
    # Stone brick lines
    for y in (10, 21):
        d.line([(0, y), (159, y)], fill=(30, 25, 38, 255), width=1)
    for x in range(0, 160, 40):
        d.line([(x, 0), (x, 10)], fill=(30, 25, 38, 255), width=1)
        d.line([(x + 20, 10), (x + 20, 21)], fill=(30, 25, 38, 255), width=1)
        d.line([(x, 21), (x, 31)], fill=(30, 25, 38, 255), width=1)
    # Gold top trim
    d.line([(0, 0), (159, 0)], fill=(210, 175, 65, 255), width=2)
    d.line([(0, 2), (159, 2)], fill=(85, 75, 105, 255), width=1)
    im.save(f"{tile_dir}/platform_castle_160.png")

    # 4. Castle Platform 80x24
    im = Image.new("RGBA", (80, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(2, 23), (77, 23), (79, 2), (0, 2)], fill=(45, 40, 55, 255))
    d.line([(0, 0), (79, 0)], fill=(200, 165, 60, 255), width=2)
    im.save(f"{tile_dir}/platform_castle_80.png")

    # 5. Lava Hazard 160x32
    im = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 4, 159, 31], fill=(175, 30, 15, 255))
    d.rectangle([0, 14, 159, 31], fill=(130, 20, 10, 255))
    # Glowing molten surface
    d.line([(0, 4), (159, 4)], fill=(255, 210, 40, 255), width=3)
    d.line([(0, 6), (159, 6)], fill=(255, 120, 20, 255), width=2)
    im.save(f"{tile_dir}/lava_hazard.png")

    # 6. Wall / Barrier 32x280 (for boss arena)
    im = Image.new("RGBA", (32, 280), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 31, 279], fill=(40, 35, 50, 255))
    for y in range(0, 280, 24):
        d.line([(0, y), (31, y)], fill=(25, 20, 32, 255), width=2)
    # Glowing magical runes sealing the arena
    for y in range(30, 260, 50):
        d.ellipse([10, y, 22, y + 12], fill=(160, 40, 255, 180))
    im.save(f"{tile_dir}/boss_barrier.png")
    print("Generated platform tiles and barriers")

if __name__ == "__main__":
    gen_platforms()
