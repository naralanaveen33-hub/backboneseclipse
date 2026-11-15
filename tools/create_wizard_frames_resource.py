def make_frames_tres():
    # Gather textures
    textures = {
        "idle": [f"res://assets/characters/wizard/idle_{i}.png" for i in range(4)],
        "run": [f"res://assets/characters/wizard/run_{i}.png" for i in range(6)],
        "jump": [f"res://assets/characters/wizard/jump_{i}.png" for i in range(2)],
        "fall": [f"res://assets/characters/wizard/fall_{i}.png" for i in range(2)],
        "attack": [f"res://assets/characters/wizard/attack_{i}.png" for i in range(4)],
        "hurt": [f"res://assets/characters/wizard/hurt_{i}.png" for i in range(2)],
        "death": [f"res://assets/characters/wizard/death_{i}.png" for i in range(6)],
        "respawn": [f"res://assets/characters/wizard/respawn_{i}.png" for i in range(6)],
    }
    
    # Assign unique IDs to each path
    tex_to_id = {}
    id_counter = 1
    for anim_name, paths in textures.items():
        for p in paths:
            if p not in tex_to_id:
                tex_to_id[p] = f"{id_counter}_{anim_name[:2]}{id_counter}"
                id_counter += 1
                
    content = f"[gd_resource type=\"SpriteFrames\" load_steps={len(tex_to_id) + 1} format=3]\n\n"
    for p, tid in tex_to_id.items():
        content += f'[ext_resource type="Texture2D" path="{p}" id="{tid}"]\n'
        
    content += "\n[resource]\nanimations = [\n"
    
    speeds = {
        "attack": 14.0,
        "death": 8.0,
        "fall": 8.0,
        "hurt": 8.0,
        "idle": 6.0,
        "jump": 8.0,
        "respawn": 9.0,
        "run": 10.0,
    }
    loops = {
        "attack": "false",
        "death": "false",
        "fall": "true",
        "hurt": "false",
        "idle": "true",
        "jump": "true",
        "respawn": "false",
        "run": "true",
    }
    
    anim_keys = sorted(textures.keys())
    for k in anim_keys:
        paths = textures[k]
        content += "  {\n"
        content += '    "frames": [\n'
        for p in paths:
            tid = tex_to_id[p]
            content += f'      {{\n        "duration": 1.0,\n        "texture": ExtResource("{tid}")\n      }},\n'
        content = content.rstrip(",\n") + "\n"
        content += f'    ],\n    "loop": {loops[k]},\n    "name": &"{k}",\n    "speed": {speeds[k]}\n  }},\n'
        
    content = content.rstrip(",\n") + "\n]\n"
    
    with open("assets/characters/wizard/wizard_frames.tres", "w") as f:
        f.write(content)
    print("Created assets/characters/wizard/wizard_frames.tres successfully!")

if __name__ == "__main__":
    make_frames_tres()
