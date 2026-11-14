extends Control

@onready var crystals_label: Label = $NinePatchRect/VBox/CrystalsLabel

func _ready() -> void:
	SoundManager.play_sfx("victory")
	crystals_label.text = "Crystals Collected: %d" % GameManager.crystals

func _on_play_again_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(1)

func _on_level_select_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/level_select.tscn")

func _on_main_menu_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
