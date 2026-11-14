#!/usr/bin/env python3
"""
Generate backgrounds, platforms, and projectile sprites for Levels 3-7.
"""
import os
import math
import random
from PIL import Image, ImageDraw

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def gen_inferno_assets():
    b_dir = "assets/backgrounds/inferno"
    ensure_dir(f"{b_dir}/inferno_sky.png")
    
    # Inferno Sky 960x540
    sky = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
    d = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        r = int(45 + (160 - 45) * t)
        g = int(8 + (35 - 8) * t)
        b = int(4 + (10 - 4) * t)
        d.line([(0, y), (960, y)], fill=(r, g, b, 255))
    # Glowing lava smoke & volcanic embers
    for _ in range(16):
        nx = random.randint(50, 900)
        ny = random.randint(100, 500)
        nr = random.randint(80, 180)
        d.ellipse([nx - nr, ny - nr//2, nx + nr, ny + nr//2], fill=(220, 70, 20, 45))
    for _ in range(80):
        ex = random.randint(0, 959)
        ey = random.randint(100, 539)
        d.point((ex, ey), fill=(255, 200, 50, random.randint(150, 255)))
    sky.save(f"{b_dir}/inferno_sky.png")
    
    # Magma Cavern BG
    bg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    # Volcanic spires / stalactites
    for i in range(12):
        bx = i * 85 + random.randint(-15, 15)
        bw = random.randint(60, 100)
        bh = random.randint(180, 360)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(35, 12, 10, 220))
        # Lava vein
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2 + random.randint(-10, 10), 540)], fill=(255, 90, 20, 180), width=2)
    bg.save(f"{b_dir}/magma_cavern.png")
    
    # Molten FG
    fg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    for i in range(16):
        bx = i * 65 + random.randint(-10, 10)
        bw = random.randint(50, 80)
        bh = random.randint(120, 260)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(55, 18, 14, 255))
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2, 540)], fill=(255, 140, 30, 230), width=2)
    fg.save(f"{b_dir}/molten_fg.png")
    print("Generated Inferno backgrounds")

def gen_frost_assets():
    b_dir = "assets/backgrounds/frost"
    ensure_dir(f"{b_dir}/frost_sky.png")
    
    # Frost Sky 960x540 (Glacial cyan & teal aurora)
    sky = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
    d = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        r = int(5 + (20 - 5) * t)
        g = int(25 + (70 - 25) * t)
        b = int(50 + (110 - 50) * t)
        d.line([(0, y), (960, y)], fill=(r, g, b, 255))
    # Aurora ribbons
    for _ in range(6):
        ax = random.randint(100, 850)
        ay = random.randint(60, 260)
        aw = random.randint(200, 450)
        ah = random.randint(50, 120)
        d.ellipse([ax - aw//2, ay - ah//2, ax + aw//2, ay + ah//2], fill=(0, 255, 200, 35))
    # Snow crystals
    for _ in range(100):
        sx = random.randint(0, 959)
        sy = random.randint(0, 539)
        d.point((sx, sy), fill=(230, 250, 255, random.randint(140, 240)))
    sky.save(f"{b_dir}/frost_sky.png")
    
    # Ice Mountains
    bg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    for i in range(10):
        bx = i * 105 + random.randint(-20, 20)
        bw = random.randint(90, 140)
        bh = random.randint(220, 380)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(20, 45, 65, 210))
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2 + 10, 540)], fill=(120, 220, 255, 180), width=2)
    bg.save(f"{b_dir}/ice_mountains.png")
    
    # Frost Cavern FG
    fg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    for i in range(14):
        bx = i * 75 + random.randint(-15, 15)
        bw = random.randint(60, 95)
        bh = random.randint(140, 270)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(30, 65, 90, 255))
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2, 540)], fill=(180, 245, 255, 220), width=2)
    fg.save(f"{b_dir}/frost_cavern.png")
    print("Generated Frost backgrounds")

