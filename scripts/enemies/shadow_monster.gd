extends EnemyBase

@export var patrol_distance: float = 120.0
@export var detection_range: float = 160.0
@export var attack_range: float = 40.0

var start_x: float = 0.0
var direction: float = 1.0
var is_chasing: bool = false
var is_attacking: bool = false
var attack_cooldown: float = 0.0

func _ready() -> void:
	super._ready()
	start_x = global_position.x
	anim.play("walk")

func _physics_process(delta: float) -> void:
	if is_dead or is_frozen:
		velocity = Vector2.ZERO
		return

	# Apply gravity
	if not is_on_floor():
		velocity.y += 980.0 * delta

	attack_cooldown -= delta

	# Check player distance
	var player = get_tree().get_first_node_in_group("player")
	if player and not player.is_dead:
		var dist = global_position.distance_to(player.global_position)
		if dist <= attack_range and attack_cooldown <= 0.0:
			_attack_player(player)
			return
		elif dist <= detection_range:
			is_chasing = true
			direction = signf(player.global_position.x - global_position.x)
		else:
			is_chasing = false
	else:
		is_chasing = false

	# Movement
	if not is_attacking:
		if is_chasing:
			velocity.x = direction * speed * 1.3
		else:
			# Patrol back and forth
			if abs(global_position.x - start_x) > patrol_distance:
				direction = -signf(global_position.x - start_x)
			if is_on_wall():
				direction *= -1.0
			velocity.x = direction * speed

		anim.flip_h = (direction < 0)
		if anim.animation != "walk":
			anim.play("walk")

	move_and_slide()

func _attack_player(player: Node2D) -> void:
	is_attacking = true
	velocity.x = 0.0
	anim.play("attack")
	direction = signf(player.global_position.x - global_position.x)
	anim.flip_h = (direction < 0)
	
	await anim.animation_finished
	if not is_dead and not is_frozen and player and global_position.distance_to(player.global_position) <= attack_range + 10.0:
		player.take_damage(damage, global_position)
	is_attacking = false
	attack_cooldown = 0.26
	
