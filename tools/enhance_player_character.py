import os
import math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

def extract_and_enhance_character():
    src_path = "/Users/naralanaveen/.gemini/antigravity/brain/1c2c2949-62af-45c1-b663-ea802790ffee/.user_uploaded/media_1794720151479_3fa09cff.png"
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    
    # 1. Clean background with smooth alpha matting
    out_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = im.load()
    out_pixels = out_im.load()
    
    # Flood-fill from borders for exterior white
    from collections import deque
    visited = [[False]*w for _ in range(h)]
    q = deque()
    
    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
        visited[0][x] = True
        visited[h - 1][x] = True
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))
        visited[y][0] = True
        visited[y][w - 1] = True
        
    while q:
        x, y = q.popleft()
        r, g, b, a = pixels[x, y]
        # If it's background white / near white
        brightness = (r + g + b) / 3.0
        if brightness > 210:
            out_pixels[x, y] = (0, 0, 0, 0)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                    visited[ny][nx] = True
                    nr, ng, nb, _ = pixels[nx, ny]
                    if (nr + ng + nb) / 3.0 > 200:
                        q.append((nx, ny))

    # Copy over non-background pixels, removing any white edge fringing
    for y in range(h):
        for x in range(w):
            if not visited[y][x]:
                r, g, b, a = pixels[x, y]
                bright = (r + g + b) / 3.0
                if bright > 235:
                    # fringe pixel
                    out_pixels[x, y] = (0, 0, 0, 0)
                elif bright > 210:
                    alpha = int(255 * (1.0 - (bright - 210) / 25.0))
                    out_pixels[x, y] = (r, g, b, alpha)
                else:
                    out_pixels[x, y] = (r, g, b, 255)
                    
    # Crop to character bounding box
    bbox = out_im.getbbox()
    if bbox:
        cropped = out_im.crop(bbox)
    else:
        cropped = out_im
        
    # Enhance contrast and saturation
    enhancer_col = ImageEnhance.Color(cropped)
    enhanced = enhancer_col.enhance(1.25)
    enhancer_con = ImageEnhance.Contrast(enhanced)
    enhanced = enhancer_con.enhance(1.15)
    
    # Save master high-resolution enhanced artwork
    dest_dir = "assets/characters/wizard"
    os.makedirs(dest_dir, exist_ok=True)
    enhanced.save(os.path.join(dest_dir, "character_full_enhanced.png"))
    print("Saved high-res enhanced character to assets/characters/wizard/character_full_enhanced.png")
    
    # 2. Generate 48x48 sprite sheets matching existing Player scene specifications
    target_h = 42 # Height inside 48x48 canvas so it fits perfectly on ground
    aspect = float(enhanced.width) / float(enhanced.height)
    target_w = int(target_h * aspect)
    base_sprite = enhanced.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Helper to paste base sprite with offsets into 48x48 canvas
    def make_frame(offset_x=0, offset_y=0, scale_y=1.0, scale_x=1.0, rot=0.0, staff_flare=False, eye_flare=False):
        f = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        spr = base_sprite
        if scale_y != 1.0 or scale_x != 1.0:
            sw = max(4, int(target_w * scale_x))
            sh = max(4, int(target_h * scale_y))
            spr = spr.resize((sw, sh), Image.Resampling.LANCZOS)
        if rot != 0.0:
            spr = spr.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
            
        px = (48 - spr.width) // 2 + offset_x
        py = (48 - spr.height) + offset_y - 2 # Align to bottom feet
        f.paste(spr, (px, py), spr)
        
        draw = ImageDraw.Draw(f)
        if staff_flare:
            # Staff tip glow (top right of character)
            staff_x = px + int(spr.width * 0.78)
            staff_y = py + int(spr.height * 0.16)
            for r in range(6, 1, -1):
                draw.ellipse([staff_x - r, staff_y - r, staff_x + r, staff_y + r], fill=(220, 80, 255, 120 - r * 15))
            draw.ellipse([staff_x - 2, staff_y - 2, staff_x + 2, staff_y + 2], fill=(255, 230, 255, 255))
            
        if eye_flare:
            # Glowing purple eyes flare
            eye_x = px + int(spr.width * 0.44)
            eye_y = py + int(spr.height * 0.35)
            draw.line([(eye_x - 3, eye_y), (eye_x + 3, eye_y)], fill=(255, 120, 255, 220), width=1)
            
        return f

    # A. IDLE (4 frames - breathing bob and staff orb pulse)
    for i in range(4):
        bob = int(math.sin(i * math.pi / 2.0) * 1.5)
        scale_y = 1.0 - (0.02 if i % 2 == 1 else 0.0)
        fr = make_frame(offset_y=bob, scale_y=scale_y, staff_flare=(i >= 2), eye_flare=True)
        fr.save(f"{dest_dir}/idle_{i}.png")
        
    # B. RUN (6 frames - stride, bounce, cape motion)
    for i in range(6):
        t = i * (math.pi / 3.0)
        bob = -int(abs(math.sin(t) * 3.0))
        lean = int(math.sin(t) * 1.5)
        rot = -3.0 if i in [1, 2] else (3.0 if i in [4, 5] else 0.0)
        fr = make_frame(offset_x=lean + 1, offset_y=bob, rot=rot, staff_flare=(i % 2 == 0), eye_flare=True)
        fr.save(f"{dest_dir}/run_{i}.png")
        
    # C. JUMP (2 frames - upward thrust, staff held high)
    j0 = make_frame(offset_y=-3, scale_y=1.06, scale_x=0.96, staff_flare=True, eye_flare=True)
    j0.save(f"{dest_dir}/jump_0.png")
    j1 = make_frame(offset_y=-4, scale_y=1.04, scale_x=0.98, staff_flare=True, eye_flare=True)
    j1.save(f"{dest_dir}/jump_1.png")
    
    # D. FALL (2 frames - cape billowing out, descending)
    f0 = make_frame(offset_y=0, scale_y=0.96, scale_x=1.05, staff_flare=False, eye_flare=True)
    f0.save(f"{dest_dir}/fall_0.png")
    f1 = make_frame(offset_y=1, scale_y=0.94, scale_x=1.06, staff_flare=False, eye_flare=True)
    f1.save(f"{dest_dir}/fall_1.png")
    
    # E. ATTACK (4 frames - staff thrust forward, colossal magical flare at orb)
    for i in range(4):
        thrust_x = i * 2
        fr = make_frame(offset_x=thrust_x, offset_y=0, rot=-4.0 * i, staff_flare=True, eye_flare=True)
        draw = ImageDraw.Draw(fr)
        # Magic casting arc at staff tip
        tip_x = 24 + thrust_x + 12
        tip_y = 12
        draw.arc([tip_x - 6 - i*2, tip_y - 6 - i*2, tip_x + 6 + i*2, tip_y + 6 + i*2], -45, 90, fill=(240, 160, 255, 230), width=2)
        fr.save(f"{dest_dir}/attack_{i}.png")
        
    # F. HURT (2 frames - recoil backward, flash)
    for i in range(2):
        fr = make_frame(offset_x=-3, offset_y=-1, rot=5.0, staff_flare=False, eye_flare=False)
        # Tint with red/white impact
        tint = Image.new("RGBA", (48, 48), (255, 80, 80, 80))
        fr.alpha_composite(tint)
        fr.save(f"{dest_dir}/hurt_{i}.png")
        
    # G. DEATH (6 frames - dark robe dissolving into void stardust)
    for i in range(6):
        fr = make_frame(offset_y=i * 2, scale_y=max(0.2, 1.0 - i * 0.15), rot=i * 5.0)
        # Dissolve alpha
        pix = fr.load()
        for y in range(48):
            for x in range(48):
                r, g, b, a = pix[x, y]
                if a > 0:
                    new_a = max(0, int(a * (1.0 - i * 0.18)))
                    pix[x, y] = (r, g, b, new_a)
        draw = ImageDraw.Draw(fr)
        # Cosmic stardust particles
        for p in range(6):
            ang = p * 1.05 + i * 0.4
            dist = 4 + i * 3
            px = 24 + int(math.cos(ang) * dist)
            py = 32 + int(math.sin(ang) * dist)
            if 0 <= px < 48 and 0 <= py < 48:
                draw.point((px, py), fill=(220, 140, 255, max(0, 255 - i * 40)))
        fr.save(f"{dest_dir}/death_{i}.png")
        
    # H. RESPAWN (6 frames - dark celestial vortex reforming into wizard)
    for i in range(6):
        prog = (i + 1) / 6.0
        fr = make_frame(offset_y=int((1.0 - prog) * 8), scale_y=prog, scale_x=prog)
        pix = fr.load()
        for y in range(48):
            for x in range(48):
                r, g, b, a = pix[x, y]
                if a > 0:
                    pix[x, y] = (r, g, b, int(a * prog))
        draw = ImageDraw.Draw(fr)
        # Reforming summoning rift ring
        rr = int(prog * 18)
        draw.ellipse([24 - rr, 36 - rr//3, 24 + rr, 36 + rr//3], outline=(200, 100, 255, int(180 * (1.0 - prog))), width=2)
        fr.save(f"{dest_dir}/respawn_{i}.png")

    print("All player wizard animations successfully generated from the new character!")

if __name__ == "__main__":
    extract_and_enhance_character()
