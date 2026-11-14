import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

# Palette definitions
COLOR_TRANSPARENT = (0, 0, 0, 0)

# Wizard Palette
WIZ_ROBE_DARK = (40, 25, 75, 255)
WIZ_ROBE_MID = (75, 45, 130, 255)
WIZ_ROBE_LIGHT = (115, 75, 185, 255)
WIZ_GOLD = (235, 185, 55, 255)
WIZ_SKIN = (255, 215, 180, 255)
WIZ_BEARD = (220, 230, 245, 255)
WIZ_HAT_DARK = (28, 18, 55, 255)
WIZ_STAFF_WOOD = (110, 65, 35, 255)
WIZ_GEM_CYAN = (80, 240, 255, 255)
WIZ_GEM_GLOW = (150, 255, 255, 180)

def draw_wizard_base(im, pose="idle", frame=0):
    draw = ImageDraw.Draw(im)
    w, h = im.size
    cx, cy = w // 2, h // 2 + 6
    
    # Offsets based on animation
    bob = int(math.sin(frame * math.pi / 2.0) * 2) if pose in ("idle", "run") else 0
    leg_offset = int(math.sin(frame * math.pi) * 3) if pose == "run" else 0
    
    if pose == "jump":
        bob = -4
    elif pose == "fall":
        bob = 3
    elif pose == "hurt":
        bob = 1
        cx -= 3
        
    y = cy + bob
    
    # Robe / Body
    # Skirt / lower robe
    robe_points = [
        (cx - 10, y + 14),
        (cx - 6 - leg_offset, y + 3),
        (cx + 6 + leg_offset, y + 3),
        (cx + 10, y + 14)
    ]
    draw.polygon(robe_points, fill=WIZ_ROBE_MID)
    draw.polygon([(cx - 8, y + 14), (cx - 4, y + 4), (cx + 4, y + 4), (cx + 8, y + 14)], fill=WIZ_ROBE_LIGHT)
    # Gold hem
    draw.line([(cx - 10, y + 14), (cx + 10, y + 14)], fill=WIZ_GOLD, width=2)
    
    # Upper chest
    draw.rectangle([cx - 7, y - 5, cx + 7, y + 3], fill=WIZ_ROBE_DARK)
    draw.rectangle([cx - 4, y - 4, cx + 4, y + 2], fill=WIZ_ROBE_MID)
    # Gold collar / buckle
    draw.rectangle([cx - 2, y - 2, cx + 2, y], fill=WIZ_GOLD)
    
    # Head & Face
    draw.rectangle([cx - 5, y - 13, cx + 5, y - 6], fill=WIZ_SKIN)
    # Eyes
    eye_x = cx + 2 if pose != "hurt" else cx + 1
    draw.point((eye_x, y - 10), fill=(25, 25, 35, 255))
    draw.point((eye_x + 3, y - 10), fill=(25, 25, 35, 255))
    
    # Beard
    draw.polygon([(cx - 4, y - 8), (cx + 4, y - 8), (cx + 1, y - 1), (cx - 2, y - 1)], fill=WIZ_BEARD)
    
    # Wizard Hat
    hat_brim_y = y - 12
    draw.line([(cx - 11, hat_brim_y), (cx + 11, hat_brim_y)], fill=WIZ_HAT_DARK, width=2)
    draw.line([(cx - 8, hat_brim_y - 1), (cx + 8, hat_brim_y - 1)], fill=WIZ_GOLD, width=1)
    # Cone
    tip_dx = -3 if pose == "run" else 2
    hat_points = [
        (cx - 7, hat_brim_y - 2),
        (cx + 7, hat_brim_y - 2),
        (cx + tip_dx, hat_brim_y - 16)
    ]
    draw.polygon(hat_points, fill=WIZ_HAT_DARK)
    draw.polygon([(cx - 4, hat_brim_y - 2), (cx + 2, hat_brim_y - 2), (cx + tip_dx, hat_brim_y - 14)], fill=WIZ_ROBE_MID)
    # Hat buckle star
    draw.point((cx, hat_brim_y - 2), fill=WIZ_GOLD)
    
    # Staff
    staff_x = cx + 12
    staff_y = y - 4
    if pose == "attack":
        staff_x = cx + 16
        staff_y = y - 10
    draw.line([(staff_x, staff_y - 12), (staff_x, staff_y + 16)], fill=WIZ_STAFF_WOOD, width=2)
    # Gem orb atop staff
    draw.ellipse([staff_x - 3, staff_y - 17, staff_x + 3, staff_y - 11], fill=WIZ_GEM_CYAN)
    draw.ellipse([staff_x - 1, staff_y - 15, staff_x + 1, staff_y - 13], fill=(255, 255, 255, 255))
    
    # Casting glow if attack
    if pose == "attack":
        glow_r = 6 + frame * 2
        draw.ellipse([staff_x - glow_r, staff_y - 14 - glow_r, staff_x + glow_r, staff_y - 14 + glow_r], fill=WIZ_GEM_GLOW)
        draw.line([(staff_x, staff_y - 14 - glow_r - 2), (staff_x, staff_y - 14 + glow_r + 2)], fill=(255, 255, 255, 200))
        draw.line([(staff_x - glow_r - 2, staff_y - 14), (staff_x + glow_r + 2, staff_y - 14)], fill=(255, 255, 255, 200))
        
    # Hurt flash
    if pose == "hurt":
        overlay = Image.new("RGBA", im.size, (255, 60, 60, 90))
        im.alpha_composite(overlay)

