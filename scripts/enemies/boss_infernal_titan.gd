extends EnemyBase

@export var boss_name: String = "INFERNAL MAGMA TITAN"
var is_active: bool = false
var is_attacking: bool = false
var attack_state: int = 0
var attack_timer: float = 1.6
var facing: float = -1.0

const SCENE_MAGMA_ORB = preload("res://scenes/enemies/magma_orb_projectile.tscn")

signal boss_died()

func _ready() -> void:
	max_hp = 900.0
	damage = 32.0
	speed = 65.0
	crystals_dropped = 18
	super._ready()
	anim.play("idle")
	modulate = Color(1.3, 0.7, 0.4) # Fiery molten glow

func activate_boss() -> void:
	if is_active:
		return
	is_active = true
	SoundManager.play_sfx("boss_roar")
	SoundManager.play_music("dark_dream")
	GameManager.boss_spawned.emit(boss_name, max_hp)
	attack_timer = 1.4

func _physics_process(delta: float) -> void:
	var player = get_tree().get_first_node_in_group("player")
	
	if not is_active and player and not player.is_dead:
		if global_position.distance_to(player.global_position) < 460.0:
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

	if not is_attacking:
		attack_timer -= delta
		if attack_timer <= 0.0 and player and not player.is_dead:
			_start_attack(player)

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
	attack_timer = 2.2
	
	match attack_state:
		0:
			_attack_magma_barrage(player)
		1:
			_attack_magma_eruption(player)
		2:
			_attack_lava_leap(player)

func _attack_magma_barrage(player: Node2D) -> void:
	anim.play("attack")
	SoundManager.play_sfx("fireball", 0.1)
	
	var base_dir = (player.global_position - global_position).normalized()
	for i in range(4):
		var orb = SCENE_MAGMA_ORB.instantiate()
		orb.global_position = global_position + Vector2(facing * 24.0, -14.0)
		var angle_offset = (i - 1.5) * 0.22
		orb.direction = base_dir.rotated(angle_offset)
		get_parent().add_child(orb)
		
	await get_tree().create_timer(0.45).timeout
	if not is_dead and not is_frozen:
		anim.play("idle")
	is_attacking = false

func _attack_magma_eruption(player: Node2D) -> void:
	anim.play("attack")
	SoundManager.play_sfx("explosion")
	GameManager.hit_stop(0.04)
	
	# Slams the ground and shoots fiery projectiles high into the air
	for i in range(3):
		var orb = SCENE_MAGMA_ORB.instantiate()
		orb.global_position = global_position + Vector2((i - 1) * 30.0, -20.0)
		orb.direction = Vector2((i - 1) * 0.4, -1.0).normalized()
		get_parent().add_child(orb)
		
	if player and not player.is_dead and global_position.distance_to(player.global_position) < 130.0:
		player.take_damage(damage, global_position)
		
	await get_tree().create_timer(0.5).timeout
	if not is_dead and not is_frozen:
		anim.play("idle")
	is_attacking = false

func _attack_lava_leap(player: Node2D) -> void:
	SoundManager.play_sfx("boss_roar")
	# Leaps toward player
	velocity.y = -350.0
	velocity.x = facing * speed * 2.5
	
	await get_tree().create_timer(0.7).timeout
	SoundManager.play_sfx("explosion")
	if player and not player.is_dead and global_position.distance_to(player.global_position) < 80.0:
		player.take_damage(damage, global_position)
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
