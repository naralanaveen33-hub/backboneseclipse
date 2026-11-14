extends Area2D

@export var max_scale: float = 3.6
@export var expansion_speed: float = 4.2
@export var damage: float = 22.0
@export var stun_duration: float = 1.8

var current_scale: float = 0.3
var is_active: bool = true
var has_hit_player: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	add_to_group("enemy_projectiles")
	top_level = true
	scale = Vector2(current_scale, current_scale)
	body_entered.connect(_on_body_entered)
	SoundManager.play_sfx("lightning")

func _physics_process(delta: float) -> void:
	current_scale += expansion_speed * delta
	scale = Vector2(current_scale, current_scale)
	sprite.rotation += delta * 8.0
	
	# Fade out towards the end of expansion
	var t = current_scale / max_scale
	modulate.a = maxf(0.0, 1.0 - t)
	
	if current_scale >= max_scale:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if not has_hit_player and body.is_in_group("player"):
		has_hit_player = true
		if body.has_method("take_damage"):
			body.take_damage(damage, global_position)
		if body.has_method("stun"):
			body.stun(stun_duration)
		GameManager.pop_floating_text("SHOCKWAVE STUN!", body.global_position + Vector2(0, -35), Color(0.3, 0.9, 1.0))

func deflect(_deflect_dir: Vector2) -> void:
	# If player timed parries the shockwave, prevent stun and damage!
	has_hit_player = true
	modulate = Color(2.0, 2.0, 0.5, 0.4)
	GameManager.pop_floating_text("SHOCK DEFLECTED!", global_position, Color(1.0, 0.9, 0.2))
