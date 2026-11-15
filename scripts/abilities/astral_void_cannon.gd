extends Area2D

@export var speed: float = 620.0
@export var damage: float = 650.0
var base_damage: float = 650.0

var velocity: Vector2 = Vector2.ZERO
var direction: float = 1.0
var lifetime: float = 3.5
var bounces: int = 0
var max_bounces: int = 4
var is_exploding: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	top_level = true
	add_to_group("player_projectiles")
	base_damage = damage * GameManager.damage_multiplier
	
	if GameManager.is_overdrive:
		max_bounces = 6
		speed *= 1.35
		base_damage *= 1.5
		modulate = Color(1.8, 1.4, 0.5)
	else:
		modulate = Color(1.2, 0.8, 1.8)
		
	if velocity == Vector2.ZERO:
		velocity = Vector2(direction * speed, 0.0)
	else:
		velocity = velocity.normalized() * speed
		
	rotation = velocity.angle()
	body_entered.connect(_on_body_entered)
	area_entered.connect(_on_area_entered)
	SoundManager.play_sfx("lightning")
	SoundManager.play_sfx_pitched("crystal", 0.7)

func _physics_process(delta: float) -> void:
	if is_exploding:
		return
		
	var step = velocity * delta
	var space_state = get_world_2d().direct_space_state
	
	# Raycast against World Geometry (Collision Layer 1)
	var query = PhysicsRayQueryParameters2D.create(global_position, global_position + step, 1)
	query.exclude = [self]
	var hit = space_state.intersect_ray(query)
	
	if hit:
		bounces += 1
		var normal: Vector2 = hit.normal
		velocity = velocity.bounce(normal) * 1.12
		global_position = hit.position + normal * 4.0
		rotation = velocity.angle()
		
		# Multiplier scaling
		damage = base_damage * (1.0 + float(bounces) * 0.5)
		SoundManager.play_sfx_pitched("crystal", 1.2 + float(bounces) * 0.3)
		GameManager.pop_floating_text("ASTRAL BOUNCE %dx!" % (bounces + 1), global_position, Color(0.8, 0.4, 1.0))
		
		if hit.collider and (hit.collider.is_in_group("shrines") or hit.collider.has_method("activate_shrine")):
			hit.collider.activate_shrine()
			_explode()
			return
			
		if bounces >= max_bounces:
			_explode()
			return
	else:
		global_position += step
		
	# Trailing cosmic pulse
	sprite.rotation += delta * 15.0
	
	lifetime -= delta
	if lifetime <= 0.0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if is_exploding:
		return
	if body.is_in_group("enemies") or body.has_method("take_damage"):
		body.take_damage(damage, "void")
		GameManager.hit_stop(0.08)
		GameManager.pop_floating_text("ASTRAL OBLIVION %d!" % int(damage), body.global_position + Vector2(0, -35), Color(0.9, 0.3, 1.0))
		GameManager.add_rebound(20.0)
		_explode()
	elif body.is_in_group("shrines") or body.has_method("activate_shrine"):
		body.activate_shrine()
		_explode()

func _on_area_entered(area: Area2D) -> void:
	if is_exploding:
		return
	if area.is_in_group("shrines") or area.has_method("activate_shrine"):
		area.activate_shrine()
		_explode()
		return
		
	# Pierces boss shields directly!
	if area.is_in_group("boss_shield"):
		if area.has_method("take_damage"):
			area.take_damage(damage * 2.0, "void")
		GameManager.pop_floating_text("SHIELD PIERCED!", area.global_position + Vector2(0, -40), Color(1.0, 0.2, 0.5))
		_explode()
		return

	var parent = area.get_parent()
	if parent and (parent.is_in_group("enemies") or parent.has_method("take_damage")):
		parent.take_damage(damage, "void")
		GameManager.hit_stop(0.08)
		GameManager.pop_floating_text("ASTRAL OBLIVION %d!" % int(damage), parent.global_position + Vector2(0, -35), Color(0.9, 0.3, 1.0))
		GameManager.add_rebound(20.0)
		_explode()

func _explode() -> void:
	if is_exploding:
		return
	is_exploding = true
	set_physics_process(false)
	col_shape.set_deferred("disabled", true)
	SoundManager.play_sfx("explosion", 0.05)
	
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(2.5, 2.5), 0.16)
	tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.16)
	await tween.finished
	queue_free()