def generate_wizard():
    base_dir = "assets/characters/wizard"
    # Idle (4 frames)
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        draw_wizard_base(im, "idle", f)
        im.save(f"{base_dir}/idle_{f}.png")
        
    # Run (6 frames)
    for f in range(6):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        draw_wizard_base(im, "run", f)
        im.save(f"{base_dir}/run_{f}.png")
        
    # Jump (2 frames)
    for f in range(2):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        draw_wizard_base(im, "jump", f)
        im.save(f"{base_dir}/jump_{f}.png")
        
    # Fall (2 frames)
    for f in range(2):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        draw_wizard_base(im, "fall", f)
        im.save(f"{base_dir}/fall_{f}.png")
        
    # Attack (4 frames)
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        draw_wizard_base(im, "attack", f)
        im.save(f"{base_dir}/attack_{f}.png")
        
    # Hurt (2 frames)
    for f in range(2):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        draw_wizard_base(im, "hurt", f)
        im.save(f"{base_dir}/hurt_{f}.png")
        
    # Death (6 frames - dissolves into magical spark)
    for f in range(6):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        alpha = max(0, 255 - f * 42)
        draw_wizard_base(im, "hurt", 0)
        # Dissolve effect
        pix = im.load()
        for x in range(48):
            for y in range(48):
                r, g, b, a = pix[x, y]
                if a > 0:
                    if random.random() < (f / 5.5):
                        pix[x, y] = (0, 0, 0, 0)
                    else:
                        pix[x, y] = (r, g, b, min(a, alpha))
        # Draw magic dispersal sparks
        d = ImageDraw.Draw(im)
        for _ in range(8 + f * 4):
            sx = random.randint(12, 36)
            sy = random.randint(10, 40) - f * 3
            d.point((sx, sy), fill=(100, 230, 255, alpha))
        im.save(f"{base_dir}/death_{f}.png")
        
    # Respawn (6 frames - magic beam descends and wizard coalesces)
    for f in range(6):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        # Beam of light
        beam_alpha = int(120 + 80 * math.sin(f * 0.8))
        d.rectangle([18, 0, 30, 48], fill=(120, 220, 255, beam_alpha))
        d.line([(24, 0), (24, 48)], fill=(255, 255, 255, beam_alpha + 40), width=3)
        # Swirling runes
        for i in range(4):
            rx = int(24 + 14 * math.cos(f * 1.2 + i * 1.5))
            ry = int(36 - f * 4 + 6 * math.sin(f * 1.2 + i * 1.5))
            d.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=WIZ_GOLD)
        # Wizard appearing
        if f >= 2:
            wiz_temp = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
            draw_wizard_base(wiz_temp, "idle", 0)
            alpha_mult = (f - 1) / 4.0
            pix = wiz_temp.load()
            for x in range(48):
                for y in range(48):
                    r, g, b, a = pix[x, y]
                    if a > 0:
                        pix[x, y] = (r, g, b, int(a * alpha_mult))
            im.alpha_composite(wiz_temp)
        im.save(f"{base_dir}/respawn_{f}.png")
    print("Generated wizard animations")

