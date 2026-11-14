extends Node2D

@export var duration: float = 5.0
var timer: float = 0.0
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
	anim.play("active")
	GameManager.shield_active = true
	SoundManager.play_sfx("shield")
	timer = duration

func _process(delta: float) -> void:
	timer -= delta
	# Slight rotation to look magical
	anim.rotation += delta * 1.5
	if timer <= 0.0 or not GameManager.shield_active:
		_deactivate()

func _deactivate() -> void:
	set_process(false)
	GameManager.shield_active = false
	var tween = create_tween()
	tween.tween_property(self, "scale", Vector2(1.3, 1.3), 0.15)
	tween.parallel().tween_property(self, "modulate:a", 0.0, 0.15)
	await tween.finished
	queue_free()
