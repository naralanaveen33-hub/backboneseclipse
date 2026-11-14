import os

def build_boss_tscn():
    tscn_path = "scenes/enemies/boss_ultimate_overlord.tscn"
    os.makedirs(os.path.dirname(tscn_path), exist_ok=True)
    
    anims = [
        ("attacking", 4, 8.0, False),
        ("dashing", 4, 10.0, True),
        ("death", 6, 7.0, False),
        ("idle", 4, 6.0, True),
        ("running", 4, 8.0, True),
        ("stunned", 3, 5.0, True),
        ("taking_damage", 2, 8.0, False),
        ("teleporting", 4, 8.0, False),
        ("ultimate_attack", 6, 8.0, False)
    ]
    
    lines = []
    lines.append('[gd_scene load_steps=42 format=3]')
    lines.append('')
    lines.append('[ext_resource type="Script" path="res://scripts/enemies/boss_ultimate_overlord.gd" id="1_script"]')
    
    res_id = 2
    anim_frames = {}
    
    for anim_name, count, speed, loop in anims:
        frame_ids = []
        for i in range(count):
            cur_id = f"{res_id}_ext"
            res_id += 1
            frame_ids.append(cur_id)
            lines.append(f'[ext_resource type="Texture2D" path="res://assets/characters/enemies/boss_ultimate_overlord/{anim_name}_{i}.png" id="{cur_id}"]')
        anim_frames[anim_name] = (frame_ids, speed, loop)
        
    lines.append('')
    lines.append('[sub_resource type="SpriteFrames" id="SpriteFrames_boss"]')
    
    anim_entries = []
    for anim_name, (frame_ids, speed, loop) in anim_frames.items():
        f_parts = []
        for fid in frame_ids:
            f_parts.append(f'{{\n"duration": 1.0,\n"texture": ExtResource("{fid}")\n}}')
        f_str = ', '.join(f_parts)
        entry_str = f"""{{
"frames": [{f_str}],
"loop": {"true" if loop else "false"},
"name": &"{anim_name}",
"speed": {speed}
}}"""
        anim_entries.append(entry_str)
        
    lines.append('animations = [' + ', '.join(anim_entries) + ']')
    lines.append('')
    lines.append('[sub_resource type="RectangleShape2D" id="RectangleShape2D_body"]')
    lines.append('size = Vector2(40, 72)')
    lines.append('')
    lines.append('[sub_resource type="RectangleShape2D" id="RectangleShape2D_hit"]')
    lines.append('size = Vector2(48, 76)')
    lines.append('')
    lines.append('[node name="BossUltimateOverlord" type="CharacterBody2D"]')
    lines.append('collision_layer = 4')
    lines.append('collision_mask = 1')
    lines.append('script = ExtResource("1_script")')
    lines.append('')
    lines.append('[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."] ')
    lines.append('sprite_frames = SubResource("SpriteFrames_boss")')
    lines.append('animation = &"idle"')
    lines.append('')
    lines.append('[node name="CollisionShape2D" type="CollisionShape2D" parent="."] ')
    lines.append('position = Vector2(0, 8)')
    lines.append('shape = SubResource("RectangleShape2D_body")')
    lines.append('')
    lines.append('[node name="Hitbox" type="Area2D" parent="."] ')
    lines.append('collision_layer = 4')
    lines.append('collision_mask = 2')
    lines.append('')
    lines.append('[node name="CollisionShape2D" type="CollisionShape2D" parent="Hitbox"] ')
    lines.append('position = Vector2(0, 8)')
    lines.append('shape = SubResource("RectangleShape2D_hit")')
    lines.append('')
    lines.append('[node name="CastPoint" type="Marker2D" parent="."] ')
    lines.append('position = Vector2(24, 0)')
    lines.append('')
    lines.append('[node name="BeamPoint" type="Marker2D" parent="."] ')
    lines.append('position = Vector2(30, 4)')
    lines.append('')
    lines.append('[node name="AuraParticles" type="CPUParticles2D" parent="."] ')
    lines.append('amount = 32')
    lines.append('lifetime = 1.2')
    lines.append('emission_shape = 1')
    lines.append('emission_sphere_radius = 28.0')
    lines.append('gravity = Vector2(0, -60)')
    lines.append('scale_amount_min = 2.0')
    lines.append('scale_amount_max = 5.0')
    lines.append('color = Color(0.7, 0.2, 0.9, 0.7)')
    lines.append('')
    lines.append('[node name="RageParticles" type="CPUParticles2D" parent="."] ')
    lines.append('emitting = false')
    lines.append('amount = 64')
    lines.append('lifetime = 0.8')
    lines.append('emission_shape = 1')
    lines.append('emission_sphere_radius = 35.0')
    lines.append('gravity = Vector2(0, -120)')
    lines.append('scale_amount_min = 3.0')
    lines.append('scale_amount_max = 7.0')
    lines.append('color = Color(1.0, 0.3, 0.1, 0.85)')
    lines.append('')
    lines.append('[connection signal="body_entered" from="Hitbox" to="." method="_on_hitbox_body_entered"]')
    lines.append('')

    with open(tscn_path, "w") as f:
        f.write('\n'.join(lines))
    print("Built", tscn_path)

if __name__ == "__main__":
    build_boss_tscn()