def generate_enemies():
    # 1. Shadow Monster (48x48)
    base_dir = "assets/characters/enemies/shadow_monster"
    ensure_dir(f"{base_dir}/walk_0.png")
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        # Shadow beast body
        cx, cy = 24, 26 + int(math.sin(f * math.pi / 2.0) * 2)
        # Claws / legs
        leg_step = int(math.sin(f * math.pi) * 4)
        d.line([(cx - 10, cy + 8), (cx - 12 - leg_step, cy + 18)], fill=(20, 15, 30, 255), width=3)
        d.line([(cx + 10, cy + 8), (cx + 12 + leg_step, cy + 18)], fill=(20, 15, 30, 255), width=3)
        # Torso
        d.ellipse([cx - 14, cy - 8, cx + 14, cy + 12], fill=(25, 20, 38, 255))
        d.ellipse([cx - 10, cy - 5, cx + 10, cy + 8], fill=(45, 35, 65, 255))
        # Spikes on back
        d.polygon([(cx - 12, cy - 6), (cx - 18, cy - 14), (cx - 6, cy - 8)], fill=(15, 10, 25, 255))
        d.polygon([(cx - 4, cy - 8), (cx - 6, cy - 18), (cx + 2, cy - 8)], fill=(15, 10, 25, 255))
        # Head / Jaws
        d.ellipse([cx + 4, cy - 12, cx + 16, cy + 2], fill=(30, 25, 45, 255))
        # Glowing Red Eyes
        d.rectangle([cx + 10, cy - 8, cx + 14, cy - 6], fill=(255, 40, 50, 255))
        # Teeth
        d.line([(cx + 8, cy), (cx + 14, cy)], fill=(230, 230, 240, 255), width=2)
        im.save(f"{base_dir}/walk_{f}.png")
        
    for f in range(3):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24 + f * 3, 24
        d.ellipse([cx - 14, cy - 8, cx + 14, cy + 12], fill=(30, 20, 45, 255))
        # Glowing swipe claw
        d.arc([cx + 6, cy - 16, cx + 24, cy + 16], start=-90, end=45, fill=(255, 50, 60, 255), width=3)
        d.rectangle([cx + 8, cy - 8, cx + 12, cy - 6], fill=(255, 40, 50, 255))
        im.save(f"{base_dir}/attack_{f}.png")
        
    for f in range(2):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        d.ellipse([10, 16, 38, 36], fill=(180, 40, 60, 255))
        d.rectangle([28, 20, 32, 22], fill=(255, 255, 255, 255))
        im.save(f"{base_dir}/hurt_{f}.png")
        
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        r = 16 - f * 3
        alpha = max(0, 255 - f * 60)
        d.ellipse([24 - r, 24 - r, 24 + r, 24 + r], fill=(45, 25, 60, alpha))
        im.save(f"{base_dir}/death_{f}.png")

    # 2. Flying Bat (32x32)
    base_dir = "assets/characters/enemies/flying_bat"
    ensure_dir(f"{base_dir}/fly_0.png")
    for f in range(4):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 16, 16
        wing_y = cy - 8 if f in (0, 2) else cy + 4
        # Body
        d.ellipse([cx - 4, cy - 5, cx + 4, cy + 6], fill=(40, 30, 50, 255))
        # Ears
        d.polygon([(cx - 3, cy - 5), (cx - 5, cy - 10), (cx - 1, cy - 5)], fill=(30, 20, 40, 255))
        d.polygon([(cx + 3, cy - 5), (cx + 5, cy - 10), (cx + 1, cy - 5)], fill=(30, 20, 40, 255))
        # Red eyes
        d.point((cx - 2, cy - 2), fill=(255, 40, 60, 255))
        d.point((cx + 2, cy - 2), fill=(255, 40, 60, 255))
        # Wings
        d.polygon([(cx - 3, cy), (cx - 14, wing_y), (cx - 8, cy + 4)], fill=(65, 40, 85, 255))
        d.polygon([(cx + 3, cy), (cx + 14, wing_y), (cx + 8, cy + 4)], fill=(65, 40, 85, 255))
        im.save(f"{base_dir}/fly_{f}.png")
        
    for f in range(2):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        d.ellipse([12, 12, 20, 22], fill=(240, 60, 80, 255))
        im.save(f"{base_dir}/hurt_{f}.png")
        
    for f in range(3):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        d.ellipse([16 - (4 - f), 16 - (4 - f), 16 + (4 - f), 16 + (4 - f)], fill=(120, 40, 150, 180 - f * 60))
        im.save(f"{base_dir}/death_{f}.png")

    # 3. Fire Demon (48x48)
    base_dir = "assets/characters/enemies/fire_demon"
    ensure_dir(f"{base_dir}/idle_0.png")
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24, 24 + int(math.sin(f * math.pi / 2.0) * 2)
        # Molten Rock Body
        d.polygon([(cx - 12, cy + 16), (cx + 12, cy + 16), (cx + 14, cy - 4), (cx - 14, cy - 4)], fill=(50, 30, 30, 255))
        # Magma cracks
        d.line([(cx - 6, cy + 12), (cx + 4, cy + 2)], fill=(255, 120, 30, 255), width=2)
        d.line([(cx - 2, cy + 6), (cx + 8, cy + 14)], fill=(255, 200, 40, 255), width=1)
        # Horned head
        d.ellipse([cx - 9, cy - 14, cx + 9, cy - 2], fill=(40, 20, 20, 255))
        # Horns
        d.polygon([(cx - 7, cy - 10), (cx - 14, cy - 18), (cx - 3, cy - 12)], fill=(180, 50, 30, 255))
        d.polygon([(cx + 7, cy - 10), (cx + 14, cy - 18), (cx + 3, cy - 12)], fill=(180, 50, 30, 255))
        # Fiery eyes & mouth
        d.rectangle([cx - 5, cy - 9, cx - 2, cy - 7], fill=(255, 240, 60, 255))
        d.rectangle([cx + 2, cy - 9, cx + 5, cy - 7], fill=(255, 240, 60, 255))
        d.line([(cx - 3, cy - 4), (cx + 3, cy - 4)], fill=(255, 100, 20, 255), width=2)
        # Flame aura
        flame_h = 4 + int(math.sin((f + 1) * math.pi) * 3)
        d.polygon([(cx - 6, cy - 14), (cx, cy - 16 - flame_h), (cx + 6, cy - 14)], fill=(255, 140, 20, 200))
        im.save(f"{base_dir}/idle_{f}.png")
        
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24, 24
        d.ellipse([cx - 12, cy - 10, cx + 12, cy + 14], fill=(70, 35, 30, 255))
        # Raised flame hands launching fireball
        hand_x = cx + 14
        hand_y = cy - 6
        d.ellipse([hand_x - 6, hand_y - 6, hand_x + 6, hand_y + 6], fill=(255, 140, 30, 255))
        d.ellipse([hand_x - 3, hand_y - 3, hand_x + 3, hand_y + 3], fill=(255, 240, 80, 255))
        im.save(f"{base_dir}/attack_{f}.png")
        
    for f in range(2):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        d.ellipse([12, 12, 36, 36], fill=(255, 100, 80, 255))
        im.save(f"{base_dir}/hurt_{f}.png")
        
    for f in range(5):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        for _ in range(12):
            rx = random.randint(10, 38)
            ry = random.randint(10, 38)
            d.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=(255, 120, 30, max(0, 255 - f * 50)))
        im.save(f"{base_dir}/death_{f}.png")

    # 4. Level 1 Mini-Boss: Shadow Behemoth (64x64)
    base_dir = "assets/characters/enemies/boss_mini"
    ensure_dir(f"{base_dir}/idle_0.png")
    for f in range(4):
        im = Image.new("RGBA", (64, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 32, 34 + int(math.sin(f * math.pi / 2.0) * 2)
        # Giant Dark Torso
        d.ellipse([cx - 22, cy - 16, cx + 22, cy + 20], fill=(20, 15, 32, 255))
        d.ellipse([cx - 16, cy - 10, cx + 16, cy + 14], fill=(38, 28, 55, 255))
        # Spikes / Armor
        for sx in (-16, -8, 0, 8, 16):
            d.polygon([(cx + sx - 3, cy - 14), (cx + sx, cy - 24), (cx + sx + 3, cy - 14)], fill=(65, 45, 90, 255))
        # Huge glowing visor/slit
        d.rectangle([cx - 10, cy - 6, cx + 10, cy - 2], fill=(255, 30, 60, 255))
        d.rectangle([cx - 6, cy - 5, cx + 6, cy - 3], fill=(255, 200, 210, 255))
        # Massive fists
        fist_offset = int(math.cos(f * math.pi) * 3)
        d.ellipse([cx - 26, cy + 6 + fist_offset, cx - 14, cy + 18 + fist_offset], fill=(25, 20, 40, 255))
        d.ellipse([cx + 14, cy + 6 - fist_offset, cx + 26, cy + 18 - fist_offset], fill=(25, 20, 40, 255))
        im.save(f"{base_dir}/idle_{f}.png")
        
    for f in range(4):
        im = Image.new("RGBA", (64, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 32, 32
        d.ellipse([cx - 24, cy - 14, cx + 24, cy + 20], fill=(25, 18, 38, 255))
        # Ground slam impact shockwave
        if f >= 2:
            d.arc([cx - 28, cy + 16, cx + 28, cy + 30], start=0, end=180, fill=(255, 50, 80, 255), width=4)
        im.save(f"{base_dir}/attack_{f}.png")
        
    for f in range(2):
        im = Image.new("RGBA", (64, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        d.ellipse([14, 14, 50, 52], fill=(200, 40, 70, 255))
        im.save(f"{base_dir}/hurt_{f}.png")
        
    for f in range(6):
        im = Image.new("RGBA", (64, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        alpha = max(0, 255 - f * 42)
        d.ellipse([32 - (24 - f * 3), 34 - (20 - f * 2), 32 + (24 - f * 3), 34 + (20 - f * 2)], fill=(35, 20, 50, alpha))
        im.save(f"{base_dir}/death_{f}.png")

    # 5. Level 2 Final Boss: Dark Wizard (48x64)
    base_dir = "assets/characters/enemies/boss_dark_wizard"
    ensure_dir(f"{base_dir}/idle_0.png")
    for f in range(4):
        im = Image.new("RGBA", (48, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24, 30 + int(math.sin(f * math.pi / 2.0) * 3)
        # Flowing dark robes
        d.polygon([(cx - 14, cy + 24), (cx - 10, cy + 4), (cx + 10, cy + 4), (cx + 14, cy + 24)], fill=(15, 12, 25, 255))
        d.polygon([(cx - 10, cy + 22), (cx - 6, cy + 6), (cx + 6, cy + 6), (cx + 10, cy + 22)], fill=(45, 18, 65, 255))
        # Torso
        d.rectangle([cx - 8, cy - 8, cx + 8, cy + 4], fill=(22, 16, 35, 255))
        # Floating Skull mask / Horned crown
        d.polygon([(cx - 7, cy - 24), (cx - 4, cy - 14), (cx, cy - 26), (cx + 4, cy - 14), (cx + 7, cy - 24)], fill=(180, 160, 210, 255))
        d.ellipse([cx - 6, cy - 18, cx + 6, cy - 8], fill=(230, 225, 240, 255))
        # Glowing purple eye sockets
        d.point((cx - 3, cy - 14), fill=(160, 40, 255, 255))
        d.point((cx + 3, cy - 14), fill=(160, 40, 255, 255))
        # Dark Magic Staff
        staff_x = cx + 14
        d.line([(staff_x, cy - 22), (staff_x, cy + 18)], fill=(35, 28, 45, 255), width=2)
        # Skull or dark crystal atop staff
        d.ellipse([staff_x - 4, cy - 26, staff_x + 4, cy - 18], fill=(180, 40, 255, 255))
        d.ellipse([staff_x - 2, cy - 24, staff_x + 2, cy - 20], fill=(255, 255, 255, 255))
        im.save(f"{base_dir}/idle_{f}.png")
        
    for f in range(4):
        im = Image.new("RGBA", (48, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24, 28
        d.polygon([(cx - 16, cy + 24), (cx + 16, cy + 24), (cx, cy - 20)], fill=(30, 15, 50, 255))
        # Staff raised with massive dark energy orb
        staff_x = cx + 12
        d.ellipse([staff_x - 10, cy - 32, staff_x + 10, cy - 12], fill=(160, 20, 240, 200))
        d.ellipse([staff_x - 5, cy - 27, staff_x + 5, cy - 17], fill=(255, 200, 255, 255))
        im.save(f"{base_dir}/cast_{f}.png")
        
    # Teleport (4 frames)
    for f in range(4):
        im = Image.new("RGBA", (48, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        r = int(22 * (1.0 - f / 4.0))
        if r > 0:
            d.ellipse([24 - r, 32 - r, 24 + r, 32 + r], fill=(120, 20, 200, 200))
            d.ellipse([24 - r//2, 32 - r//2, 24 + r//2, 32 + r//2], fill=(255, 255, 255, 220))
        im.save(f"{base_dir}/teleport_{f}.png")
        
    for f in range(2):
        im = Image.new("RGBA", (48, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        d.rectangle([12, 10, 36, 54], fill=(255, 60, 100, 255))
        im.save(f"{base_dir}/hurt_{f}.png")
        
    for f in range(6):
        im = Image.new("RGBA", (48, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        alpha = max(0, 255 - f * 42)
        d.ellipse([24 - (16 - f * 2), 32 - (24 - f * 3), 24 + (16 - f * 2), 32 + (24 - f * 3)], fill=(80, 20, 120, alpha))
        im.save(f"{base_dir}/death_{f}.png")
    print("Generated enemy sprites")

def generate_abilities_and_effects():
    # 1. Fireball (32x32)
    base_dir = "assets/effects/projectiles"
    ensure_dir(f"{base_dir}/fireball_0.png")
    for f in range(4):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 18, 16
        # Fiery tail
        d.polygon([(cx - 16, cy + random.randint(-4, 4)), (cx, cy - 6), (cx, cy + 6)], fill=(255, 100, 20, 180))
        # Core
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 140, 20, 255))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 220, 40, 255))
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 240, 255))
        im.save(f"{base_dir}/fireball_{f}.png")
        
    # Fire explosion (48x48, 5 frames)
    for f in range(5):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        r = 6 + f * 4
        alpha = max(0, 255 - f * 45)
        d.ellipse([24 - r, 24 - r, 24 + r, 24 + r], fill=(255, 80 + f * 20, 20, alpha))
        if r > 4:
            d.ellipse([24 - r//2, 24 - r//2, 24 + r//2, 24 + r//2], fill=(255, 220, 50, alpha))
        im.save(f"{base_dir}/explosion_{f}.png")
        
    # 2. Ice Blast (32x32, 4 frames)
    for f in range(4):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 16, 16
        angle = f * (math.pi / 4.0)
        # Snowflake crystal shards
        for a in [0, math.pi/2, math.pi, 3*math.pi/2, math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]:
            th = a + angle
            x1 = cx + int(math.cos(th) * 11)
            y1 = cy + int(math.sin(th) * 11)
            d.line([(cx, cy), (x1, y1)], fill=(120, 240, 255, 255), width=2)
            d.point((x1, y1), fill=(255, 255, 255, 255))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(220, 255, 255, 255))
        im.save(f"{base_dir}/ice_blast_{f}.png")
        
    # Ice Freeze Overlay (48x48)
    im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, 44, 44], fill=(120, 210, 255, 140), outline=(200, 245, 255, 230), width=2)
    # Ice facet reflections
    d.line([(8, 8), (20, 8), (12, 40)], fill=(255, 255, 255, 160), width=2)
    d.line([(28, 40), (40, 40)], fill=(255, 255, 255, 180), width=2)
    im.save(f"{base_dir}/ice_freeze.png")
    
    # 3. Lightning Strike (48x160, 4 frames)
    for f in range(4):
        im = Image.new("RGBA", (48, 160), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        # Jagged bolt
        pts = [(24, 0)]
        curr_x = 24
        for y in range(16, 160, 16):
            curr_x += random.randint(-8, 8)
            curr_x = max(10, min(38, curr_x))
            pts.append((curr_x, y))
        # Draw bolt glow
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i+1]], fill=(140, 220, 255, 200), width=5)
            d.line([pts[i], pts[i+1]], fill=(255, 255, 255, 255), width=2)
        # Ground scorch ring
        d.ellipse([14, 150, 34, 158], fill=(100, 230, 255, 220))
        im.save(f"{base_dir}/lightning_{f}.png")
        
    # 4. Magic Shield (48x48, 4 frames)
    for f in range(4):
        im = Image.new("RGBA", (48, 48), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24, 24
        pulse = int(math.sin(f * math.pi / 2.0) * 2)
        r = 21 + pulse
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(80, 200, 255, 75), outline=(130, 235, 255, 220), width=2)
        # Rotating runic markings
        for i in range(6):
            th = (f * 0.4) + i * (math.pi / 3.0)
            rx = cx + int(math.cos(th) * (r - 4))
            ry = cy + int(math.sin(th) * (r - 4))
            d.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=WIZ_GOLD)
        im.save(f"{base_dir}/shield_{f}.png")
        
    # Dark Orb for Boss (32x32, 4 frames)
    for f in range(4):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 16, 16
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(70, 15, 110, 200), outline=(180, 50, 255, 240), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(220, 140, 255, 255))
        im.save(f"{base_dir}/dark_orb_{f}.png")
        
    # Demon Flame projectile (32x32, 4 frames)
    for f in range(4):
        im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 16, 16
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 70, 20, 220))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 40, 255))
        im.save(f"{base_dir}/demon_flame_{f}.png")

    # Particles (assets/effects/particles)
    part_dir = "assets/effects/particles"
    ensure_dir(f"{part_dir}/sparkle.png")
    # Sparkle
    im = Image.new("RGBA", (16, 16), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.line([(8, 1), (8, 15)], fill=(255, 255, 255, 255), width=2)
    d.line([(1, 8), (15, 8)], fill=(255, 255, 255, 255), width=2)
    d.ellipse([6, 6, 10, 10], fill=(120, 230, 255, 255))
    im.save(f"{part_dir}/sparkle.png")
    
    # Smoke
    im = Image.new("RGBA", (16, 16), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.ellipse([3, 3, 13, 13], fill=(180, 175, 195, 180))
    im.save(f"{part_dir}/smoke.png")
    print("Generated abilities and effects")

def generate_tiles_and_props():
    tile_dir = "assets/tiles"
    ensure_dir(f"{tile_dir}/forest_tiles.png")
    
    # Forest Tileset: 128x128 (4x4 32x32 tiles)
    # Row 0: Grass Top, Grass Slope L, Grass Slope R, Floating Platform
    # Row 1: Dirt Middle, Dirt Wall L, Dirt Wall R, Wood Plank Platform
    # Row 2: Deep Stone, Moss Stone, Root Block, Hanging Vine
    # Row 3: Blue Glowing Mushroom, Purple Glowing Mushroom, Flower, Bush
    forest_im = Image.new("RGBA", (128, 128), COLOR_TRANSPARENT)
    fd = ImageDraw.Draw(forest_im)
    
    # Tile (0, 0): Grass Top
    fd.rectangle([0, 0, 31, 31], fill=(100, 65, 40, 255)) # Dirt base
    fd.rectangle([0, 0, 31, 8], fill=(60, 160, 60, 255)) # Grass top
    fd.rectangle([0, 0, 31, 3], fill=(100, 210, 80, 255)) # Grass highlight
    for x in range(0, 32, 4):
        fd.line([(x, 8), (x + 2, 12)], fill=(45, 120, 45, 255), width=1)
        
    # Tile (1, 0): Floating Moss Platform
    fd.rectangle([32, 4, 63, 20], fill=(85, 55, 35, 255))
    fd.rectangle([32, 4, 63, 10], fill=(70, 180, 70, 255))
    fd.line([(32, 4), (63, 4)], fill=(120, 230, 90, 255), width=2)
    
    # Tile (2, 0): Wooden Bridge Platform
    fd.rectangle([64, 8, 95, 20], fill=(130, 80, 45, 255))
    for x in range(64, 96, 8):
        fd.line([(x, 8), (x, 20)], fill=(90, 50, 25, 255), width=1)
        fd.rectangle([x+1, 9, x+6, 11], fill=(165, 110, 65, 255))
        
    # Tile (3, 0): Moss Stone Wall
    fd.rectangle([96, 0, 127, 31], fill=(75, 80, 75, 255))
    fd.line([(96, 15), (127, 15)], fill=(50, 55, 50, 255), width=1)
    fd.line([(111, 0), (111, 15)], fill=(50, 55, 50, 255), width=1)
    fd.line([(111, 15), (111, 31)], fill=(50, 55, 50, 255), width=1)
    fd.rectangle([98, 2, 106, 6], fill=(70, 150, 70, 255)) # moss
    
    # Tile (0, 1): Dirt Block
    fd.rectangle([0, 32, 31, 63], fill=(95, 60, 38, 255))
    for _ in range(6):
        px = random.randint(3, 28)
        py = random.randint(35, 60)
        fd.point((px, py), fill=(120, 80, 50, 255))
        
    # Tile (1, 1): Glowing Blue Mushroom (32, 32)
    fd.line([(48, 52), (48, 62)], fill=(200, 200, 210, 255), width=3)
    fd.ellipse([38, 42, 58, 54], fill=(60, 180, 255, 255))
    fd.ellipse([42, 44, 46, 48], fill=(220, 245, 255, 255))
    fd.ellipse([50, 45, 54, 49], fill=(220, 245, 255, 255))
    
    # Tile (2, 1): Glowing Purple Mushroom
    fd.line([(80, 52), (80, 62)], fill=(200, 190, 210, 255), width=3)
    fd.ellipse([70, 42, 90, 54], fill=(190, 60, 255, 255))
    fd.ellipse([74, 44, 78, 48], fill=(255, 230, 255, 255))
    
    # Tile (3, 1): Hanging Vine
    fd.line([(112, 32), (112, 63)], fill=(50, 140, 50, 255), width=2)
    for y in range(36, 60, 6):
        fd.ellipse([108, y, 112, y + 4], fill=(70, 180, 70, 255))
        fd.ellipse([112, y + 2, 116, y + 6], fill=(90, 210, 80, 255))
        
    forest_im.save(f"{tile_dir}/forest_tiles.png")
    
    # Castle Tileset: 128x128 (4x4 32x32 tiles)
    castle_im = Image.new("RGBA", (128, 128), COLOR_TRANSPARENT)
    cd = ImageDraw.Draw(castle_im)
    
    # Tile (0, 0): Castle Stone Brick
    cd.rectangle([0, 0, 31, 31], fill=(55, 50, 65, 255))
    cd.line([(0, 15), (31, 15)], fill=(30, 25, 40, 255), width=1)
    cd.line([(15, 0), (15, 15)], fill=(30, 25, 40, 255), width=1)
    cd.line([(7, 15), (7, 31)], fill=(30, 25, 40, 255), width=1)
    cd.line([(23, 15), (23, 31)], fill=(30, 25, 40, 255), width=1)
    # Stone highlights
    cd.line([(1, 1), (14, 1)], fill=(85, 78, 98, 255), width=1)
    cd.line([(17, 1), (30, 1)], fill=(85, 78, 98, 255), width=1)
    
    # Tile (1, 0): Castle Ornate Platform
    cd.rectangle([32, 6, 63, 18], fill=(45, 40, 55, 255))
    cd.line([(32, 6), (63, 6)], fill=(190, 155, 60, 255), width=2) # Gold trim
    cd.line([(32, 18), (63, 18)], fill=(25, 20, 32, 255), width=1)
    
    # Tile (2, 0): Spikes (32x32)
    for x in range(64, 96, 8):
        cd.polygon([(x, 31), (x + 4, 12), (x + 8, 31)], fill=(170, 175, 190, 255), outline=(90, 95, 110, 255))
        cd.line([(x + 4, 12), (x + 4, 30)], fill=(230, 235, 245, 255))
        
    # Tile (3, 0): Lava Surface
    cd.rectangle([96, 6, 127, 31], fill=(220, 60, 15, 255))
    cd.line([(96, 6), (127, 6)], fill=(255, 220, 50, 255), width=2)
    cd.rectangle([96, 16, 127, 31], fill=(170, 30, 10, 255))
    
    # Tile (0, 1): Lava Deep
    cd.rectangle([0, 32, 31, 63], fill=(160, 25, 10, 255))
    for _ in range(5):
        px = random.randint(2, 29)
        py = random.randint(35, 60)
        cd.point((px, py), fill=(255, 160, 30, 255))
        
    # Tile (1, 1): Iron Grate / Chain
    cd.line([(48, 32), (48, 63)], fill=(120, 125, 140, 255), width=3)
    for y in range(36, 60, 8):
        cd.rectangle([45, y, 51, y + 4], outline=(180, 185, 200, 255))
        
    castle_im.save(f"{tile_dir}/castle_tiles.png")
    
    # Props:
    # 1. Crystal (24x24, 6 frames)
    prop_dir = "assets/tiles"
    for f in range(6):
        im = Image.new("RGBA", (24, 24), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 12, 12
        # Spinning facet effect
        w_factor = math.cos(f * math.pi / 3.0)
        fw = max(2, int(8 * abs(w_factor)))
        gem_pts = [(cx, cy - 9), (cx + fw, cy), (cx, cy + 9), (cx - fw, cy)]
        d.polygon(gem_pts, fill=(60, 210, 255, 255), outline=(180, 245, 255, 255))
        d.line([(cx, cy - 9), (cx, cy + 9)], fill=(255, 255, 255, 200), width=1)
        # Sparkle
        if f in (0, 3):
            d.point((cx + 5, cy - 5), fill=(255, 255, 255, 255))
        im.save(f"{prop_dir}/crystal_{f}.png")
        
    # 2. Checkpoint Shrine (32x48) - Off and On
    im_off = Image.new("RGBA", (32, 48), COLOR_TRANSPARENT)
    od = ImageDraw.Draw(im_off)
    # Stone Obelisk
    od.polygon([(8, 46), (24, 46), (20, 14), (12, 14)], fill=(75, 75, 85, 255))
    od.polygon([(12, 14), (20, 14), (16, 6)], fill=(95, 95, 105, 255))
    od.rectangle([6, 42, 26, 46], fill=(55, 55, 65, 255)) # Base pedestal
    # Dormant dark runes
    od.line([(16, 18), (16, 38)], fill=(45, 45, 55, 255), width=2)
    od.line([(13, 24), (19, 24)], fill=(45, 45, 55, 255), width=2)
    od.line([(13, 32), (19, 32)], fill=(45, 45, 55, 255), width=2)
    im_off.save(f"{prop_dir}/checkpoint_off.png")
    
    im_on = Image.new("RGBA", (32, 48), COLOR_TRANSPARENT)
    ond = ImageDraw.Draw(im_on)
    # Stone Obelisk
    ond.polygon([(8, 46), (24, 46), (20, 14), (12, 14)], fill=(80, 80, 95, 255))
    ond.polygon([(12, 14), (20, 14), (16, 6)], fill=(100, 100, 115, 255))
    ond.rectangle([6, 42, 26, 46], fill=(60, 60, 75, 255))
    # Glowing Cyan/Gold Runes
    ond.line([(16, 18), (16, 38)], fill=(80, 240, 255, 255), width=2)
    ond.line([(13, 24), (19, 24)], fill=WIZ_GOLD, width=2)
    ond.line([(13, 32), (19, 32)], fill=WIZ_GOLD, width=2)
    # Floating Mystic Flame atop
    ond.ellipse([12, 2, 20, 10], fill=(90, 220, 255, 220))
    ond.ellipse([14, 4, 18, 8], fill=(255, 255, 255, 255))
    im_on.save(f"{prop_dir}/checkpoint_on.png")
    
    # 3. Portal Gateway (48x64, 6 frames)
    for f in range(6):
        im = Image.new("RGBA", (48, 64), COLOR_TRANSPARENT)
        d = ImageDraw.Draw(im)
        cx, cy = 24, 32
        # Stone arch frame
        d.arc([cx - 20, cy - 28, cx + 20, cy + 28], start=180, end=0, fill=(80, 75, 95, 255), width=4)
        d.line([(cx - 20, cy), (cx - 20, cy + 28)], fill=(80, 75, 95, 255), width=4)
        d.line([(cx + 20, cy), (cx + 20, cy + 28)], fill=(80, 75, 95, 255), width=4)
        # Swirling mystic portal center
        rot = f * (math.pi / 3.0)
        d.ellipse([cx - 15, cy - 22, cx + 15, cy + 22], fill=(40, 15, 80, 200))
        for i in range(4):
            th = rot + i * (math.pi / 2.0)
            px = cx + int(math.cos(th) * 9)
            py = cy + int(math.sin(th) * 14)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(130, 220, 255, 230))
        im.save(f"{prop_dir}/portal_{f}.png")
        
    # 4. Moving Platform (64x20)
    im = Image.new("RGBA", (64, 20), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.polygon([(4, 16), (60, 16), (63, 4), (1, 4)], fill=(65, 60, 78, 255))
    d.line([(1, 4), (63, 4)], fill=(120, 210, 255, 255), width=2)
    # Glowing runes in center
    d.ellipse([27, 8, 37, 14], fill=(70, 200, 255, 200))
    d.line([(18, 11), (24, 11)], fill=WIZ_GOLD, width=2)
    d.line([(40, 11), (46, 11)], fill=WIZ_GOLD, width=2)
    im.save(f"{prop_dir}/moving_platform.png")
    
    # 5. Tutorial / Lore Sign (32x32)
    im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([14, 14, 18, 31], fill=(110, 70, 40, 255))
    d.rectangle([4, 6, 28, 20], fill=(160, 110, 65, 255), outline=(80, 50, 30, 255), width=1)
    d.line([(7, 10), (25, 10)], fill=(90, 60, 35, 255), width=1)
    d.line([(7, 14), (20, 14)], fill=(90, 60, 35, 255), width=1)
    # Small blue rune mark on sign
    d.point((24, 15), fill=(80, 220, 255, 255))
    im.save(f"{prop_dir}/tutorial_sign.png")
    
    # 6. Spike Trap (32x32)
    im = Image.new("RGBA", (32, 32), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    for x in (2, 10, 18, 26):
        d.polygon([(x, 31), (x + 3, 10), (x + 6, 31)], fill=(160, 165, 180, 255), outline=(80, 85, 95, 255))
    im.save(f"{prop_dir}/spike_trap.png")
    print("Generated tiles and props")

def generate_backgrounds():
    # Forest Backgrounds: 960x540
    f_dir = "assets/backgrounds/forest"
    ensure_dir(f"{f_dir}/sky.png")
    
    # 1. Forest Sky (twilight magical gradient + stars + moon)
    sky = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    sd = ImageDraw.Draw(sky)
    for y in range(540):
        t = y / 540.0
        r = int(18 + (45 - 18) * t)
        g = int(15 + (35 - 15) * t)
        b = int(48 + (95 - 48) * t)
        sd.line([(0, y), (960, y)], fill=(r, g, b, 255))
    # Stars
    for _ in range(80):
        sx = random.randint(0, 959)
        sy = random.randint(0, 350)
        brightness = random.randint(180, 255)
        sd.point((sx, sy), fill=(255, 255, 255, brightness))
    # Glowing crescent / full moon
    sd.ellipse([800, 60, 870, 130], fill=(240, 245, 255, 220))
    sd.ellipse([790, 50, 880, 140], fill=(160, 220, 255, 40))
    sky.save(f"{f_dir}/sky.png")
    
    # 2. Forest Mountains (distant misty purple mountains)
    mountains = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    md = ImageDraw.Draw(mountains)
    pts = [(0, 540)]
    pts.append((0, 340))
    for x in range(0, 961, 80):
        h = 240 + int(60 * math.sin(x * 0.012) + 40 * math.cos(x * 0.025))
        pts.append((x, h))
    pts.append((960, 540))
    md.polygon(pts, fill=(35, 25, 65, 220))
    mountains.save(f"{f_dir}/mountains.png")
    
    # 3. Forest Trees Background (silhouetted pines)
    trees_bg = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    tbd = ImageDraw.Draw(trees_bg)
    for x in range(0, 960, 35):
        th = random.randint(160, 240)
        tbd.polygon([(x - 20, 540), (x, 540 - th), (x + 20, 540)], fill=(22, 38, 45, 200))
    trees_bg.save(f"{f_dir}/trees_bg.png")
    
    # 4. Forest Trees Foreground (ancient mossy trunks)
    trees_fg = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    tfd = ImageDraw.Draw(trees_fg)
    for tx in (80, 380, 680, 880):
        tfd.rectangle([tx - 24, 0, tx + 24, 540], fill=(18, 30, 30, 150))
        # Spores
        for _ in range(8):
            spx = tx + random.randint(-40, 40)
            spy = random.randint(100, 500)
            tfd.ellipse([spx - 2, spy - 2, spx + 2, spy + 2], fill=(120, 240, 200, 180))
    trees_fg.save(f"{f_dir}/trees_fg.png")

    # Castle Backgrounds: 960x540
    c_dir = "assets/backgrounds/castle"
    ensure_dir(f"{c_dir}/sky.png")
    
    # 1. Castle Sky (dark crimson & stormy clouds)
    csky = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    csd = ImageDraw.Draw(csky)
    for y in range(540):
        t = y / 540.0
        r = int(12 + (55 - 12) * t)
        g = int(8 + (15 - 8) * t)
        b = int(22 + (30 - 22) * t)
        csd.line([(0, y), (960, y)], fill=(r, g, b, 255))
    # Blood moon
    csd.ellipse([140, 70, 210, 140], fill=(220, 50, 40, 220))
    csd.ellipse([130, 60, 220, 150], fill=(255, 30, 30, 50))
    csky.save(f"{c_dir}/sky.png")
    
    # 2. Castle Spires (distant gothic towers)
    spires = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    spd = ImageDraw.Draw(spires)
    for sx in (120, 280, 450, 620, 790):
        w = 40
        h = random.randint(220, 320)
        # Tower base
        spd.rectangle([sx - w//2, 540 - h, sx + w//2, 540], fill=(25, 18, 35, 230))
        # Spire tip
        spd.polygon([(sx - w//2 - 4, 540 - h), (sx, 540 - h - 50), (sx + w//2 + 4, 540 - h)], fill=(20, 14, 28, 230))
    spires.save(f"{c_dir}/spires.png")
    
    # 3. Castle Interior Arches / Pillars
    interior = Image.new("RGBA", (960, 540), COLOR_TRANSPARENT)
    ind = ImageDraw.Draw(interior)
    for px in (160, 480, 800):
        ind.rectangle([px - 28, 0, px + 28, 540], fill=(35, 28, 45, 170))
        # Arch connection
        ind.arc([px - 160, 40, px + 160, 200], start=180, end=0, fill=(40, 32, 52, 170), width=18)
        # Torch sconce on pillar
        ind.rectangle([px - 4, 280, px + 4, 292], fill=(120, 90, 50, 255))
        ind.ellipse([px - 6, 268, px + 6, 280], fill=(255, 140, 30, 240))
        ind.ellipse([px - 20, 254, px + 20, 294], fill=(255, 160, 40, 50))
    interior.save(f"{c_dir}/interior_bg.png")
    print("Generated backgrounds")

def generate_ui():
    ui_dir = "assets/ui"
    ensure_dir(f"{ui_dir}/bar_bg.png")
    
    # 1. Bar BG (180x24)
    im = Image.new("RGBA", (180, 24), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 179, 23], fill=(20, 18, 28, 230), outline=(130, 105, 55, 255), width=2)
    d.rectangle([2, 2, 177, 21], outline=(50, 45, 60, 255), width=1)
    im.save(f"{ui_dir}/bar_bg.png")
    
    # 2. HP Fill (176x20)
    im = Image.new("RGBA", (176, 20), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    for x in range(176):
        d.line([(x, 0), (x, 19)], fill=(230 - int(x * 0.3), 35 + int(x * 0.1), 50, 255))
    d.line([(0, 1), (175, 1)], fill=(255, 140, 150, 200), width=2)
    im.save(f"{ui_dir}/hp_fill.png")
    
    # 3. MP Fill (176x20)
    im = Image.new("RGBA", (176, 20), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    for x in range(176):
        d.line([(x, 0), (x, 19)], fill=(30 + int(x * 0.2), 120 + int(x * 0.3), 245, 255))
    d.line([(0, 1), (175, 1)], fill=(150, 220, 255, 200), width=2)
    im.save(f"{ui_dir}/mp_fill.png")
    
    # 4. Boss Bar BG (304x24) & Boss Fill (300x20)
    im = Image.new("RGBA", (304, 24), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 303, 23], fill=(25, 15, 30, 240), outline=(210, 50, 60, 255), width=2)
    im.save(f"{ui_dir}/boss_bar_bg.png")
    
    im = Image.new("RGBA", (300, 20), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    for x in range(300):
        d.line([(x, 0), (x, 19)], fill=(180 - int(x * 0.2), 25, 75 + int(x * 0.3), 255))
    d.line([(0, 1), (299, 1)], fill=(255, 120, 160, 200), width=2)
    im.save(f"{ui_dir}/boss_fill.png")
    
    # 5. Ability Icons (40x40): Fireball [J], Ice [K], Lightning [L], Shield [I]
    # Fireball Icon
    im = Image.new("RGBA", (40, 40), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 39, 39], fill=(30, 20, 25, 240), outline=(235, 140, 40, 255), width=2)
    # Flame
    d.polygon([(20, 6), (28, 22), (24, 30), (16, 30), (12, 22)], fill=(255, 90, 20, 255))
    d.polygon([(20, 12), (25, 24), (15, 24)], fill=(255, 230, 60, 255))
    im.save(f"{ui_dir}/ability_fireball.png")
    
    # Ice Icon
    im = Image.new("RGBA", (40, 40), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 39, 39], fill=(20, 25, 35, 240), outline=(80, 210, 255, 255), width=2)
    # Snowflake
    d.line([(20, 8), (20, 32)], fill=(120, 235, 255, 255), width=2)
    d.line([(8, 20), (32, 20)], fill=(120, 235, 255, 255), width=2)
    d.line([(11, 11), (29, 29)], fill=(180, 245, 255, 255), width=2)
    d.line([(11, 29), (29, 11)], fill=(180, 245, 255, 255), width=2)
    im.save(f"{ui_dir}/ability_ice.png")
    
    # Lightning Icon
    im = Image.new("RGBA", (40, 40), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 39, 39], fill=(25, 22, 35, 240), outline=(240, 220, 60, 255), width=2)
    # Bolt
    d.polygon([(22, 6), (12, 20), (20, 20), (17, 34), (28, 17), (21, 17)], fill=(255, 240, 80, 255))
    im.save(f"{ui_dir}/ability_lightning.png")
    
    # Shield Icon
    im = Image.new("RGBA", (40, 40), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 39, 39], fill=(20, 28, 30, 240), outline=(60, 240, 180, 255), width=2)
    # Shield crest
    d.polygon([(20, 7), (31, 11), (28, 27), (20, 33), (12, 27), (9, 11)], fill=(50, 180, 150, 255), outline=(140, 255, 220, 255))
    im.save(f"{ui_dir}/ability_shield.png")
    
    # Ability Lock Overlay (40x40)
    im = Image.new("RGBA", (40, 40), (15, 15, 20, 200))
    d = ImageDraw.Draw(im)
    # Padlock
    d.rectangle([14, 18, 26, 28], fill=(160, 150, 120, 255))
    d.arc([16, 12, 24, 20], start=180, end=0, fill=(200, 190, 160, 255), width=2)
    im.save(f"{ui_dir}/ability_locked.png")
    
    # Cooldown overlay (40x40)
    im = Image.new("RGBA", (40, 40), (0, 0, 0, 160))
    im.save(f"{ui_dir}/ability_cooldown.png")
    
    # Crystal HUD Icon (24x24)
    im = Image.new("RGBA", (24, 24), COLOR_TRANSPARENT)
    d = ImageDraw.Draw(im)
    d.polygon([(12, 2), (21, 12), (12, 22), (3, 12)], fill=(80, 230, 255, 255), outline=(220, 255, 255, 255), width=1)
    im.save(f"{ui_dir}/icon_crystal.png")
    
    # Button normal, hover, pressed (180x44)
    im_norm = Image.new("RGBA", (180, 44), COLOR_TRANSPARENT)
    nd = ImageDraw.Draw(im_norm)
    nd.rectangle([0, 0, 179, 43], fill=(45, 35, 60, 240), outline=(180, 140, 60, 255), width=2)
    nd.rectangle([2, 2, 177, 41], outline=(90, 70, 115, 255), width=1)
    im_norm.save(f"{ui_dir}/button_normal.png")
    
    im_hov = Image.new("RGBA", (180, 44), COLOR_TRANSPARENT)
    hd = ImageDraw.Draw(im_hov)
    hd.rectangle([0, 0, 179, 43], fill=(70, 50, 95, 240), outline=(255, 215, 80, 255), width=2)
    hd.rectangle([2, 2, 177, 41], outline=(140, 110, 185, 255), width=1)
    im_hov.save(f"{ui_dir}/button_hover.png")
    
    im_press = Image.new("RGBA", (180, 44), COLOR_TRANSPARENT)
    pd = ImageDraw.Draw(im_press)
    pd.rectangle([0, 0, 179, 43], fill=(30, 22, 42, 240), outline=(130, 100, 40, 255), width=2)
    im_press.save(f"{ui_dir}/button_pressed.png")
    
    # Dialog Panel BG (400x320)
    im_p = Image.new("RGBA", (400, 320), COLOR_TRANSPARENT)
    pd = ImageDraw.Draw(im_p)
    pd.rectangle([0, 0, 399, 319], fill=(22, 18, 30, 245), outline=(190, 150, 65, 255), width=3)
    pd.rectangle([4, 4, 395, 315], outline=(65, 50, 85, 255), width=1)
    # Corner ornaments
    for cx, cy in [(6, 6), (393, 6), (6, 313), (393, 313)]:
        pd.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=WIZ_GOLD)
    im_p.save(f"{ui_dir}/panel_bg.png")
    print("Generated UI assets")

if __name__ == "__main__":
    generate_wizard()
    generate_enemies()
    generate_abilities_and_effects()
    generate_tiles_and_props()
    generate_backgrounds()
    generate_ui()
    print("All graphics successfully generated!")
