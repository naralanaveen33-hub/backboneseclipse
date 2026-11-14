import os
import math
import random
from PIL import Image, ImageDraw

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def draw_boss_body(draw, frame_type, step, scale=1.0, tint=(255, 255, 255)):
    # Canvas is 80 x 96
    cx = 40
    cy = 48
    
    # Colors
    c_armor_dark = (20, 15, 30)
    c_armor_plate = (45, 35, 65)
    c_trim = (180, 50, 90) # Crimson / Magenta trim
    c_rune_gold = (240, 190, 60)
    c_core_glow = (180, 40, 255)
    c_eye_glow = (255, 50, 80)
    
    # Offsets based on frame_type & step
    bob = int(math.sin(step * math.pi / 2.0) * 3) if frame_type == "idle" else 0
    lean = 0
    cape_spread = 0
    
    if frame_type == "running":
        bob = abs(int(math.sin(step * math.pi) * 4))
        lean = 5
        cape_spread = step * 4
    elif frame_type == "dashing":
        lean = 12
        bob = 2
        cape_spread = 14
    elif frame_type == "attacking":
        lean = 4
    elif frame_type == "ultimate":
        bob = -8 - step * 2
        cape_spread = 18 + step * 3
    elif frame_type == "stunned":
        bob = 4
        lean = -3
    elif frame_type == "hurt":
        lean = -6
        bob = -2
    elif frame_type == "teleport":
        # shrinks / fades
        pass
    elif frame_type == "death":
        bob = step * 6
    
    base_y = cy + bob
    base_x = cx + lean

    # 1. Cape / Mantle
    cape_left = base_x - 22 - cape_spread
    cape_right = base_x + 22 + cape_spread
    cape_bottom = base_y + 42
    
    # Cape back shadow
    draw.polygon([
        (base_x - 14, base_y - 12),
        (cape_left, cape_bottom),
        (base_x, cape_bottom - 6),
        (cape_right, cape_bottom),
        (base_x + 14, base_y - 12)
    ], fill=(12, 8, 22, 230), outline=(50, 20, 70, 255))
    
    # 2. Main Robes / Lower Armor
    draw.polygon([
        (base_x - 15, base_y + 6),
        (base_x - 18, base_y + 36),
        (base_x + 18, base_y + 36),
        (base_x + 15, base_y + 6)
    ], fill=c_armor_dark, outline=c_trim)
    
    # Central armor slit
    draw.line([(base_x, base_y + 8), (base_x, base_y + 34)], fill=c_core_glow, width=2)
    
    # 3. Torso Armor / Breastplate
    draw.polygon([
        (base_x - 14, base_y - 12),
        (base_x + 14, base_y - 12),
        (base_x + 11, base_y + 8),
        (base_x - 11, base_y + 8)
    ], fill=c_armor_plate, outline=c_trim)
    
    # Core Gem (Primordial Singularity)
    draw.ellipse([base_x - 5, base_y - 5, base_x + 5, base_y + 5], fill=c_core_glow, outline=c_rune_gold)
    draw.point((base_x, base_y), fill=(255, 255, 255))
    
    # 4. Pauldrons (Spiked Shoulder Guards)
    draw.polygon([
        (base_x - 14, base_y - 10),
        (base_x - 26, base_y - 20),
        (base_x - 16, base_y + 2)
    ], fill=c_armor_dark, outline=c_trim)
    
    draw.polygon([
        (base_x + 14, base_y - 10),
        (base_x + 26, base_y - 20),
        (base_x + 16, base_y + 2)
    ], fill=c_armor_dark, outline=c_trim)
    
    # 5. Head / Emperor's Greathelm & Crown
    head_y = base_y - 22
    draw.ellipse([base_x - 9, head_y - 9, base_x + 9, head_y + 9], fill=c_armor_dark, outline=c_trim)
    
    # Crown Spikes
    crown_pts = [
        (base_x - 10, head_y - 6),
        (base_x - 12, head_y - 18),
        (base_x - 6, head_y - 10),
        (base_x, head_y - 22),
        (base_x + 6, head_y - 10),
        (base_x + 12, head_y - 18),
        (base_x + 10, head_y - 6)
    ]
    draw.polygon(crown_pts, fill=c_armor_plate, outline=c_rune_gold)
    
    # Glowing Eyes
    if frame_type != "stunned" and frame_type != "death":
        draw.line([(base_x - 5, head_y - 1), (base_x - 2, head_y - 1)], fill=c_eye_glow, width=2)
        draw.line([(base_x + 2, head_y - 1), (base_x + 5, head_y - 1)], fill=c_eye_glow, width=2)
    elif frame_type == "stunned":
        # Stunned swirl eyes
        draw.line([(base_x - 5, head_y - 2), (base_x - 2, head_y)], fill=(240, 220, 50), width=1)
        draw.line([(base_x + 2, head_y), (base_x + 5, head_y - 2)], fill=(240, 220, 50), width=1)
        
    # 6. Specific action additions
    if frame_type == "attacking":
        # Dark energy scythe / blade slash
        sword_x = base_x + 22 + step * 4
        sword_y = base_y - 10 + step * 6
        draw.line([(base_x + 10, base_y), (sword_x, sword_y)], fill=(160, 40, 240), width=4)
        draw.line([(sword_x - 4, sword_y - 14), (sword_x + 8, sword_y + 14)], fill=(255, 60, 100), width=3)
        # Energy arc
        draw.arc([sword_x - 16, sword_y - 24, sword_x + 24, sword_y + 24], -60, 60, fill=(255, 200, 255), width=2)
        
    elif frame_type == "dashing":
        # Forward speed aura cones
        draw.polygon([
            (base_x + 20, base_y - 16),
            (base_x + 38, base_y),
            (base_x + 20, base_y + 16)
        ], fill=(220, 40, 100, 160), outline=(255, 220, 120, 220))
        # Trail lines behind
        draw.line([(base_x - 25, base_y - 8), (base_x - 38, base_y - 8)], fill=(180, 50, 220), width=2)
        draw.line([(base_x - 28, base_y + 8), (base_x - 42, base_y + 8)], fill=(180, 50, 220), width=2)
        
    elif frame_type == "ultimate":
        # Giant astral cosmic wings
        wing_span = 24 + step * 4
        # Left Wing
        draw.polygon([
            (base_x - 14, base_y - 10),
            (base_x - 28 - wing_span, base_y - 32 - step * 2),
            (base_x - 22, base_y + 10)
        ], fill=(140, 30, 200, 180), outline=(240, 200, 255, 240))
        # Right Wing
        draw.polygon([
            (base_x + 14, base_y - 10),
            (base_x + 28 + wing_span, base_y - 32 - step * 2),
            (base_x + 22, base_y + 10)
        ], fill=(140, 30, 200, 180), outline=(240, 200, 255, 240))
        # Raised hands & Cosmic Doom Orb above head
        orb_y = head_y - 26 - step * 2
        draw.ellipse([base_x - 14, orb_y - 14, base_x + 14, orb_y + 14], fill=(255, 40, 90, 220), outline=(255, 220, 80))
        draw.ellipse([base_x - 7, orb_y - 7, base_x + 7, orb_y + 7], fill=(255, 255, 255))
        
    elif frame_type == "stunned":
        # Orbiting stun stars & electric rings
        ring_y = head_y - 14
        draw.ellipse([base_x - 16, ring_y - 5, base_x + 16, ring_y + 5], outline=(255, 230, 40), width=2)
        for ang in [step * 1.5, step * 1.5 + 2.1, step * 1.5 + 4.2]:
            sx = base_x + int(math.cos(ang) * 15)
            sy = ring_y + int(math.sin(ang) * 5)
            draw.line([(sx - 2, sy), (sx + 2, sy)], fill=(255, 255, 200), width=2)
            draw.line([(sx, sy - 2), (sx, sy + 2)], fill=(255, 255, 200), width=2)
            
    elif frame_type == "teleport":
        # Void distortion rings
        ring_r = 12 + step * 8
        draw.ellipse([base_x - ring_r, base_y - ring_r, base_x + ring_r, base_y + ring_r], outline=(180, 50, 255, 200 - step * 40), width=3)
        # Vertical spatial slit
        draw.line([(base_x, base_y - 40), (base_x, base_y + 40)], fill=(255, 100, 200, 220 - step * 50), width=3)

    elif frame_type == "death":
        # Cosmic fracturing shards
        for i in range(8):
            ang = i * 0.78 + step * 0.3
            dist = 10 + step * 8
            sx = base_x + int(math.cos(ang) * dist)
            sy = base_y + int(math.sin(ang) * dist)
            draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 50, 120, max(0, 255 - step * 45)))

