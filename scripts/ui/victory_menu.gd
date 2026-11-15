extends Control

@onready var crystals_label: Label = $NinePatchRect/VBox/CrystalsLabel
@onready var stats_label: Label = $NinePatchRect/VBox/StatsLabel if has_node("NinePatchRect/VBox/StatsLabel") else null

func _ready() -> void:
	SoundManager.play_sfx("victory")
	crystals_label.text = "Crystals Collected: %d" % GameManager.crystals
	if stats_label:
		stats_label.text = "💀 Total Deaths: %d  |  🔄 Total Respawns: %d" % [GameManager.death_count, GameManager.respawn_count]

func _on_play_again_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(1)

func _on_level_select_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/level_select.tscn")

func _on_main_menu_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
