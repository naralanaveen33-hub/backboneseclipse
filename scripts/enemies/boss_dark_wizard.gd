extends EnemyBase

@export var boss_name: String = "DARK WIZARD - LORD OF SHADOWS"
var is_active: bool = false
var is_casting: bool = false
var phase: int = 1
var teleport_timer: float = 3.2
var cast_timer: float = 1.2

# Anchors in boss arena
var teleport_anchors: Array[Vector2] = []
var current_anchor_idx: int = 0

const SCENE_DARK_ORB = preload("res://scenes/enemies/dark_orb_projectile.tscn")
const SCENE_BAT = preload("res://scenes/enemies/flying_bat.tscn")

signal boss_died()

func _ready() -> void:
	max_hp = 750.0
	damage = 30.0
	speed = 0.0
	crystals_dropped = 15
	super._ready()
	anim.play("idle")

func activate_boss(anchors: Array[Vector2] = []) -> void:
	if is_active:
		return
	is_active = true
	if not anchors.is_empty():
		teleport_anchors = anchors
	else:
		teleport_anchors = [
			global_position,
			global_position + Vector2(-180, -50),
			global_position + Vector2(180, -50),
			global_position + Vector2(0, -70)
		]
	SoundManager.play_sfx("boss_roar")
	SoundManager.play_music("dark_dream")
	GameManager.boss_spawned.emit(boss_name, max_hp)

func _physics_process(delta: float) -> void:
	var player = get_tree().get_first_node_in_group("player")
	
	if not is_active and player and not player.is_dead:
		if global_position.distance_to(player.global_position) < 450.0:
			activate_boss(teleport_anchors)

	if not is_active or is_dead or is_frozen:
		return

	if player and not player.is_dead:
		var dir_to_p = signf(player.global_position.x - global_position.x)
		anim.flip_h = (dir_to_p < 0)

	# Check Phase
	if hp < max_hp * 0.5 and phase == 1:
		phase = 2
		SoundManager.play_sfx("boss_roar")
		GameManager.post_notification("Dark Wizard enrages! Shadows surge!")
		_spawn_minion()

	teleport_timer -= delta
	cast_timer -= delta

	if cast_timer <= 0.0 and not is_casting:
		_cast_attack(player)
		cast_timer = 1.8 if phase == 1 else 1.2

	if teleport_timer <= 0.0 and not is_casting:
		_teleport()
		teleport_timer = 3.6 if phase == 1 else 2.5

func _cast_attack(player: Node2D) -> void:
	if not player or player.is_dead or is_dead or is_frozen:
		return

	is_casting = true
	anim.play("cast")
	SoundManager.play_sfx("fireball", 0.15)
	
	var orb_count = 3 if phase == 1 else 5
	var base_dir = (player.global_position - global_position).normalized()
	
	for i in range(orb_count):
		var orb = SCENE_DARK_ORB.instantiate()
		orb.global_position = global_position + Vector2(0, -12)
		var angle_offset = (i - (orb_count - 1) / 2.0) * 0.25
		orb.direction = base_dir.rotated(angle_offset)
		get_parent().add_child(orb)
		
	await get_tree().create_timer(0.4).timeout
	if not is_dead and not is_frozen:
		anim.play("idle")
	is_casting = false

func _teleport() -> void:
	if teleport_anchors.is_empty() or is_dead or is_frozen:
		return
	
	is_casting = true
	anim.play("teleport")
	SoundManager.play_sfx("freeze")
	
	await anim.animation_finished
	var next_idx = randi() % teleport_anchors.size()
	if next_idx == current_anchor_idx and teleport_anchors.size() > 1:
		next_idx = (next_idx + 1) % teleport_anchors.size()
	current_anchor_idx = next_idx
	
	global_position = teleport_anchors[current_anchor_idx]
	
	anim.play_backwards("teleport")
	await anim.animation_finished
	anim.play("idle")
	is_casting = false
	
	if phase == 2 and randf() < 0.4:
		_spawn_minion()

func _spawn_minion() -> void:
	var bat = SCENE_BAT.instantiate()
	bat.global_position = global_position + Vector2(randf_range(-60, 60), -40)
	get_parent().add_child(bat)

func take_damage(amount: float, type: String = "magic") -> void:
	super.take_damage(amount, type)
	GameManager.boss_health_changed.emit(hp, max_hp)

func die() -> void:
	is_active = false
	GameManager.boss_defeated.emit()
	boss_died.emit()
	super.die()
