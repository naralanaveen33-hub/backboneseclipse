extends CanvasLayer

@onready var panel: Control = $Panel

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	panel.visible = false

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause") and not event.is_echo():
		toggle_pause()

func toggle_pause() -> void:
	var paused = not get_tree().paused
	get_tree().paused = paused
	panel.visible = paused
	if paused:
		SoundManager.play_sfx("click")

func _on_resume_pressed() -> void:
	SoundManager.play_sfx("click")
	toggle_pause()

func _on_restart_checkpoint_pressed() -> void:
	SoundManager.play_sfx("click")
	toggle_pause()
	GameManager.respawn_player()

func _on_restart_level_pressed() -> void:
	SoundManager.play_sfx("click")
	toggle_pause()
	GameManager.start_level(GameManager.current_level)

func _on_main_menu_pressed() -> void:
	SoundManager.play_sfx("click")
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
