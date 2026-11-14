extends Area2D

@export var requires_boss_defeat: bool = true
var is_open: bool = false

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
	if requires_boss_defeat:
		is_open = false
		modulate.a = 0.3
		GameManager.boss_defeated.connect(_on_boss_defeated)
	else:
		is_open = true
		modulate.a = 1.0
	anim.play("spin")

func _on_boss_defeated() -> void:
	is_open = true
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 1.0, 0.5)
	GameManager.post_notification("The Portal has opened!")

func _on_body_entered(body: Node2D) -> void:
	if is_open and body.is_in_group("player"):
		GameManager.complete_level()