def generate_boss_sprites():
    out_dir = "assets/characters/enemies/boss_ultimate_overlord"
    os.makedirs(out_dir, exist_ok=True)
    
    animations = {
        "idle": 4,
        "running": 4,
        "teleporting": 4,
        "attacking": 4,
        "dashing": 4,
        "taking_damage": 2,
        "stunned": 3,
        "ultimate_attack": 6,
        "death": 6
    }
    
    alias_map = {
        "teleporting": "teleport",
        "taking_damage": "hurt",
        "ultimate_attack": "ultimate"
    }
    
    for anim_name, count in animations.items():
        base_type = alias_map.get(anim_name, anim_name)
        for i in range(count):
            img = Image.new("RGBA", (80, 96), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw_boss_body(draw, base_type, i)
            file_name = f"{anim_name}_{i}.png"
            img.save(os.path.join(out_dir, file_name))
            
    print("Boss sprites generated successfully in", out_dir)

def generate_ability_effects():
    eff_dir = "assets/effects/projectiles"
    os.makedirs(eff_dir, exist_ok=True)
    
    # 1. Dark Energy Orb (32x32)
    orb = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    od = ImageDraw.Draw(orb)
    od.ellipse([2, 2, 29, 29], fill=(30, 10, 45, 230), outline=(220, 50, 100))
    od.ellipse([6, 6, 25, 25], fill=(140, 20, 190, 240), outline=(255, 180, 255))
    od.ellipse([11, 11, 20, 20], fill=(255, 255, 255))
    # Swirling void tendrils
    od.arc([0, 0, 31, 31], 45, 160, fill=(255, 60, 120), width=2)
    od.arc([0, 0, 31, 31], 225, 340, fill=(180, 50, 255), width=2)
    orb.save(f"{eff_dir}/dark_energy_orb.png")
    
    # 2. Dangerous Energy Wave (48x24) - Ground slicing wave
    wave = Image.new("RGBA", (48, 24), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wave)
    # Crescent energy blade
    wd.polygon([
        (6, 23),
        (24, 1),
        (42, 23),
        (24, 12)
    ], fill=(180, 20, 90, 230), outline=(255, 220, 120))
    wd.line([(14, 22), (24, 4)], fill=(255, 255, 255), width=2)
    wd.line([(34, 22), (24, 4)], fill=(255, 255, 255), width=2)
    wave.save(f"{eff_dir}/energy_wave.png")
    
    # 3. Dark Energy Beam (128x32)
    beam = Image.new("RGBA", (128, 32), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    # Outer dark glow
    bd.rectangle([0, 2, 127, 29], fill=(50, 15, 75, 180))
    # Inner energy core
    bd.rectangle([0, 6, 127, 25], fill=(190, 30, 120, 230))
    # Super concentrated white core
    bd.rectangle([0, 11, 127, 20], fill=(255, 240, 255, 255))
    # Electric lightning forks along beam
    for x in range(0, 128, 16):
        bd.line([(x, 4), (x + 8, 27)], fill=(255, 180, 255), width=1)
    beam.save(f"{eff_dir}/dark_beam.png")
    
    # 4. Electric Shockwave (64x64)
    shock = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shock)
    sd.ellipse([4, 4, 59, 59], outline=(255, 230, 60, 240), width=4)
    sd.ellipse([10, 10, 53, 53], outline=(60, 220, 255, 220), width=3)
    sd.ellipse([18, 18, 45, 45], outline=(255, 255, 255, 180), width=2)
    # Electric sparks along perimeter
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        x1 = 32 + int(math.cos(rad) * 26)
        y1 = 32 + int(math.sin(rad) * 26)
        x2 = 32 + int(math.cos(rad) * 31)
        y2 = 32 + int(math.sin(rad) * 31)
        sd.line([(x1, y1), (x2, y2)], fill=(255, 255, 255), width=2)
    shock.save(f"{eff_dir}/electric_shockwave.png")
    
    # 5. Void Explosion (80x80)
    exp = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    ed = ImageDraw.Draw(exp)
    ed.ellipse([4, 4, 75, 75], fill=(20, 10, 35, 210), outline=(180, 30, 90))
    ed.ellipse([12, 12, 67, 67], fill=(160, 20, 140, 230), outline=(255, 120, 60))
    ed.ellipse([22, 22, 57, 57], fill=(240, 80, 40, 240), outline=(255, 230, 100))
    ed.ellipse([30, 30, 49, 49], fill=(255, 255, 255))
    # Radial blast spikes
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x1 = 40 + int(math.cos(rad) * 25)
        y1 = 40 + int(math.sin(rad) * 25)
        x2 = 40 + int(math.cos(rad) * 39)
        y2 = 40 + int(math.sin(rad) * 39)
        ed.line([(x1, y1), (x2, y2)], fill=(255, 220, 120), width=3)
    exp.save(f"{eff_dir}/void_explosion.png")
    
    # 6. Protective Shield (96x96)
    sh = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    shd = ImageDraw.Draw(sh)
    # Hexagonal / spherical rune barrier
    shd.ellipse([4, 4, 91, 91], fill=(80, 30, 140, 80), outline=(180, 60, 255, 240), width=4)
    shd.ellipse([10, 10, 85, 85], outline=(255, 120, 220, 200), width=2)
    # Hexagon points
    pts = []
    for i in range(6):
        ang = i * (math.pi / 3.0)
        pts.append((48 + int(math.cos(ang) * 40), 48 + int(math.sin(ang) * 40)))
    shd.polygon(pts, outline=(255, 240, 140, 220), width=2)
    sh.save(f"{eff_dir}/boss_shield.png")
    
    # 7. Teleport Vortex (64x64)
    vort = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vort)
    vd.ellipse([6, 6, 57, 57], fill=(15, 8, 25, 220), outline=(220, 40, 120), width=3)
    vd.arc([2, 2, 61, 61], 30, 180, fill=(180, 40, 255), width=4)
    vd.arc([2, 2, 61, 61], 210, 360, fill=(255, 100, 180), width=4)
    vd.line([(32, 4), (32, 59)], fill=(255, 255, 255), width=3)
    vd.line([(4, 32), (59, 32)], fill=(255, 255, 255), width=1)
    vort.save(f"{eff_dir}/teleport_vortex.png")
    
    # 8. Heal Aura / Siphon Rune (64x64)
    heal = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    hd = ImageDraw.Draw(heal)
    hd.ellipse([8, 8, 55, 55], outline=(50, 255, 140, 200), width=3)
    # Cross & runes
    hd.line([(32, 14), (32, 49)], fill=(120, 255, 180), width=4)
    hd.line([(14, 32), (49, 32)], fill=(120, 255, 180), width=4)
    heal.save(f"{eff_dir}/heal_aura.png")
    
    # 9. Stun Indicator Spark (24x24)
    st = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    std = ImageDraw.Draw(st)
    std.ellipse([6, 6, 17, 17], fill=(255, 240, 80), outline=(255, 180, 20))
    std.line([(12, 1), (12, 22)], fill=(255, 255, 255), width=2)
    std.line([(1, 12), (22, 12)], fill=(255, 255, 255), width=2)
    st.save(f"{eff_dir}/stun_spark.png")
    
    print("Ability effects generated successfully in", eff_dir)

