import os

def build_level_1():
    tscn = """[gd_scene load_steps=23 format=3]

[ext_resource type="Script" path="res://scripts/systems/level_controller.gd" id="1_ctrl"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/forest/sky.png" id="2_sky"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/forest/mountains.png" id="3_mount"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/forest/trees_bg.png" id="4_trees_bg"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/forest/trees_fg.png" id="5_trees_fg"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_forest_160.png" id="6_p160"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_forest_80.png" id="7_p80"]
[ext_resource type="Texture2D" path="res://assets/tiles/boss_barrier.png" id="8_barr"]
[ext_resource type="PackedScene" path="res://scenes/player/player.tscn" id="9_player"]
[ext_resource type="PackedScene" path="res://scenes/objects/crystal.tscn" id="10_crys"]
[ext_resource type="PackedScene" path="res://scenes/objects/checkpoint.tscn" id="11_chk"]
[ext_resource type="PackedScene" path="res://scenes/objects/tutorial_sign.tscn" id="12_sign"]
[ext_resource type="PackedScene" path="res://scenes/objects/moving_platform.tscn" id="13_mplat"]
[ext_resource type="PackedScene" path="res://scenes/objects/level_portal.tscn" id="14_port"]
[ext_resource type="PackedScene" path="res://scenes/objects/boss_trigger.tscn" id="15_btrig"]
[ext_resource type="PackedScene" path="res://scenes/enemies/shadow_monster.tscn" id="16_sm"]
[ext_resource type="PackedScene" path="res://scenes/enemies/flying_bat.tscn" id="17_bat"]
[ext_resource type="PackedScene" path="res://scenes/enemies/boss_mini.tscn" id="18_boss"]
[ext_resource type="PackedScene" path="res://scenes/ui/hud.tscn" id="19_hud"]
[ext_resource type="PackedScene" path="res://scenes/ui/pause_menu.tscn" id="20_pmenu"]
[ext_resource type="PackedScene" path="res://scenes/ui/game_over_menu.tscn" id="21_gomenu"]
[ext_resource type="PackedScene" path="res://scenes/objects/ruined_shrine.tscn" id="22_shrine"]

[sub_resource type="RectangleShape2D" id="Shape_160"]
size = Vector2(160, 32)

[sub_resource type="RectangleShape2D" id="Shape_80"]
size = Vector2(80, 24)

[sub_resource type="RectangleShape2D" id="Shape_Barrier"]
size = Vector2(32, 280)

[node name="Level1" type="Node2D"]
script = ExtResource("1_ctrl")
level_number = 1
music_track = "forest_theme"
death_y = 650.0

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="LayerSky" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0, 0)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerSky"]
texture = ExtResource("2_sky")
centered = false

[node name="LayerMountains" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.2, 0.05)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerMountains"]
texture = ExtResource("3_mount")
centered = false

[node name="LayerTreesBG" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.45, 0.1)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerTreesBG"]
texture = ExtResource("4_trees_bg")
centered = false

[node name="LayerTreesFG" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.75, 0.15)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerTreesFG"]
texture = ExtResource("5_trees_fg")
centered = false

[node name="Platforms" type="Node2D" parent="."]

"""
    # Ground platforms (160x32)
    # Start: X = 0, 160, 320 (Y=440)
    # Mid: X = 800, 960, 1120 (Y=440)
    # Pre-Boss: X = 1580, 1740 (Y=440)
    # Boss: X = 1900, 2060, 2220, 2380, 2540 (Y=460)
    p160_coords = [
        (80, 456), (240, 456), (400, 456), # start
        (880, 456), (1040, 456), (1200, 456), # mid
        (1620, 456), (1780, 456), # pre-boss
        (1960, 476), (2120, 476), (2280, 476), (2440, 476), (2600, 476) # boss arena
    ]
    for i, (x, y) in enumerate(p160_coords):
        tscn += f"""[node name="Ground_{i}" type="StaticBody2D" parent="Platforms"]
position = Vector2({x}, {y})
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="Platforms/Ground_{i}"]
texture = ExtResource("6_p160")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Ground_{i}"]
shape = SubResource("Shape_160")

"""

    # Floating platforms (80x24)
    # X = 520, Y = 400; X = 630, Y = 340; X = 740, Y = 390
    # X = 1380, Y = 340; X = 1490, Y = 280
    # Boss Arena tactical platforms: X = 2080, Y = 360; X = 2360, Y = 360
    p80_coords = [
        (530, 410), (640, 350), (750, 400),
        (1380, 370), (1490, 310),
        (2080, 370), (2360, 370)
    ]
    for i, (x, y) in enumerate(p80_coords):
        tscn += f"""[node name="Float_{i}" type="StaticBody2D" parent="Platforms"]
position = Vector2({x}, {y})
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="Platforms/Float_{i}"]
texture = ExtResource("7_p80")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Float_{i}"]
shape = SubResource("Shape_80")
one_way_collision = true

"""

    # Moving Platform across gap: at X = 1260, Y = 430, moves Vector2(100, 0)
    tscn += """[node name="MovingPlatform" parent="." instance=ExtResource("13_mplat")]
position = Vector2(1260, 430)
move_offset = Vector2(90, 0)
speed = 45.0

"""

    # Checkpoints
    # Checkpoint 1 at X = 860, Y = 416
    # Checkpoint 2 at X = 1660, Y = 416
    tscn += """[node name="Checkpoint1" parent="." instance=ExtResource("11_chk")]
position = Vector2(860, 416)
checkpoint_id = 1

[node name="Checkpoint2" parent="." instance=ExtResource("11_chk")]
position = Vector2(1660, 416)
checkpoint_id = 2

"""

    # Tutorial signs
    signs = [
        (120, 420, "⚡ BOUNCE BACK!\\n[A] / [D] Move, [Space] Jump, [J / L-Click] Cast Fireball!"),
        (280, 420, "RICOCHET COMBAT:\\nFireballs bounce off walls & floors! Each bounce multiplies damage (1x->2x->3x)!"),
        (520, 420, "MAGICAL RECOIL BOOST:\\nAim downwards with mouse or hold [S] while casting to rocket-jump!"),
        (640, 316, "PARRY DEFLECT:\\nRight-Click or [Shift]/[I] to reflect enemy projectiles with 3x speed & stun!"),
        (880, 420, "RUINED SHRINES:\\nAwaken dormant shrines with ricocheted spells for permanent stat buffs!"),
        (1100, 420, "REBOUND OVERDRIVE:\\nNear-misses & hits charge your Rebound Meter! Press [Q] when full!"),
        (1760, 420, "DANGER: The Corrupted Shadow Behemoth guards the forest exit! Parry its strikes!")
    ]
    for i, (sx, sy, msg) in enumerate(signs):
        tscn += f"""[node name="Sign_{i}" parent="." instance=ExtResource("12_sign")]
position = Vector2({sx}, {sy})
message = "{msg}"

"""

    # Collectible Crystals
    crys_coords = [
        (200, 400), (320, 400),
        (530, 360), (640, 300), (750, 350),
        (940, 400), (1080, 400),
        (1300, 380), (1380, 320), (1490, 260),
        (2080, 320), (2360, 320)
    ]
    for i, (cx, cy) in enumerate(crys_coords):
        tscn += f"""[node name="Crystal_{i}" parent="." instance=ExtResource("10_crys")]
position = Vector2({cx}, {cy})

"""

    # Enemies
    # Shadow monsters on ground
    tscn += """[node name="Enemies" type="Node2D" parent="."]

[node name="ShadowMonster1" parent="Enemies" instance=ExtResource("16_sm")]
position = Vector2(380, 424)

[node name="FlyingBat1" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(580, 260)

[node name="FlyingBat2" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(740, 240)

[node name="ShadowMonster2" parent="Enemies" instance=ExtResource("16_sm")]
position = Vector2(1040, 424)

[node name="FlyingBat3" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(1380, 260)

[node name="ShadowMonster3" parent="Enemies" instance=ExtResource("16_sm")]
position = Vector2(1540, 424)

"""

    # Boss Arena:
    # Trigger at X = 1840, Y = 360
    # Left Barrier at X = 1890, Y = 340
    # Right Barrier at X = 2540, Y = 340
    # Boss Mini at X = 2220, Y = 430
    # Portal at X = 2480, Y = 436
    tscn += """[node name="BossArena" type="Node2D" parent="."]

[node name="BossTrigger" parent="BossArena" instance=ExtResource("15_btrig")]
position = Vector2(1840, 360)
boss_node = NodePath("../BossMini")

[node name="BarrierLeft" type="StaticBody2D" parent="BossArena"]
position = Vector2(1890, 340)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="BossArena/BarrierLeft"]
texture = ExtResource("8_barr")

[node name="CollisionShape2D" type="CollisionShape2D" parent="BossArena/BarrierLeft"]
shape = SubResource("Shape_Barrier")

[node name="BarrierRight" type="StaticBody2D" parent="BossArena"]
position = Vector2(2540, 340)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="BossArena/BarrierRight"]
texture = ExtResource("8_barr")

[node name="CollisionShape2D" type="CollisionShape2D" parent="BossArena/BarrierRight"]
shape = SubResource("Shape_Barrier")

[node name="BossMini" parent="BossArena" instance=ExtResource("18_boss")]
position = Vector2(2220, 430)

[node name="LevelPortal" parent="BossArena" instance=ExtResource("14_port")]
position = Vector2(2480, 436)

"""

    # Player & UI
    tscn += """[node name="RuinedShrine" parent="." instance=ExtResource("22_shrine")]
position = Vector2(820, 246)
stat_buff = "hp"

[node name="Player" parent="." instance=ExtResource("9_player")]
position = Vector2(60, 410)

[node name="HUD" parent="." instance=ExtResource("19_hud")]

[node name="PauseMenu" parent="." instance=ExtResource("20_pmenu")]

[node name="GameOverMenu" parent="." instance=ExtResource("21_gomenu")]
"""
    with open("scenes/levels/level_1.tscn", "w") as f:
        f.write(tscn)
    print("Built scenes/levels/level_1.tscn")

if __name__ == "__main__":
    build_level_1()
