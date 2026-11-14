#!/usr/bin/env python3
"""
Generate updated scenes/menus/level_select.tscn and scripts/menus/level_select.gd for 7 levels.
"""

def build_level_select():
    tscn = """[gd_scene load_steps=9 format=3]

[ext_resource type="Script" path="res://scripts/menus/level_select.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/backgrounds/forest/sky.png" id="2_sky"]
[ext_resource type="Texture2D" path="res://assets/ui/panel_bg.png" id="3_panel"]
[ext_resource type="Texture2D" path="res://assets/ui/button_normal.png" id="4_btn"]
[ext_resource type="Texture2D" path="res://assets/ui/button_hover.png" id="5_hov"]
[ext_resource type="Texture2D" path="res://assets/ui/button_pressed.png" id="6_prs"]

[sub_resource type="LabelSettings" id="LabelSettings_title"]
font_size = 24
font_color = Color(1, 0.88, 0.45, 1)
outline_size = 5
outline_color = Color(0.1, 0.05, 0.15, 1)

[sub_resource type="LabelSettings" id="LabelSettings_btn"]
font_size = 12
font_color = Color(1, 1, 1, 1)
outline_size = 2
outline_color = Color(0, 0, 0, 1)

[node name="LevelSelect" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_script")

[node name="Sky" type="TextureRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
texture = ExtResource("2_sky")
expand_mode = 1

[node name="NinePatchRect" type="NinePatchRect" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -300.0
offset_top = -240.0
offset_right = 300.0
offset_bottom = 240.0
grow_horizontal = 2
grow_vertical = 2
texture = ExtResource("3_panel")
patch_margin_left = 16
patch_margin_top = 16
patch_margin_right = 16
patch_margin_bottom = 16

[node name="VBox" type="VBoxContainer" parent="NinePatchRect"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 20.0
offset_top = 16.0
offset_right = -20.0
offset_bottom = -16.0
grow_horizontal = 2
grow_vertical = 2
theme_override_constants/separation = 8
alignment = 1

[node name="Title" type="Label" parent="NinePatchRect/VBox"]
layout_mode = 2
text = "SELECT REALM (7 LEVELS & BOSSES)"
label_settings = SubResource("LabelSettings_title")
horizontal_alignment = 1

[node name="Grid" type="GridContainer" parent="NinePatchRect/VBox"]
layout_mode = 2
theme_override_constants/h_separation = 12
theme_override_constants/v_separation = 8
columns = 2

"""
    levels = [
        (1, "1: Enchanted Forest (Behemoth)"),
        (2, "2: Dark Castle (Dark Wizard)"),
        (3, "3: Molten Caverns (Magma Titan)"),
        (4, "4: Frozen Crypts (Frost Lich)"),
        (5, "5: Tempest Spire (Storm Archon)"),
        (6, "6: Astral Void (Void Monarch)"),
        (7, "7: Abyssal Throne (Malakor)")
    ]
    for lid, lname in levels:
        tscn += f"""[node name="Level{lid}Btn" type="TextureButton" parent="NinePatchRect/VBox/Grid"]
custom_minimum_size = Vector2(270, 36)
layout_mode = 2
texture_normal = ExtResource("4_btn")
texture_pressed = ExtResource("6_prs")
texture_hover = ExtResource("5_hov")
ignore_texture_size = true
stretch_mode = 0

[node name="Label" type="Label" parent="NinePatchRect/VBox/Grid/Level{lid}Btn"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
text = "{lname}"
label_settings = SubResource("LabelSettings_btn")
horizontal_alignment = 1
vertical_alignment = 1

"""

    tscn += """[node name="BackBtn" type="TextureButton" parent="NinePatchRect/VBox"]
custom_minimum_size = Vector2(250, 36)
layout_mode = 2
size_flags_horizontal = 4
texture_normal = ExtResource("4_btn")
texture_pressed = ExtResource("6_prs")
texture_hover = ExtResource("5_hov")
ignore_texture_size = true
stretch_mode = 0

[node name="Label" type="Label" parent="NinePatchRect/VBox/BackBtn"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
text = "Back to Main Menu"
label_settings = SubResource("LabelSettings_btn")
horizontal_alignment = 1
vertical_alignment = 1

[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level1Btn" to="." method="_on_level_1_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level2Btn" to="." method="_on_level_2_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level3Btn" to="." method="_on_level_3_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level4Btn" to="." method="_on_level_4_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level5Btn" to="." method="_on_level_5_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level6Btn" to="." method="_on_level_6_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/Grid/Level7Btn" to="." method="_on_level_7_pressed"]
[connection signal="pressed" from="NinePatchRect/VBox/BackBtn" to="." method="_on_back_pressed"]
"""
    with open("scenes/menus/level_select.tscn", "w") as f:
        f.write(tscn)
    print("Built scenes/menus/level_select.tscn")

if __name__ == "__main__":
    build_level_select()