def generate_level_8_environment():
    bg_dir = "assets/backgrounds/ultimate_void"
    os.makedirs(bg_dir, exist_ok=True)
    
    # 1. Ultimate Void Sky 960x540 (Cosmic Singularity with accretion disk and glowing rifts)
    sky = Image.new("RGBA", (960, 540), (0, 0, 0, 255))
    sd = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        # Deep primordial cosmic gradient
        r = int(14 + (45 - 14) * t)
        g = int(6 + (16 - 6) * t)
        b = int(28 + (60 - 28) * t)
        sd.line([(0, y), (960, y)], fill=(r, g, b, 255))
        
    # Singularity Black Hole at Center (480, 200)
    # Accretion disk glow (ellipses)
    for rad in range(160, 240, 10):
        alpha = int(90 * (1.0 - (rad - 160) / 80.0))
        sd.ellipse([480 - rad, 200 - rad//3, 480 + rad, 200 + rad//3], outline=(255, 100, 60, alpha), width=3)
        sd.ellipse([480 - rad - 5, 200 - rad//3 - 3, 480 + rad + 5, 200 + rad//3 + 3], outline=(180, 40, 220, alpha//2), width=2)
        
    # Black Hole event horizon
    sd.ellipse([480 - 75, 200 - 38, 480 + 75, 200 + 38], fill=(6, 2, 10, 255), outline=(255, 230, 180, 255), width=4)
    # Bright photon sphere ring
    sd.ellipse([480 - 82, 200 - 42, 480 + 82, 200 + 42], outline=(255, 255, 255, 160), width=2)
    
    # Twinkling cosmic stars
    for _ in range(220):
        sx = random.randint(0, 959)
        sy = random.randint(0, 539)
        bright = random.randint(160, 255)
        c = random.choice([
            (255, 255, 255, bright),
            (255, 180, 200, bright),
            (160, 220, 255, bright),
            (240, 200, 100, bright)
        ])
        sd.point((sx, sy), fill=c)
        if random.random() < 0.12:
            sd.line([(sx - 1, sy), (sx + 1, sy)], fill=c)
            sd.line([(sx, sy - 1), (sx, sy + 1)], fill=c)
            
    sky.save(f"{bg_dir}/ultimate_sky.png")
    
    # 2. Singularity Spires 960x540 (Gigantic cosmic monoliths in background)
    spires = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    spd = ImageDraw.Draw(spires)
    
    spire_peaks = [
        (80, 220), (200, 170), (330, 240), (450, 190), 
        (580, 180), (710, 230), (840, 160), (920, 210)
    ]
    for px, py in spire_peaks:
        spd.polygon([
            (px - 45, 540),
            (px - 14, py + 30),
            (px, py),
            (px + 14, py + 30),
            (px + 45, 540)
        ], fill=(22, 12, 34, 210), outline=(140, 40, 110, 240))
        # Cosmic rune line along spine
        spd.line([(px, py + 10), (px, 540)], fill=(220, 60, 140, 180), width=2)
    spires.save(f"{bg_dir}/singularity_spires.png")
    
    # 3. Celestial Pillars 960x540 (Midground floating obelisks)
    pillars = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    pld = ImageDraw.Draw(pillars)
    pillar_pos = [60, 180, 310, 440, 570, 700, 830]
    for x in pillar_pos:
        pld.polygon([
            (x - 22, 540),
            (x - 16, 260),
            (x, 240),
            (x + 16, 260),
            (x + 22, 540)
        ], fill=(30, 16, 45, 230), outline=(220, 80, 160, 255))
        # Glowing runes
        for ry in range(290, 500, 45):
            pld.rectangle([x - 6, ry, x + 6, ry + 12], fill=(255, 60, 120, 200), outline=(255, 240, 140))
    pillars.save(f"{bg_dir}/celestial_pillars.png")
    
    # 4. Tiles: Platform 160x32 & Platform 80x24
    tile_dir = "assets/tiles"
    os.makedirs(tile_dir, exist_ok=True)
    
    p160 = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
    p160d = ImageDraw.Draw(p160)
    p160d.rounded_rectangle([0, 0, 159, 31], radius=4, fill=(28, 18, 42, 255), outline=(180, 40, 120, 255), width=2)
    # Glowing top walking edge
    p160d.line([(2, 2), (157, 2)], fill=(255, 120, 200), width=2)
    p160d.line([(4, 4), (155, 4)], fill=(240, 220, 100), width=1)
    # Engraved runes
    for rx in range(18, 150, 24):
        p160d.rectangle([rx, 10, rx + 10, 22], fill=(120, 30, 90, 200), outline=(255, 60, 140))
        p160d.line([(rx + 5, 12), (rx + 5, 20)], fill=(255, 240, 160))
    p160.save(f"{tile_dir}/platform_ultimate_160.png")
    
    p80 = Image.new("RGBA", (80, 24), (0, 0, 0, 0))
    p80d = ImageDraw.Draw(p80)
    p80d.rounded_rectangle([0, 0, 79, 23], radius=3, fill=(28, 18, 42, 255), outline=(180, 40, 120, 255), width=2)
    p80d.line([(2, 2), (77, 2)], fill=(255, 120, 200), width=2)
    for rx in range(12, 70, 20):
        p80d.rectangle([rx, 7, rx + 8, 17], fill=(120, 30, 90, 200), outline=(255, 60, 140))
    p80.save(f"{tile_dir}/platform_ultimate_80.png")
    
    print("Level 8 backgrounds and tiles generated successfully!")

if __name__ == "__main__":
    generate_boss_sprites()
    generate_ability_effects()
    generate_level_8_environment()
