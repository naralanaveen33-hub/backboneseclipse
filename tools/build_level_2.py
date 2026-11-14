import os

def build_level_2():
    tscn = """[gd_scene load_steps=25 format=3]

[ext_resource type="Script" path="res://scripts/systems/level_controller.gd" id="1_ctrl"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/castle/sky.png" id="2_sky"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/castle/spires.png" id="3_spires"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/castle/interior_bg.png" id="4_interior"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_castle_160.png" id="5_p160"]
[ext_resource type="Texture2D" path="res://assets/tiles/platform_castle_80.png" id="6_p80"]
[ext_resource type="Texture2D" path="res://assets/tiles/lava_hazard.png" id="7_lava"]
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
[ext_resource type="PackedScene" path="res://scenes/enemies/boss_dark_wizard.tscn" id="19_boss"]
[ext_resource type="PackedScene" path="res://scenes/ui/hud.tscn" id="20_hud"]
[ext_resource type="PackedScene" path="res://scenes/ui/pause_menu.tscn" id="21_pmenu"]
[ext_resource type="PackedScene" path="res://scenes/ui/game_over_menu.tscn" id="22_gomenu"]
[ext_resource type="PackedScene" path="res://scenes/objects/ruined_shrine.tscn" id="23_shrine"]

[sub_resource type="RectangleShape2D" id="Shape_160"]
size = Vector2(160, 32)

[sub_resource type="RectangleShape2D" id="Shape_80"]
size = Vector2(80, 24)

[sub_resource type="RectangleShape2D" id="Shape_Barrier"]
size = Vector2(32, 280)

[node name="Level2" type="Node2D"]
script = ExtResource("1_ctrl")
level_number = 2
music_track = "castle_theme"
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
motion_scale = Vector2(0.5, 0.1)
motion_mirroring = Vector2(960, 0)

[node name="Sprite2D" type="Sprite2D" parent="ParallaxBackground/LayerInterior"]
texture = ExtResource("4_interior")
centered = false

[node name="Platforms" type="Node2D" parent="."]

"""
    # Castle ground platforms
    p160_coords = [
        (80, 456), (240, 456), (360, 456), # Entrance battlement
        (840, 456), (1000, 456), # Spike & hall ground
        (1300, 332), # High rampart 1
        (1680, 332), (1840, 332), # Antechamber
        (2080, 476), (2240, 476), (2400, 476), (2560, 476), (2720, 476) # Throne Room floor
    ]
    for i, (x, y) in enumerate(p160_coords):
        tscn += f"""[node name="Ground_{i}" type="StaticBody2D" parent="Platforms"]
position = Vector2({x}, {y})
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="Platforms/Ground_{i}"]
texture = ExtResource("5_p160")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Ground_{i}"]
shape = SubResource("Shape_160")

"""

    # Floating stone blocks (80x24)
    p80_coords = [
        (490, 410), (730, 380), # Crossing lava pit 1
        (1160, 390), (1240, 350), # Ascending stairs
        (2180, 360), (2540, 360) # Throne Room tactical platforms
    ]
    for i, (x, y) in enumerate(p80_coords):
        tscn += f"""[node name="Float_{i}" type="StaticBody2D" parent="Platforms"]
position = Vector2({x}, {y})
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="Platforms/Float_{i}"]
texture = ExtResource("6_p80")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Float_{i}"]
shape = SubResource("Shape_80")
one_way_collision = true

"""

    # Lava Hazards (Area2D hazards that damage player on touch)
    # Lava Pit 1: X = 460 to 760
    # Lava Pit 2: X = 1420 to 1640
    lava_coords = [
        (540, 520), (680, 520),
        (1480, 450), (1600, 450)
    ]
    for i, (lx, ly) in enumerate(lava_coords):
        tscn += f"""[node name="Lava_{i}" parent="." instance=ExtResource("14_spike")]
position = Vector2({lx}, {ly})
damage = 40.0

"""

    # Moving platforms over lava
    # 1: X = 600, Y = 370, moves Vector2(80, 0)
    # 2: X = 1440, Y = 330, moves Vector2(120, 0)
    tscn += """[node name="MovingPlatform1" parent="." instance=ExtResource("13_mplat")]
position = Vector2(600, 370)
move_offset = Vector2(80, 0)
speed = 50.0

[node name="MovingPlatform2" parent="." instance=ExtResource("13_mplat")]
position = Vector2(1440, 330)
move_offset = Vector2(110, 0)
speed = 55.0

"""

    # Spike Traps
    spike_coords = [
        (920, 432), (1040, 432), (1800, 308)
    ]
    for i, (sx, sy) in enumerate(spike_coords):
        tscn += f"""[node name="Spike_{i}" parent="." instance=ExtResource("14_spike")]
position = Vector2({sx}, {sy})

"""

    # Checkpoints:
    # Checkpoint 1 at X = 840, Y = 416
    # Checkpoint 2 at X = 1680, Y = 292
    tscn += """[node name="Checkpoint1" parent="." instance=ExtResource("11_chk")]
position = Vector2(840, 416)
checkpoint_id = 1

[node name="Checkpoint2" parent="." instance=ExtResource("11_chk")]
position = Vector2(1680, 292)
checkpoint_id = 2

"""

    # Tutorial / Lore signs
    signs = [
        (120, 420, "THE DARK CASTLE\\nYou have unlocked Lightning Strike [L]!\\nCall down lightning bolts to smite multiple foes."),
        (260, 420, "Press [I] to invoke Magic Shield!\\nForms a barrier absorbing all damage for 4 seconds."),
        (800, 420, "Beware the burning lava and lethal spikes! Use shield to survive damage."),
        (1740, 296, "FINAL BATTLE: The Throne of Shadows.\\nDefeat the Dark Wizard to save the Mystic Realms!")
    ]
    for i, (sx, sy, msg) in enumerate(signs):
        tscn += f"""[node name="Sign_{i}" parent="." instance=ExtResource("12_sign")]
position = Vector2({sx}, {sy})
message = "{msg}"

"""

    # Collectible Crystals
    crys_coords = [
        (200, 400), (490, 360), (600, 320), (730, 330),
        (880, 400), (960, 380),
        (1160, 340), (1240, 300), (1300, 280),
        (1440, 280), (1550, 280),
        (1840, 280),
        (2180, 310), (2540, 310)
    ]
    for i, (cx, cy) in enumerate(crys_coords):
        tscn += f"""[node name="Crystal_{i}" parent="." instance=ExtResource("10_crys")]
position = Vector2({cx}, {cy})

"""

    # Enemies
    tscn += """[node name="Enemies" type="Node2D" parent="."]

[node name="FireDemon1" parent="Enemies" instance=ExtResource("18_fdemon")]
position = Vector2(340, 424)

[node name="FlyingBat1" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(520, 250)

[node name="FlyingBat2" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(680, 230)

[node name="ShadowMonster1" parent="Enemies" instance=ExtResource("16_sm")]
position = Vector2(980, 424)

[node name="FireDemon2" parent="Enemies" instance=ExtResource("18_fdemon")]
position = Vector2(1300, 300)

[node name="FlyingBat3" parent="Enemies" instance=ExtResource("17_bat")]
position = Vector2(1520, 200)

[node name="FireDemon3" parent="Enemies" instance=ExtResource("18_fdemon")]
position = Vector2(1860, 300)

"""

    # Boss Arena: Throne Room
    # Trigger at X = 1960, Y = 360
    # Left barrier at X = 2010, Y = 340
    # Right barrier at X = 2760, Y = 340
    # Dark Wizard at X = 2360, Y = 400
    tscn += """[node name="BossArena" type="Node2D" parent="."]

[node name="BossTrigger" parent="BossArena" instance=ExtResource("15_btrig")]
position = Vector2(1960, 360)
boss_node = NodePath("../BossDarkWizard")

[node name="Anchors" type="Node2D" parent="BossArena/BossTrigger"]

[node name="Anchor1" type="Marker2D" parent="BossArena/BossTrigger/Anchors"]
position = Vector2(220, -50)

[node name="Anchor2" type="Marker2D" parent="BossArena/BossTrigger/Anchors"]
position = Vector2(220, 70)

[node name="Anchor3" type="Marker2D" parent="BossArena/BossTrigger/Anchors"]
position = Vector2(580, -50)

[node name="Anchor4" type="Marker2D" parent="BossArena/BossTrigger/Anchors"]
position = Vector2(580, 70)

[node name="BarrierLeft" type="StaticBody2D" parent="BossArena"]
position = Vector2(2010, 340)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="BossArena/BarrierLeft"]
texture = ExtResource("8_barr")

[node name="CollisionShape2D" type="CollisionShape2D" parent="BossArena/BarrierLeft"]
shape = SubResource("Shape_Barrier")

[node name="BarrierRight" type="StaticBody2D" parent="BossArena"]
position = Vector2(2760, 340)
collision_layer = 1
collision_mask = 6

[node name="Sprite2D" type="Sprite2D" parent="BossArena/BarrierRight"]
texture = ExtResource("8_barr")

[node name="CollisionShape2D" type="CollisionShape2D" parent="BossArena/BarrierRight"]
shape = SubResource("Shape_Barrier")

[node name="BossDarkWizard" parent="BossArena" instance=ExtResource("19_boss")]
position = Vector2(2360, 420)

"""

    # Player & UI
    tscn += """[node name="RuinedShrine" parent="." instance=ExtResource("23_shrine")]
position = Vector2(960, 246)
stat_buff = "speed"

[node name="Player" parent="." instance=ExtResource("9_player")]
position = Vector2(60, 410)

[node name="HUD" parent="." instance=ExtResource("20_hud")]

[node name="PauseMenu" parent="." instance=ExtResource("21_pmenu")]

[node name="GameOverMenu" parent="." instance=ExtResource("22_gomenu")]
"""
    with open("scenes/levels/level_2.tscn", "w") as f:
        f.write(tscn)
    print("Built scenes/levels/level_2.tscn")

if __name__ == "__main__":
    build_level_2()
