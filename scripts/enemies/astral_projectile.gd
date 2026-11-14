extends Area2D

@export var speed: float = 280.0
@export var damage: float = 30.0
var direction: Vector2 = Vector2.LEFT
var is_deflected: bool = false

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
	top_level = true
	add_to_group("enemy_projectiles")
	anim.play("fly")

func _physics_process(delta: float) -> void:
	position += direction * speed * delta

func deflect(new_dir: Vector2) -> void:
	if is_deflected:
		return
	is_deflected = true
	remove_from_group("enemy_projectiles")
	add_to_group("player_projectiles")
	direction = new_dir.normalized()
	speed *= 3.0
	damage *= 3.0
	collision_layer = 8
	collision_mask = 5 # Enemies & World
	modulate = Color(1.0, 0.9, 0.2)
	scale = Vector2(1.4, 1.4)

func _on_body_entered(body: Node2D) -> void:
	if not is_deflected:
		if body.has_method("take_damage") and body.is_in_group("player"):
			body.take_damage(damage, global_position)
		queue_free()
	else:
		if body.is_in_group("enemies") or body.has_method("take_damage"):
			body.take_damage(damage, "deflected")
			if body.has_method("freeze_enemy"):
				body.freeze_enemy(2.5)
			GameManager.hit_stop(0.06)
			GameManager.pop_floating_text("CRIT %d!" % int(damage), global_position, Color(1.0, 0.9, 0.2))
		queue_free()

func _on_area_entered(area: Area2D) -> void:
	if not is_deflected:
		var parent = area.get_parent()
		if parent and parent.has_method("take_damage") and parent.is_in_group("player"):
			parent.take_damage(damage, global_position)
			queue_free()
	else:
		var parent = area.get_parent()
		if parent and (parent.is_in_group("enemies") or parent.has_method("take_damage")):
			parent.take_damage(damage, "deflected")
			if parent.has_method("freeze_enemy"):
				parent.freeze_enemy(2.5)
			GameManager.hit_stop(0.06)
			GameManager.pop_floating_text("CRIT %d!" % int(damage), global_position, Color(1.0, 0.9, 0.2))
			queue_free()

func _on_timer_timeout() -> void:
	queue_free()
