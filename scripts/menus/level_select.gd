extends Control

func _ready() -> void:
	SoundManager.play_music("dark_dream")

func _on_tutorial_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(0)

func _on_level_1_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(1)

func _on_level_2_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(2)

func _on_level_3_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(3)

func _on_level_4_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(4)

func _on_level_5_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(5)

func _on_level_6_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(6)

func _on_level_7_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(7)

func _on_level_8_pressed() -> void:
	SoundManager.play_sfx("click")
	GameManager.start_level(8)

func _on_back_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
