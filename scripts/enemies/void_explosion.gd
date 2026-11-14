extends Area2D

@export var telegraph_duration: float = 0.55
@export var damage: float = 48.0
@export var explosion_radius: float = 55.0

var is_detonated: bool = false
var has_hit_player: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	add_to_group("enemy_projectiles")
	top_level = true
	col_shape.disabled = true # Disabled during telegraph
	sprite.scale = Vector2(0.4, 0.4)
	sprite.modulate = Color(1.0, 0.2, 0.5, 0.5)
	
	_run_telegraph()

func _run_telegraph() -> void:
	# Warning pulse and grow
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.0, 1.0), telegraph_duration)
	tween.parallel().tween_property(sprite, "modulate:a", 0.9, telegraph_duration)
	await tween.finished
	_detonate()

func _detonate() -> void:
	if not is_inside_tree():
		return
	is_detonated = true
	col_shape.disabled = false
	SoundManager.play_sfx("explosion")
	GameManager.hit_stop(0.04)
	
	# Blast surge
	var blast_tween = create_tween()
	sprite.modulate = Color(2.0, 0.4, 0.8, 1.0)
	blast_tween.tween_property(sprite, "scale", Vector2(2.2, 2.2), 0.22)
	blast_tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.25)
	
	# Check bodies in radius
	var bodies = get_overlapping_bodies()
	for b in bodies:
		_process_body_hit(b)
		
	await blast_tween.finished
	queue_free()

func _on_body_entered(body: Node2D) -> void:
	if is_detonated:
		_process_body_hit(body)

func _process_body_hit(body: Node2D) -> void:
	if not has_hit_player and body.is_in_group("player") and body.has_method("take_damage"):
		has_hit_player = true
		body.take_damage(damage, global_position)
		GameManager.pop_floating_text("VOID BLAST %d!" % int(damage), body.global_position + Vector2(0, -35), Color(1.0, 0.2, 0.4))
