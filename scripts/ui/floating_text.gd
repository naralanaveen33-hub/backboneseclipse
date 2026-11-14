extends Node2D

@onready var label: Label = $Label

func setup(text: String, start_pos: Vector2, color: Color = Color.WHITE) -> void:
	global_position = start_pos
	global_position.x += randf_range(-12.0, 12.0)
	label.text = text
	label.add_theme_color_override("font_color", color)
	
	scale = Vector2(0.6, 0.6)
	modulate.a = 1.0
	
	var tween = create_tween().set_parallel(true)
	tween.tween_property(self, "position:y", position.y - 48.0, 0.75).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "scale", Vector2(1.15, 1.15), 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	
	var fade_tween = create_tween()
	fade_tween.tween_interval(0.40)
	fade_tween.tween_property(self, "modulate:a", 0.0, 0.35)
	fade_tween.tween_callback(queue_free)
