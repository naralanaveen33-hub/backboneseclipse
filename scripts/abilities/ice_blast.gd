extends Area2D

@export var speed: float = 400.0
@export var damage: float = 30.0
@export var freeze_duration: float = 4.0
var base_damage: float = 30.0

var velocity: Vector2 = Vector2.ZERO
var direction: float = 1.0
var lifetime: float = 2.8
var bounces: int = 0
var max_bounces: int = 2
var is_shattering: bool = false

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	top_level = true
	add_to_group("player_projectiles")
	anim.play("fly")
	base_damage = damage * GameManager.damage_multiplier
	
	if GameManager.is_overdrive:
		max_bounces = 4
		speed *= 1.25
		base_damage *= 1.3
		
	if velocity == Vector2.ZERO:
		velocity = Vector2(direction * speed, 0.0)
	else:
		velocity = velocity.normalized() * speed
		
	rotation = velocity.angle()
	if velocity.x < 0:
		anim.flip_v = true

func _physics_process(delta: float) -> void:
	if is_shattering:
		return
		
	var step = velocity * delta
	var space_state = get_world_2d().direct_space_state
	var query = PhysicsRayQueryParameters2D.create(global_position, global_position + step, 1)
	query.exclude = [self]
	var hit = space_state.intersect_ray(query)
	
	if hit:
		bounces += 1
		var normal: Vector2 = hit.normal
		velocity = velocity.bounce(normal) * 1.15
		global_position = hit.position + normal * 4.0
		rotation = velocity.angle()
		damage = base_damage * (1.0 + float(bounces))
		
		var pitch = 1.2 + (bounces * 0.3)
		SoundManager.play_sfx_pitched("crystal", pitch)
		
		modulate = Color(0.4, 0.95, 1.0).lerp(Color(1.0, 1.0, 1.0), 0.3 * bounces)
		GameManager.pop_floating_text("%dx ICE BOUNCE!" % bounces, global_position, Color(0.3, 0.9, 1.0))
		
		if hit.collider and (hit.collider.is_in_group("shrines") or hit.collider.has_method("activate_shrine")):
			hit.collider.activate_shrine()
			_shatter()
			return
			
		if bounces >= max_bounces:
			_shatter()
			return
	else:
		global_position += step

	lifetime -= delta
	if lifetime <= 0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if is_shattering:
		return
	if body.is_in_group("enemies") or body.has_method("take_damage"):
		body.take_damage(damage, "ice")
		if body.has_method("freeze_enemy"):
			body.freeze_enemy(freeze_duration)
		if bounces > 0:
			GameManager.hit_stop(0.04)
			GameManager.pop_floating_text("FROZEN %d!" % int(damage), body.global_position + Vector2(0, -25), Color(0.3, 0.9, 1.0))
		_shatter()
	elif body.is_in_group("shrines") or body.has_method("activate_shrine"):
		body.activate_shrine()
		_shatter()

func _on_area_entered(area: Area2D) -> void:
	if is_shattering:
		return
	if area.is_in_group("shrines") or area.has_method("activate_shrine"):
		area.activate_shrine()
		_shatter()
		return
	var parent = area.get_parent()
	if parent and (parent.is_in_group("enemies") or parent.has_method("take_damage")):
		parent.take_damage(damage, "ice")
		if parent.has_method("freeze_enemy"):
			parent.freeze_enemy(freeze_duration)
		_shatter()

func _shatter() -> void:
	if is_shattering:
		return
	is_shattering = true
	set_physics_process(false)
	col_shape.set_deferred("disabled", true)
	SoundManager.play_sfx("freeze")
	var tween = create_tween()
	tween.tween_property(anim, "scale", Vector2(1.5, 1.5), 0.15)
	tween.parallel().tween_property(anim, "modulate:a", 0.0, 0.15)
	await tween.finished
	queue_free()
