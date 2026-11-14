import os

def build_level_4():
    tscn = """[gd_scene load_steps=25 format=3]

[ext_resource type="Script" path="res://scripts/systems/level_controller.gd" id="1_ctrl"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/frost/frost_sky.png" id="2_sky"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/frost/ice_mountains.png" id="3_mount"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/frost/frost_cavern.png" id="4_cavern"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_frost_160.png" id="5_p160"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_frost_80.png" id="6_p80"]
[ext_resource type="Texture2D" path="res://assets/tiles/spike_trap.png" id="7_spike"]
[ext_resource type="Texture2D" path="res://assets/tiles/boss_barrier.png" id="8_barr"]
[ext_resource type="PackedScene" path="res://scenes/player/player.tscn" id="9_player"]
[ext_resource type="PackedScene" path="res://scenes/objects/crystal.tscn" id="10_crys"]
[ext_resource type="PackedScene" path="res://scenes/objects/checkpoint.tscn" id="11_chk"]
[ext_resource type="PackedScene" path="res://scenes/objects/tutorial_sign.tscn" id="12_sign"]
[ext_resource type="PackedScene" path="res://scenes/objects/moving_platform.tscn" id="13_mplat"]
[ext_resource type="PackedScene" path="res://scenes/objects/spike_trap.tscn" id="14_spiketrap"]
[ext_resource type="PackedScene" path="res://scenes/objects/boss_trigger.tscn" id="15_btrig"]
[ext_resource type="PackedScene" path="res://scenes/enemies/shadow_monster.tscn" id="16_sm"]
[ext_resource type="PackedScene" path="res://scenes/enemies/flying_bat.tscn" id="17_bat"]
[ext_resource type="PackedScene" path="res://scenes/enemies/fire_demon.tscn" id="18_fdemon"]
[ext_resource type="PackedScene" path="res://scenes/enemies/boss_frost_lich.tscn" id="19_boss"]
[ext_resource type="PackedScene" path="res://scenes/ui/hud.tscn" id="20_hud"]
[ext_resource type="PackedScene" path="res://scenes/ui/pause_menu.tscn" id="21_pmenu"]
[ext_resource type="PackedScene" path="res://scenes/ui/game_over_menu.tscn" id="22_gomenu"]
[ext_resource type="PackedScene" path="res://scenes/objects/ruined_shrine.tscn" id="23_shrine"]
[ext_resource type="PackedScene" path="res://scenes/objects/level_portal.tscn" id="24_port"]

[sub_resource type="RectangleShape2D" id="Shape_160"]
size = Vector2(160, 32)

[sub_resource type="RectangleShape2D" id="Shape_80"]
size = Vector2(80, 24)

[sub_resource type="RectangleShape2D" id="Shape_Barrier"]
size = Vector2(32, 280)

[node name="Level4" type="Node2D"]
script = ExtResource("1_ctrl")
level_number = 4
music_track = "dark_dream"
death_y = 650.0

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="LayerSky" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0, 0)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerSky"]
texture = ExtResource("2_sky")
centered = false

[node name="LayerMount" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.2, 0.05)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerMount"]
texture = ExtResource("3_mount")
centered = false

[node name="LayerCavern" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.6, 0.1)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerCavern"]
texture = ExtResource("4_cavern")
centered = false

[node name="Platforms" type="Node2D" parent="."]

"""
    # Ground platforms (160x32)
    ground_x = [
        0, 160, 320, 480, 640,
        960, 1120, 1280,
        1600, 1760, 1920,
        2080, 2240, 2400, 2560, 2720, 2880
    ]
    for i, gx in enumerate(ground_x):
        tscn += f"""[node name="Ground_{i}" type="StaticBody2D" parent="Platforms"]
position = Vector2({gx + 80}, 464)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="Platforms/Ground_{i}"]
texture = ExtResource("5_p160")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Ground_{i}"]
shape = SubResource("Shape_160")

"""

    # Floating platforms (80x24)
    floats = [
        (420, 350), (540, 270), (740, 350), (860, 280),
        (1100, 340), (1240, 260), (1440, 320),
        (2160, 350), (2320, 290), (2480, 350)
    ]
    for i, (fx, fy) in enumerate(floats):
        tscn += f"""[node name="Float_{i}" type="StaticBody2D" parent="Platforms"]
position = Vector2({fx}, {fy})
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="Platforms/Float_{i}"]
texture = ExtResource("6_p80")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Float_{i}"]
shape = SubResource("Shape_80")
one_way_collision = true

"""

    # Spikes
    tscn += """[node name="Spike1" parent="." instance=ExtResource("14_spiketrap")]
position = Vector2(800, 470)

[node name="Spike2" parent="." instance=ExtResource("14_spiketrap")]
position = Vector2(1480, 470)

"""

    # Moving Platform across gap: at X = 800, Y = 400
    tscn += """[node name="MovingPlatform1" parent="." instance=ExtResource("13_mplat")]
position = Vector2(800, 400)
move_offset = Vector2(100, 0)
speed = 50.0

[node name="MovingPlatform2" parent="." instance=ExtResource("13_mplat")]
position = Vector2(1480, 400)
move_offset = Vector2(90, 0)
speed = 45.0

"""

    # Checkpoints
    tscn += """[node name="Checkpoint1" parent="." instance=ExtResource("11_chk")]
position = Vector2(960, 416)
checkpoint_id = 1

[node name="Checkpoint2" parent="." instance=ExtResource("11_chk")]
position = Vector2(1920, 416)
checkpoint_id = 2

"""

    # Ruined Shrine of Vitality (+30 Max HP & Full Heal)
    tscn += """[node name="RuinedShrine" parent="." instance=ExtResource("23_shrine")]
position = Vector2(1240, 236)
stat_buff = "hp"

"""

    # Signs
    signs = [
        (140, 420, "LEVEL 4: THE FROZEN CRYPTS\\nDeflect the Frost Lich's shards back into him to freeze him!"),
        (980, 420, "Frost Lich Sovereign awaits in the frozen sanctum!")
    ]
    for i, (sx, sy, msg) in enumerate(signs):
        tscn += f"""[node name="Sign_{i}" parent="." instance=ExtResource("12_sign")]
position = Vector2({sx}, {sy})
message = "{msg}"

"""

    # Crystals
    crys = [
        (220, 410), (340, 360), (540, 230), (740, 310), (860, 240),
        (1100, 300), (1240, 220), (1440, 280), (1640, 410),
        (2160, 310), (2320, 250), (2480, 310)
    ]
    for i, (cx, cy) in enumerate(crys):
        tscn += f"""[node name="Crystal_{i}" parent="." instance=ExtResource("10_crys")]
position = Vector2({cx}, {cy})

"""

    # Enemies
    tscn += """[node name="Enemies" type="Node2D" parent="."]

[node name="ShadowMonster1" parent="Enemies" instance=ExtResource("16_sm")]
position = Vector2(420, 420)

[node name="FlyingBat1" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(640, 250)

[node name="FireDemon1" parent="Enemies" instance=ExtResource("18_fdemon")]
position = Vector2(1160, 420)

[node name="FlyingBat2" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(1380, 250)

"""

    # Boss Arena
    tscn += """[node name="BossArena" type="Node2D" parent="."]

[node name="BossTrigger" parent="BossArena" instance=ExtResource("15_btrig")]
position = Vector2(2040, 360)
boss_node = NodePath("../BossFrostLich")

[node name="BarrierLeft" type="StaticBody2D" parent="BossArena"]
position = Vector2(2090, 340)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="BossArena/BarrierLeft"]
texture = ExtResource("8_barr")

[node name="CollisionShape2D" type="CollisionShape2D" parent="BossArena/BarrierLeft"]
shape = SubResource("Shape_Barrier")

[node name="BarrierRight" type="StaticBody2D" parent="BossArena"]
position = Vector2(2840, 340)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="BossArena/BarrierRight"]
texture = ExtResource("8_barr")

[node name="CollisionShape2D" type="CollisionShape2D" parent="BossArena/BarrierRight"]
shape = SubResource("Shape_Barrier")

[node name="BossFrostLich" parent="BossArena" instance=ExtResource("19_boss")]
position = Vector2(2480, 410)

[node name="LevelPortal" parent="BossArena" instance=ExtResource("24_port")]
position = Vector2(2760, 436)

"""

    # Player & UI
    tscn += """[node name="Player" parent="." instance=ExtResource("9_player")]
position = Vector2(60, 410)

[node name="HUD" parent="." instance=ExtResource("20_hud")]

[node name="PauseMenu" parent="." instance=ExtResource("21_pmenu")]

[node name="GameOverMenu" parent="." instance=ExtResource("22_gomenu")]
"""
    with open("scenes/levels/level_4.tscn", "w") as f:
        f.write(tscn)
    print("Built scenes/levels/level_4.tscn successfully!")

if __name__ == "__main__":
    build_level_4()
