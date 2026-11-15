extends EnemyBase

@export var boss_name: String = "CORRUPTED SHADOW BEHEMOTH"
var is_active: bool = false
var is_attacking: bool = false
var attack_state: int = 0
var attack_timer: float = 1.8
var facing: float = -1.0

const SCENE_DARK_ORB = preload("res://scenes/enemies/dark_orb_projectile.tscn")

signal boss_died()

func _ready() -> void:
	max_hp = 800.0
	damage = 200.0
	speed = 75.0
	crystals_dropped = 12
	super._ready()
	anim.play("idle")

func activate_boss() -> void:
	if is_active:
		return
	is_active = true
	SoundManager.play_sfx("boss_roar")
	SoundManager.play_music("dark_dream")
	GameManager.boss_spawned.emit(boss_name, max_hp)
	attack_timer = 1.5

func _physics_process(delta: float) -> void:
	var player = get_tree().get_first_node_in_group("player")
	
	# Auto-activate when player gets close to arena
	if not is_active and player and not player.is_dead:
		if global_position.distance_to(player.global_position) < 420.0:
			activate_boss()

	if not is_active or is_dead or is_frozen:
		velocity = Vector2.ZERO
		return

	if not is_on_floor():
		velocity.y += 980.0 * delta

	if player and not player.is_dead:
		facing = signf(player.global_position.x - global_position.x)
		anim.flip_h = (facing > 0)
	else:
		facing = -1.0

	# Attack cooldown countdown
	if not is_attacking:
		attack_timer -= delta
		if attack_timer <= 0.0 and player and not player.is_dead:
			_start_attack(player)

	# Movement: pace toward player if not attacking
	if not is_attacking and is_on_floor():
		velocity.x = facing * speed
		if anim.animation != "idle":
			anim.play("idle")
	elif is_attacking and attack_state != 2:
		velocity.x = 0.0

	move_and_slide()

func _start_attack(player: Node2D) -> void:
	is_attacking = true
	attack_state = (attack_state + 1) % 3
	attack_timer = 2.4 # Immediately reset timer so it never double-triggers!
	
	match attack_state:
		0:
			_attack_shadow_spores(player)
		1:
			_attack_ground_slam(player)
		2:
			_attack_charge(player)

func _attack_shadow_spores(player: Node2D) -> void:
	# Deflectable projectile attack: shoots 3 dark spores!
	anim.play("attack")
	SoundManager.play_sfx("fireball", 0.1)
	
	var base_dir = (player.global_position - global_position).normalized()
	for i in range(3):
		var orb = SCENE_DARK_ORB.instantiate()
		orb.global_position = global_position + Vector2(facing * 20.0, -10.0)
		var angle_offset = (i - 1) * 0.22
		orb.direction = base_dir.rotated(angle_offset)
		get_parent().add_child(orb)
		
	await get_tree().create_timer(0.5).timeout
	if not is_dead and not is_frozen:
		anim.play("idle")
	is_attacking = false

func _attack_ground_slam(player: Node2D) -> void:
	anim.play("attack")
	SoundManager.play_sfx("boss_roar")
	
	await get_tree().create_timer(0.35).timeout
	SoundManager.play_sfx("explosion")
	GameManager.hit_stop(0.04)
	
	# Deals area damage if player is close and not airborne
	if not is_dead and player and not player.is_dead:
		var d = global_position.distance_to(player.global_position)
		if d < 140.0 and player.is_on_floor():
			player.take_damage(damage, global_position)
			GameManager.pop_floating_text("SHOCKWAVE!", player.global_position + Vector2(0, -25), Color(1.0, 0.3, 0.2))
			
	await get_tree().create_timer(0.4).timeout
	if not is_dead and not is_frozen:
		anim.play("idle")
	is_attacking = false

func _attack_charge(player: Node2D) -> void:
	SoundManager.play_sfx("boss_roar")
	anim.play("idle")
	var charge_dir = facing
	var charge_duration = 0.10


	
	while charge_duration > 0 and not is_dead and not is_frozen:
		velocity.x = charge_dir * speed * 2.4
		move_and_slide()
		
		# Contact damage during charge
		if player and not player.is_dead and global_position.distance_to(player.global_position) < 45.0:
			player.take_damage(damage, global_position)
			break
			
		charge_duration -= get_physics_process_delta_time()
		await get_tree().physics_frame
		
	velocity.x = 0.0
	is_attacking = false

func take_damage(amount: float, type: String = "magic") -> void:
	super.take_damage(amount, type)
	GameManager.boss_health_changed.emit(hp, max_hp)

func die() -> void:
	is_active = false
	is_attacking = false
	GameManager.boss_defeated.emit()
	boss_died.emit()
	super.die()
