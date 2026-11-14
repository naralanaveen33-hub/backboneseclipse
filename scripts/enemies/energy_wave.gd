extends Area2D

@export var speed: float = 400.0
@export var damage: float = 28.0
var direction_x: float = 1.0
var lifetime: float = 3.5

@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	add_to_group("enemy_projectiles")
	top_level = true
	sprite.flip_h = (direction_x < 0)
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	global_position.x += direction_x * speed * delta
	
	# Shimmer pulse
	sprite.modulate.a = 0.85 + sin(lifetime * 16.0) * 0.15
	
	lifetime -= delta
	if lifetime <= 0.0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("take_damage"):
		body.take_damage(damage, global_position)
		_explode()
	elif body is StaticBody2D and not body.is_in_group("platforms"):
		# Hit arena walls
		_explode()

func deflect(deflect_dir: Vector2) -> void:
	direction_x = signf(deflect_dir.x) if abs(deflect_dir.x) > 0.1 else -direction_x
	speed *= 2.0
	damage *= 3.0
	sprite.flip_h = (direction_x < 0)
	modulate = Color(2.0, 1.6, 0.4)
	remove_from_group("enemy_projectiles")
	add_to_group("player_projectiles")

func _explode() -> void:
	set_physics_process(false)
	col_shape.set_deferred("disabled", true)
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.15)
	await tween.finished
	queue_free()
