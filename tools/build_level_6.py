import os

def build_level_6():
    tscn = """[gd_scene load_steps=25 format=3]

[ext_resource type="Script" path="res://scripts/systems/level_controller.gd" id="1_ctrl"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/void/void_sky.png" id="2_sky"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/void/void_spires.png" id="3_spires"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/void/void_interior.png" id="4_interior"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_void_160.png" id="5_p160"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_void_80.png" id="6_p80"]
[ext_resource type="Texture2D" path="res://assets/tiles/void_rift.png" id="7_rift"]
[ext_resource type="Texture2D" path="res://assets/tiles/boss_barrier.png" id="8_barr"]
[ext_resource type="PackedScene" path="res://scenes/player/player.tscn" id="9_player"]
[ext_resource type="PackedScene" path="res://scenes/objects/crystal.tscn" id="10_crys"]
[ext_resource type="PackedScene" path="res://scenes/objects/checkpoint.tscn" id="11_chk"]
[ext_resource type="PackedScene" path="res://scenes/objects/tutorial_sign.tscn" id="12_sign"]
[ext_resource type="PackedScene" path="res://scenes/objects/moving_platform.tscn" id="13_mplat"]
[ext_resource type="PackedScene" path="res://scenes/objects/spike_trap.tscn" id="14_spike"]
[ext_resource type="PackedScene" path="res://scenes/objects/boss_trigger.tscn" id="15_btrig"]
[ext_resource type="PackedScene" path="res://scenes/enemies/shadow_monster.tscn" id="16_sm"]
[ext_resource type="PackedScene" path="res://scenes/enemies/flying_bat.tscn" id="17_bat"]
[ext_resource type="PackedScene" path="res://scenes/enemies/fire_demon.tscn" id="18_fdemon"]
[ext_resource type="PackedScene" path="res://scenes/enemies/boss_void_monarch.tscn" id="19_boss"]
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

[node name="Level6" type="Node2D"]
script = ExtResource("1_ctrl")
level_number = 6
music_track = "dark_dream"
death_y = 650.0

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="LayerSky" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0, 0)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerSky"]
texture = ExtResource("2_sky")
centered = false

[node name="LayerSpires" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.2, 0.05)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerSpires"]
texture = ExtResource("3_spires")
centered = false

[node name="LayerInterior" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.6, 0.1)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerInterior"]
texture = ExtResource("4_interior")
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
        (420, 340), (540, 260), (740, 340), (860, 270),
        (1100, 330), (1240, 250), (1440, 310),
        (2160, 340), (2320, 280), (2480, 340)
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

    # Moving Platform across gap: at X = 800, Y = 390
    tscn += """[node name="MovingPlatform1" parent="." instance=ExtResource("13_mplat")]
position = Vector2(800, 390)
move_offset = Vector2(100, 0)
speed = 50.0

[node name="MovingPlatform2" parent="." instance=ExtResource("13_mplat")]
position = Vector2(1480, 390)
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

    # Ruined Shrine of Rebound (+30% Rebound Gain Rate)
    tscn += """[node name="RuinedShrine" parent="." instance=ExtResource("23_shrine")]
position = Vector2(1240, 226)
stat_buff = "rebound"

"""

    # Signs
    signs = [
        (140, 420, "LEVEL 6: SANCTUM OF THE MYSTERIES\\nPrepare for the Void Monarch! Harness 5x Overdrive ricochets!"),
        (980, 420, "Celestial Void Monarch guards the gateway to the Abyssal Throne!")
    ]
    for i, (sx, sy, msg) in enumerate(signs):
        tscn += f"""[node name="Sign_{i}" parent="." instance=ExtResource("12_sign")]
position = Vector2({sx}, {sy})
message = "{msg}"

"""

    # Crystals
    crys = [
        (220, 410), (340, 350), (540, 220), (740, 300), (860, 230),
        (1100, 290), (1240, 210), (1440, 270), (1640, 410),
        (2160, 300), (2320, 240), (2480, 300)
    ]
    for i, (cx, cy) in enumerate(crys):
        tscn += f"""[node name="Crystal_{i}" parent="." instance=ExtResource("10_crys")]
position = Vector2({cx}, {cy})

"""

    # Enemies
    tscn += """[node name="Enemies" type="Node2D" parent="."]

[node name="FireDemon1" parent="Enemies" instance=ExtResource("18_fdemon")]
position = Vector2(440, 420)

[node name="FlyingBat1" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(660, 240)

[node name="ShadowMonster1" parent="Enemies" instance=ExtResource("16_sm")]
position = Vector2(1180, 420)

[node name="FlyingBat2" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(1400, 240)

"""

    # Boss Arena
    tscn += """[node name="BossArena" type="Node2D" parent="."]

[node name="BossTrigger" parent="BossArena" instance=ExtResource("15_btrig")]
position = Vector2(2040, 360)
boss_node = NodePath("../BossVoidMonarch")

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

[node name="BossVoidMonarch" parent="BossArena" instance=ExtResource("19_boss")]
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
    with open("scenes/levels/level_6.tscn", "w") as f:
        f.write(tscn)
    print("Built scenes/levels/level_6.tscn successfully!")

if __name__ == "__main__":
    build_level_6()
