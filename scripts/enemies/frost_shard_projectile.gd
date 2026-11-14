extends Area2D

@export var speed: float = 300.0
@export var damage: float = 24.0
var direction: Vector2 = Vector2.LEFT
var is_deflected: bool = false

func _ready() -> void:
	top_level = true
	add_to_group("enemy_projectiles")
	rotation = direction.angle()

func _physics_process(delta: float) -> void:
	position += direction * speed * delta

func deflect(new_dir: Vector2) -> void:
	if is_deflected:
		return
	is_deflected = true
	remove_from_group("enemy_projectiles")
	add_to_group("player_projectiles")
	direction = new_dir.normalized()
	rotation = direction.angle()
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
				body.freeze_enemy(3.0) # Deflected frost freezes the boss!
			GameManager.hit_stop(0.06)
			GameManager.pop_floating_text("FROZEN CRIT %d!" % int(damage), global_position, Color(0.3, 0.9, 1.0))
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
				parent.freeze_enemy(3.0)
			GameManager.hit_stop(0.06)
			GameManager.pop_floating_text("FROZEN CRIT %d!" % int(damage), global_position, Color(0.3, 0.9, 1.0))
			queue_free()

func _on_timer_timeout() -> void:
	queue_free()
