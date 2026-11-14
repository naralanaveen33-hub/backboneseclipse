extends Control

func _ready() -> void:
	SoundManager.play_music("dark_dream")

func _on_start_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(1)

func _on_level_select_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/level_select.tscn")

func _on_quit_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().quit()
