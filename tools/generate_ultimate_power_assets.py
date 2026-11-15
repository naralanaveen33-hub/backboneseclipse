import os
import math
from PIL import Image, ImageDraw

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def generate_ultimate_power_assets():
    ui_dir = "assets/ui"
    eff_dir = "assets/effects/projectiles"
    obj_dir = "assets/tiles"
    ensure_dir(f"{ui_dir}/ability_void_cannon.png")
    ensure_dir(f"{eff_dir}/astral_beam_proj.png")
    
    # 1. UI Icon: Ability Void Cannon (32x32)
    vc_icon = Image.new("RGBA", (32, 32), (20, 10, 35, 255))
    vd = ImageDraw.Draw(vc_icon)
    vd.rectangle([0, 0, 31, 31], outline=(220, 60, 255, 255), width=2)
    # Cosmic cannon flare
    vd.ellipse([4, 4, 27, 27], fill=(80, 20, 120, 220), outline=(255, 180, 255))
    vd.line([(4, 16), (28, 16)], fill=(255, 240, 255), width=3)
    vd.line([(16, 4), (16, 28)], fill=(255, 240, 255), width=3)
    vd.ellipse([10, 10, 21, 21], fill=(255, 255, 255))
    vc_icon.save(f"{ui_dir}/ability_void_cannon.png")
    
    # 2. UI Icon: Ability Shadow Step (32x32)
    ss_icon = Image.new("RGBA", (32, 32), (15, 25, 40, 255))
    sd = ImageDraw.Draw(ss_icon)
    sd.rectangle([0, 0, 31, 31], outline=(60, 220, 255, 255), width=2)
    # Winged boots / teleport arrows
    sd.polygon([(6, 16), (18, 6), (18, 12), (28, 12), (28, 20), (18, 20), (18, 26)], fill=(100, 220, 255, 240), outline=(255, 255, 255))
    sd.line([(4, 6), (4, 26)], fill=(180, 240, 255), width=2)
    ss_icon.save(f"{ui_dir}/ability_shadow_step.png")

    # 3. Player Astral Beam Projectile (160x40)
    beam = Image.new("RGBA", (160, 40), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    # Outer astral flare
    bd.rectangle([0, 4, 159, 35], fill=(140, 30, 220, 160))
    # Mid starlight glow
    bd.rectangle([0, 8, 159, 31], fill=(220, 80, 255, 220))
    # Core laser beam
    bd.rectangle([0, 14, 159, 25], fill=(255, 255, 255, 255))
    # Energy ripples
    for x in range(0, 160, 20):
        bd.ellipse([x - 6, 2, x + 6, 37], outline=(255, 240, 180, 180), width=2)
    beam.save(f"{eff_dir}/astral_beam_proj.png")
    
    # 4. God Relic Shrine Artwork (48x64)
    shrine = Image.new("RGBA", (48, 64), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shrine)
    # Pedestal base
    shd.polygon([(4, 60), (44, 60), (40, 48), (8, 48)], fill=(30, 15, 45, 255), outline=(220, 160, 40), width=2)
    shd.rectangle([14, 28, 34, 48], fill=(45, 22, 65, 255), outline=(255, 120, 220), width=2)
    # Floating Divine Relic Orb (top)
    shd.ellipse([12, 4, 36, 28], fill=(160, 30, 240, 230), outline=(255, 220, 80), width=3)
    shd.ellipse([18, 10, 30, 22], fill=(255, 255, 255))
    # Ancient gold wings on sides of altar
    shd.polygon([(8, 48), (0, 28), (14, 36)], fill=(240, 190, 50, 240), outline=(255, 240, 140))
    shd.polygon([(40, 48), (48, 28), (34, 36)], fill=(240, 190, 50, 240), outline=(255, 240, 140))
    shrine.save("assets/tiles/god_relic_shrine.png")
    
    # 5. Secret False Wall / Crack Tile (80x80)
    wall = Image.new("RGBA", (80, 80), (28, 18, 42, 255))
    wd = ImageDraw.Draw(wall)
    wd.rectangle([0, 0, 79, 79], outline=(140, 40, 100), width=2)
    # Glowing crack in wall
    wd.line([(40, 4), (44, 25)], fill=(220, 60, 255), width=2)
    wd.line([(44, 25), (32, 45)], fill=(255, 120, 220), width=3)
    wd.line([(32, 45), (48, 62)], fill=(220, 60, 255), width=2)
    wd.line([(48, 62), (38, 76)], fill=(255, 240, 160), width=2)
    wall.save("assets/tiles/secret_wall_cracked.png")
    
    print("Generated all ultimate ability and secret room assets!")

if __name__ == "__main__":
    generate_ultimate_power_assets()