def gen_storm_assets():
    b_dir = "assets/backgrounds/storm"
    ensure_dir(f"{b_dir}/storm_sky.png")
    
    # Storm Sky 960x540 (Dark slate, purple lightning hue)
    sky = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
    d = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        r = int(15 + (45 - 15) * t)
        g = int(12 + (30 - 12) * t)
        b = int(35 + (70 - 35) * t)
        d.line([(0, y), (960, y)], fill=(r, g, b, 255))
    # Lightning forks in sky
    d.line([(280, 20), (295, 100), (275, 180), (310, 250)], fill=(255, 250, 180, 230), width=2)
    d.line([(680, 10), (665, 90), (690, 160), (670, 230)], fill=(180, 240, 255, 230), width=2)
    sky.save(f"{b_dir}/storm_sky.png")
    
    # Thunder Spires BG
    bg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    for i in range(11):
        bx = i * 95 + random.randint(-15, 15)
        bw = random.randint(70, 110)
        bh = random.randint(220, 400)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(25, 22, 38, 220))
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2, 540)], fill=(255, 220, 80, 180), width=2)
    bg.save(f"{b_dir}/thunder_spires.png")
    
    # Storm Clouds FG
    fg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    for i in range(16):
        cx = i * 65 + random.randint(-15, 15)
        cy = 480 + random.randint(-30, 20)
        cr = random.randint(60, 95)
        d.ellipse([cx - cr, cy - cr//2, cx + cr, cy + cr//2], fill=(42, 36, 58, 220))
    fg.save(f"{b_dir}/storm_clouds.png")
    print("Generated Storm backgrounds")

def gen_abyss_assets():
    b_dir = "assets/backgrounds/abyss"
    ensure_dir(f"{b_dir}/abyss_sky.png")
    
    # Abyss Sky 960x540 (Black hole & crimson eclipse void)
    sky = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
    d = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        r = int(12 + (55 - 12) * t)
        g = int(2 + (12 - 2) * t)
        b = int(18 + (38 - 18) * t)
        d.line([(0, y), (960, y)], fill=(r, g, b, 255))
    # Crimson Eclipse Sun (Black hole with blazing solar flares)
    d.ellipse([430, 80, 530, 180], fill=(255, 50, 40, 240))
    d.ellipse([440, 90, 520, 170], fill=(0, 0, 0, 255)) # Dark core
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.randint(60, 120)
        fx = 480 + int(math.cos(angle) * dist)
        fy = 130 + int(math.sin(angle) * dist)
        d.line([(480, 130), (fx, fy)], fill=(255, 120, 50, 160), width=2)
    sky.save(f"{b_dir}/abyss_sky.png")
    
    # Throne Spires BG
    bg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    for i in range(10):
        bx = i * 105 + random.randint(-15, 15)
        bw = random.randint(80, 130)
        bh = random.randint(240, 420)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(28, 10, 20, 230))
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2, 540)], fill=(255, 40, 80, 190), width=2)
    bg.save(f"{b_dir}/throne_spires.png")
    
    # Abyssal Pillars FG
    fg = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    for i in range(14):
        bx = i * 75 + random.randint(-10, 10)
        bw = random.randint(60, 90)
        bh = random.randint(160, 300)
        d.polygon([(bx, 540), (bx + bw//2, 540 - bh), (bx + bw, 540)], fill=(45, 14, 28, 255))
        d.line([(bx + bw//2, 540 - bh), (bx + bw//2, 540)], fill=(255, 200, 60, 240), width=2)
    fg.save(f"{b_dir}/abyssal_pillars.png")
    print("Generated Abyss backgrounds")

def gen_platform_tiles():
    themes = [
        ("inferno", (45, 16, 12), (255, 120, 30), (255, 60, 20)),
        ("frost", (25, 55, 80), (180, 240, 255), (100, 200, 255)),
        ("storm", (35, 30, 50), (255, 230, 70), (180, 220, 255)),
        ("abyss", (35, 12, 24), (255, 60, 90), (255, 210, 60))
    ]
    for theme, base_c, rim_c, rune_c in themes:
        # 160x32 platform
        im160 = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(im160)
        d.rectangle([0, 0, 159, 31], fill=base_c, outline=(base_c[0]//2, base_c[1]//2, base_c[2]//2, 255))
        # Top glowing rim
        d.rectangle([0, 0, 159, 4], fill=rim_c)
        # Decorative runes
        for rx in range(16, 144, 28):
            d.line([(rx, 10), (rx + 8, 22), (rx + 16, 10)], fill=rune_c, width=2)
        im160.save(f"assets/tiles/platform_{theme}_160.png")
        
        # 80x24 platform
        im80 = Image.new("RGBA", (80, 24), (0, 0, 0, 0))
        d = ImageDraw.Draw(im80)
        d.rectangle([0, 0, 79, 23], fill=base_c, outline=(base_c[0]//2, base_c[1]//2, base_c[2]//2, 255))
        d.rectangle([0, 0, 79, 3], fill=rim_c)
        d.line([(32, 8), (40, 16), (48, 8)], fill=rune_c, width=2)
        im80.save(f"assets/tiles/platform_{theme}_80.png")
    print("Generated platform tiles for all themes")

def gen_projectiles():
    p_dir = "assets/effects/projectiles"
    ensure_dir(f"{p_dir}/magma_orb.png")
    
    # 1. Magma Orb 24x24
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 21, 21], fill=(255, 90, 10, 255), outline=(255, 220, 50, 255))
    d.ellipse([6, 6, 17, 17], fill=(255, 240, 150, 255))
    im.save(f"{p_dir}/magma_orb.png")
    
    # 2. Frost Shard 24x24
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(12, 1), (22, 12), (12, 22), (2, 12)], fill=(120, 220, 255, 255), outline=(220, 255, 255, 255))
    d.polygon([(12, 5), (18, 12), (12, 18), (6, 12)], fill=(255, 255, 255, 255))
    im.save(f"{p_dir}/frost_shard.png")
    
    # 3. Thunder Orb 24x24
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 21, 21], fill=(255, 220, 40, 255), outline=(255, 255, 180, 255))
    d.line([(12, 4), (16, 11), (9, 13), (13, 20)], fill=(255, 255, 255, 255), width=2)
    im.save(f"{p_dir}/thunder_orb.png")
    
    # 4. Chaos Orb 24x24
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([1, 1, 22, 22], fill=(240, 20, 60, 255), outline=(255, 200, 80, 255))
    d.ellipse([5, 5, 18, 18], fill=(30, 0, 20, 255))
    d.ellipse([8, 8, 15, 15], fill=(255, 40, 80, 255))
    im.save(f"{p_dir}/chaos_orb.png")
    print("Generated boss projectiles")

if __name__ == "__main__":
    gen_inferno_assets()
    gen_frost_assets()
    gen_storm_assets()
    gen_abyss_assets()
    gen_platform_tiles()
    gen_projectiles()
