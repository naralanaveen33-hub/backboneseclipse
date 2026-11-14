extends Area2D

@export var speed: float = 380.0
@export var damage: float = 24.0
@export var homing_strength: float = 0.0

var direction: Vector2 = Vector2.RIGHT
var is_deflected: bool = false
var lifetime: float = 5.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	add_to_group("enemy_projectiles")
	top_level = true
	rotation = direction.angle()
	body_entered.connect(_on_body_entered)
	area_entered.connect(_on_area_entered)

func _physics_process(delta: float) -> void:
	# Optional slight homing towards player if not deflected
	if not is_deflected and homing_strength > 0.0:
		var player = get_tree().get_first_node_in_group("player")
		if player and not player.is_dead:
			var target_dir = (player.global_position - global_position).normalized()
			direction = direction.lerp(target_dir, homing_strength * delta).normalized()
			rotation = direction.angle()
			
	global_position += direction * speed * delta
	sprite.rotation += delta * 12.0
	
	lifetime -= delta
	if lifetime <= 0.0:
		_fade_out()

func deflect(deflect_dir: Vector2) -> void:
	if is_deflected:
		return
	is_deflected = true
	remove_from_group("enemy_projectiles")
	add_to_group("player_projectiles")
	
	direction = deflect_dir.normalized()
	speed *= 2.8
	damage *= 3.0
	rotation = direction.angle()
	modulate = Color(1.8, 1.4, 0.4) # Radiant Golden Deflection
	lifetime = 4.0

func _on_body_entered(body: Node2D) -> void:
	if not is_deflected:
		if body.is_in_group("player") and body.has_method("take_damage"):
			body.take_damage(damage, global_position)
			_explode()
		elif body is StaticBody2D or body is TileMap:
			_explode()
	else:
		if body.is_in_group("enemies") and body.has_method("take_damage"):
			body.take_damage(damage, "deflected")
			GameManager.pop_floating_text("DEFLECT CRIT %d!" % int(damage), body.global_position + Vector2(0, -25), Color(1.0, 0.85, 0.2))
			_explode()
		elif body is StaticBody2D or body is TileMap:
			_explode()

func _on_area_entered(area: Area2D) -> void:
	if is_deflected:
		var parent = area.get_parent()
		if parent and parent.is_in_group("enemies") and parent.has_method("take_damage"):
			parent.take_damage(damage, "deflected")
			GameManager.pop_floating_text("DEFLECT CRIT %d!" % int(damage), parent.global_position + Vector2(0, -25), Color(1.0, 0.85, 0.2))
			_explode()

func _explode() -> void:
	set_physics_process(false)
	col_shape.set_deferred("disabled", true)
	SoundManager.play_sfx("explosion", 0.08)
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.8, 1.8), 0.12)
	tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.12)
	await tween.finished
	queue_free()

func _fade_out() -> void:
	set_physics_process(false)
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.2)
	await tween.finished
	queue_free()
