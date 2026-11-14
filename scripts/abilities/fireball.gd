extends Area2D

@export var speed: float = 460.0
@export var damage: float = 45.0
var base_damage: float = 45.0

var velocity: Vector2 = Vector2.ZERO
var direction: float = 1.0
var lifetime: float = 3.2
var bounces: int = 0
var max_bounces: int = 3
var is_exploding: bool = false

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	top_level = true
	add_to_group("player_projectiles")
	anim.play("fly")
	
	base_damage = damage * GameManager.damage_multiplier
	
	if GameManager.is_overdrive:
		max_bounces = 5
		speed *= 1.3
		base_damage *= 1.4
		modulate = Color(1.0, 0.9, 0.3)
	
	if velocity == Vector2.ZERO:
		velocity = Vector2(direction * speed, 0.0)
	else:
		velocity = velocity.normalized() * speed
		
	# Rotate to face velocity
	rotation = velocity.angle()
	if velocity.x < 0:
		anim.flip_v = true

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
		
		# Ricochet bounce physics
		velocity = velocity.bounce(normal) * 1.15 # +15% speed per bounce
		global_position = hit.position + normal * 4.0
		rotation = velocity.angle()
		
		# Damage multiplier (1x -> 2x -> 3x -> 4x -> 5x)
		damage = base_damage * (1.0 + float(bounces))
		
		# Pitch-escalating audio ping
		var pitch = 1.0 + (bounces * 0.25)
		SoundManager.play_sfx_pitched("crystal", pitch)
		
		# Color glow shift
		match bounces:
			1:
				modulate = Color(1.0, 0.85, 0.2) # Bright Amber
			2:
				modulate = Color(0.2, 0.9, 1.0)  # Electric Cyan
			3:
				modulate = Color(1.0, 0.3, 0.9)  # Prismatic Magenta
			_:
				modulate = Color(1.0, 1.0, 0.4)  # Solar Overdrive
				
		# Game jam floating combo feedback
		GameManager.pop_floating_text("%dx BOUNCE!" % bounces, global_position, modulate)
		
		# Check if the collided surface was a shrine
		if hit.collider and (hit.collider.is_in_group("shrines") or hit.collider.has_method("activate_shrine")):
			hit.collider.activate_shrine()
			_explode()
			return
			
		if bounces >= max_bounces:
			_explode()
			return
	else:
		global_position += step

	lifetime -= delta
	if lifetime <= 0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if is_exploding:
		return
	if body.is_in_group("enemies") or body.has_method("take_damage"):
		body.take_damage(damage, "fire")
		if bounces > 0 or GameManager.is_overdrive:
			GameManager.hit_stop(0.04 * max(1, bounces))
			GameManager.pop_floating_text("CRIT %d!" % int(damage), body.global_position + Vector2(0, -25), modulate)
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
		
	var parent = area.get_parent()
	if parent and (parent.is_in_group("enemies") or parent.has_method("take_damage")):
		parent.take_damage(damage, "fire")
		if bounces > 0 or GameManager.is_overdrive:
			GameManager.hit_stop(0.04 * max(1, bounces))
			GameManager.pop_floating_text("CRIT %d!" % int(damage), parent.global_position + Vector2(0, -25), modulate)
		_explode()

func _explode() -> void:
	if is_exploding:
		return
	is_exploding = true
	set_physics_process(false)
	col_shape.set_deferred("disabled", true)
	SoundManager.play_sfx("explosion", 0.05)
	anim.play("explode")
	await anim.animation_finished
	queue_free()
