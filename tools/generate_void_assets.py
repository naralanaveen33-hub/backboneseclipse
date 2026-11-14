import os
import math
import random
from PIL import Image, ImageDraw

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def gen_void_assets():
    # 1. Backgrounds
    b_dir = "assets/backgrounds/void"
    ensure_dir(f"{b_dir}/void_sky.png")
    
    # Void Sky 960x540 (Cosmic deep indigo/cyan nebula gradient with stars and galaxies)
    sky = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
    sd = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        # Deep space gradient from dark cosmic blue to eerie violet-cyan
        r = int(8 + (35 - 8) * t)
        g = int(4 + (18 - 4) * t)
        b = int(24 + (55 - 24) * t)
        sd.line([(0, y), (960, y)], fill=(r, g, b, 255))
        
    # Draw cosmic nebula clouds
    for _ in range(12):
        nx = random.randint(100, 860)
        ny = random.randint(80, 460)
        nr = random.randint(70, 160)
        color = random.choice([
            (70, 30, 120, 60),
            (30, 70, 140, 55),
            (110, 40, 160, 50),
            (30, 120, 160, 45)
        ])
        sd.ellipse([nx - nr, ny - nr//2, nx + nr, ny + nr//2], fill=color)
        
    # Distant twinkling stars & constellations
    for _ in range(140):
        sx = random.randint(0, 959)
        sy = random.randint(0, 539)
        bright = random.randint(180, 255)
        c = random.choice([
            (255, 255, 255, bright),
            (160, 230, 255, bright),
            (230, 180, 255, bright),
            (255, 240, 160, bright)
        ])
        sd.point((sx, sy), fill=c)
        if random.random() < 0.15:
            sd.line([(sx - 1, sy), (sx + 1, sy)], fill=c)
            sd.line([(sx, sy - 1), (sx, sy + 1)], fill=c)
            
    # Giant shattered Celestial Moon
    sd.ellipse([720, 60, 840, 180], fill=(160, 210, 255, 220))
    sd.ellipse([705, 45, 855, 195], fill=(100, 180, 255, 50))
    # Crater rings
    sd.ellipse([750, 90, 780, 120], fill=(130, 180, 230, 220))
    sd.ellipse([790, 130, 815, 155], fill=(130, 180, 230, 220))
    sky.save(f"{b_dir}/void_sky.png")

    # Void Spires 960x540 (Floating cosmic shattered citadel towers)
    spires = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    spd = ImageDraw.Draw(spires)
    for sx in (100, 260, 430, 620, 810):
        w = 46
        h = random.randint(240, 360)
        # Inverted / floating citadel fragments
        spd.rectangle([sx - w//2, 540 - h, sx + w//2, 540], fill=(22, 18, 38, 220))
        # Spire peak with floating jewel
        spd.polygon([(sx - w//2 - 6, 540 - h), (sx, 540 - h - 60), (sx + w//2 + 6, 540 - h)], fill=(32, 25, 52, 230))
        spd.ellipse([sx - 6, 540 - h - 75, sx + 6, 540 - h - 63], fill=(120, 220, 255, 240))
    spires.save(f"{b_dir}/void_spires.png")

    # Void Interior / Arch 960x540 (Ethereal rune pillars and astral portals)
    interior = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    ind = ImageDraw.Draw(interior)
    for px in (180, 500, 820):
        ind.rectangle([px - 26, 0, px + 26, 540], fill=(28, 24, 48, 160))
        # Cosmic rune arches
        ind.arc([px - 180, 30, px + 180, 220], start=180, end=0, fill=(70, 50, 110, 170), width=16)
        # Glowing cyan runes along pillar
        for ry in range(120, 480, 60):
            ind.ellipse([px - 5, ry, px + 5, ry + 12], fill=(100, 240, 255, 200))
    interior.save(f"{b_dir}/void_interior.png")

    # 2. Void Platforms
    t_dir = "assets/tiles"
    ensure_dir(f"{t_dir}/platform_void_160.png")
    
    # Astral Platform 160x32
    im = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 159, 31], fill=(30, 25, 48, 255))
    # Glowing celestial crystal edge
    d.line([(0, 0), (159, 0)], fill=(120, 240, 255, 255), width=2)
    d.line([(0, 2), (159, 2)], fill=(80, 160, 240, 255), width=1)
    # Astral runes
    for x in range(20, 150, 30):
        d.line([(x, 10), (x + 8, 22)], fill=(160, 90, 255, 220), width=2)
        d.line([(x + 8, 10), (x, 22)], fill=(160, 90, 255, 220), width=2)
    d.line([(0, 31), (159, 31)], fill=(60, 45, 90, 255), width=1)
    im.save(f"{t_dir}/platform_void_160.png")

    # Astral Platform 80x24 (Floating)
    im = Image.new("RGBA", (80, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(4, 23), (75, 23), (79, 2), (0, 2)], fill=(35, 28, 55, 255))
    d.line([(0, 0), (79, 0)], fill=(130, 245, 255, 255), width=2)
    d.ellipse([34, 8, 46, 18], fill=(160, 100, 255, 220))
    d.ellipse([37, 11, 43, 15], fill=(240, 255, 255, 255))
    im.save(f"{t_dir}/platform_void_80.png")

    # Void Rift Hazard 160x32 (Dark purple swirling cosmic energy that damages player)
    im = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 4, 159, 31], fill=(25, 10, 40, 255))
    d.line([(0, 4), (159, 4)], fill=(180, 50, 255, 255), width=3)
    d.line([(0, 7), (159, 7)], fill=(120, 220, 255, 255), width=2)
    for x in range(10, 160, 20):
        d.ellipse([x - 6, 12, x + 6, 26], fill=(150, 40, 220, 180))
    im.save(f"{t_dir}/void_rift.png")

    # 3. Supreme Boss Sprites: The Celestial Void Monarch (64x80)
    c_dir = "assets/characters/enemies/boss_void_monarch"
    ensure_dir(f"{c_dir}/idle_0.png")
    
    # Idle (4 frames)
    for f in range(4):
        im = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy = 32, 40 + int(math.sin(f * math.pi / 2.0) * 3)
        # Flowing Astral Robes
        d.polygon([(cx - 20, cy + 34), (cx - 12, cy + 4), (cx + 12, cy + 4), (cx + 20, cy + 34)], fill=(20, 15, 40, 255))
        d.polygon([(cx - 14, cy + 32), (cx - 8, cy + 6), (cx + 8, cy + 6), (cx + 14, cy + 32)], fill=(65, 30, 110, 255))
        # Celestial Torso Armor
        d.rectangle([cx - 10, cy - 10, cx + 10, cy + 6], fill=(30, 25, 55, 255))
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 2], fill=(120, 240, 255, 255))
        # Celestial Mask / Mystery Hood
        d.ellipse([cx - 9, cy - 24, cx + 9, cy - 10], fill=(220, 230, 255, 255))
        # Piercing Void Eyes
        d.point((cx - 4, cy - 18), fill=(180, 50, 255, 255))
        d.point((cx + 4, cy - 18), fill=(180, 50, 255, 255))
        # Floating Crown of Celestial Orbs
        for i in range(5):
            angle = (f * 0.4) + i * (math.pi / 2.5)
            ox = cx + int(math.cos(angle) * 18)
            oy = cy - 28 + int(math.sin(angle) * 6)
            d.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=(140, 235, 255, 255))
        # Cosmic Void Staff
        staff_x = cx + 22
        d.line([(staff_x, cy - 34), (staff_x, cy + 28)], fill=(60, 45, 90, 255), width=3)
        d.ellipse([staff_x - 6, cy - 42, staff_x + 6, cy - 30], fill=(180, 60, 255, 255))
        d.ellipse([staff_x - 3, cy - 39, staff_x + 3, cy - 33], fill=(255, 255, 255, 255))
        im.save(f"{c_dir}/idle_{f}.png")
        
    # Cast (4 frames)
    for f in range(4):
        im = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy = 32, 38
        d.polygon([(cx - 24, cy + 34), (cx + 24, cy + 34), (cx, cy - 26)], fill=(35, 20, 65, 255))
        # Massive celestial energy orb above
        staff_x = cx + 18
        r = 14 + f * 3
        d.ellipse([staff_x - r, cy - 44 - r, staff_x + r, cy - 44 + r], fill=(140, 40, 255, 180))
        d.ellipse([staff_x - r//2, cy - 44 - r//2, staff_x + r//2, cy - 44 + r//2], fill=(180, 240, 255, 240))
        d.ellipse([staff_x - 4, cy - 48, staff_x + 4, cy - 40], fill=(255, 255, 255, 255))
        im.save(f"{c_dir}/cast_{f}.png")

    # Teleport (4 frames)
    for f in range(4):
        im = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        r = int(28 * (1.0 - f / 4.0))
        if r > 0:
            d.ellipse([32 - r, 40 - r, 32 + r, 40 + r], fill=(140, 40, 240, 180))
            d.ellipse([32 - r//2, 40 - r//2, 32 + r//2, 40 + r//2], fill=(180, 245, 255, 220))
        im.save(f"{c_dir}/teleport_{f}.png")

    # Hurt (2 frames)
    for f in range(2):
        im = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle([14, 12, 50, 72], fill=(255, 80, 120, 255))
        im.save(f"{c_dir}/hurt_{f}.png")

    # Death (6 frames)
    for f in range(6):
        im = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = max(0, 255 - f * 42)
        d.ellipse([32 - (26 - f * 4), 40 - (32 - f * 5), 32 + (26 - f * 4), 40 + (32 - f * 5)], fill=(120, 30, 200, alpha))
        for _ in range(12):
            rx = random.randint(12, 52)
            ry = random.randint(10, 70)
            d.point((rx, ry), fill=(160, 240, 255, alpha))
        im.save(f"{c_dir}/death_{f}.png")

    # 4. Void Ray / Astral Projectile (32x32)
    ensure_dir("assets/effects/projectiles/astral_orb_0.png")
    for f in range(4):
        im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy = 16, 16
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(140, 30, 240, 190), outline=(140, 240, 255, 255), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
        # Astral star rays
        for a in (0, math.pi/2, math.pi, 3*math.pi/2):
            th = a + f * (math.pi / 4.0)
            x1 = cx + int(math.cos(th) * 14)
            y1 = cy + int(math.sin(th) * 14)
            d.line([(cx, cy), (x1, y1)], fill=(180, 240, 255, 220), width=1)
        im.save(f"assets/effects/projectiles/astral_orb_{f}.png")

    print("Generated all Level 3 Astral Void assets successfully!")

if __name__ == "__main__":
    gen_void_assets()
