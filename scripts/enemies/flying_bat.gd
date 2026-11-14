extends EnemyBase

@export var swoop_range: float = 200.0
@export var return_speed: float = 80.0
@export var dive_speed: float = 160.0

var home_pos: Vector2 = Vector2.ZERO
var is_diving: bool = false
var dive_target: Vector2 = Vector2.ZERO
var hover_time: float = 0.0

func _ready() -> void:
	max_hp = 30.0
	speed = dive_speed
	damage = 10.0
	super._ready()
	home_pos = global_position
	anim.play("fly")

func _physics_process(delta: float) -> void:
	if is_dead or is_frozen:
		velocity = Vector2.ZERO
		return

	hover_time += delta
	var player = get_tree().get_first_node_in_group("player")

	if not is_diving:
		# Check for player
		if player and not player.is_dead and global_position.distance_to(player.global_position) <= swoop_range:
			is_diving = true
			dive_target = player.global_position
		else:
			# Gentle hovering near home position
			var hover_offset = Vector2(0, sin(hover_time * 3.0) * 8.0)
			global_position = global_position.move_toward(home_pos + hover_offset, return_speed * delta)
	else:
		# Swooping towards target
		var dir = (dive_target - global_position).normalized()
		velocity = dir * dive_speed
		move_and_slide()
		anim.flip_h = (dir.x < 0)
		
		# Once reached target or hit wall, return
		if global_position.distance_to(dive_target) < 16.0 or is_on_wall():
			is_diving = false
			# Update home pos slightly
			await get_tree().create_timer(0.4).timeout
