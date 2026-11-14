extends CanvasLayer

@onready var panel: Control = $Panel

func _ready() -> void:
	panel.visible = false
	GameManager.player_died.connect(_on_player_died)
	GameManager.player_respawned.connect(_on_player_respawned)

func _on_player_died() -> void:
	await get_tree().create_timer(1.2).timeout
	panel.visible = true
	panel.modulate.a = 0.0
	var tween = create_tween()
	tween.tween_property(panel, "modulate:a", 1.0, 0.4)

func _on_player_respawned() -> void:
	panel.visible = false

func _on_respawn_pressed() -> void:
	SoundManager.play_sfx("click")
	panel.visible = false
	GameManager.respawn_player()

func _on_restart_level_pressed() -> void:
	SoundManager.play_sfx("click")
	panel.visible = false
	GameManager.start_level(GameManager.current_level)

func _on_main_menu_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
