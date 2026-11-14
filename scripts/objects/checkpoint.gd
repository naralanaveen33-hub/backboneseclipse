extends Area2D

@export var checkpoint_id: int = 1
var is_active: bool = false

@onready var sprite: Sprite2D = $Sprite2D
const TEX_OFF = preload("res://assets/tiles/checkpoint_off.png")
const TEX_ON = preload("res://assets/tiles/checkpoint_on.png")

func _ready() -> void:
	sprite.texture = TEX_OFF

func _on_body_entered(body: Node2D) -> void:
	if not is_active and body.is_in_group("player"):
		is_active = true
		sprite.texture = TEX_ON
		GameManager.set_checkpoint(global_position + Vector2(0, -10))
		
		# Pulse glow
		var tween = create_tween()
		tween.tween_property(sprite, "scale", Vector2(1.2, 1.2), 0.2)
		tween.tween_property(sprite, "scale", Vector2(1.0, 1.0), 0.2)
