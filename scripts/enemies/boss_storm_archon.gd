extends EnemyBase

@export var boss_name: String = "STORM THUNDER ARCHON"
var is_active: bool = false
var is_casting: bool = false
var phase: int = 1
var teleport_timer: float = 3.0
var cast_timer: float = 1.0
var lightning_timer: float = 3.5

var teleport_anchors: Array[Vector2] = []
var current_anchor_idx: int = 0

const SCENE_THUNDER_ORB = preload("res://scenes/enemies/thunder_orb_projectile.tscn")
const SCENE_LIGHTNING = preload("res://scenes/abilities/lightning_strike.tscn")

signal boss_died()

func _ready() -> void:
	max_hp = 1200.0
	damage = 34.0
	speed = 0.0
	crystals_dropped = 25
	super._ready()
	anim.play("idle")
	modulate = Color(1.3, 1.3, 0.5) # Electric thunder gold

func activate_boss(anchors: Array[Vector2] = []) -> void:
	if is_active:
		return
	is_active = true
	if not anchors.is_empty():
		teleport_anchors = anchors
	else:
		teleport_anchors = [
			global_position,
			global_position + Vector2(-220, -50),
			global_position + Vector2(220, -50),
			global_position + Vector2(0, -90)
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

	if hp < max_hp * 0.5 and phase == 1:
		phase = 2
		SoundManager.play_sfx("boss_roar")
		GameManager.post_notification("Storm Archon summons the Tempest! Sky lightning intensifies!")

	teleport_timer -= delta
	cast_timer -= delta
	lightning_timer -= delta

	if cast_timer <= 0.0 and not is_casting:
		_cast_thunder_burst(player)
		cast_timer = 1.6 if phase == 1 else 1.0

	if teleport_timer <= 0.0 and not is_casting:
		_teleport()
		teleport_timer = 3.2 if phase == 1 else 2.1

	if lightning_timer <= 0.0:
		_cast_sky_lightning(player)
		lightning_timer = 3.5 if phase == 1 else 2.0

func _cast_thunder_burst(player: Node2D) -> void:
	if not player or player.is_dead or is_dead or is_frozen:
		return

	is_casting = true
	anim.play("cast")
	SoundManager.play_sfx("lightning", 0.1)
	
	var orb_count = 3 if phase == 1 else 5
	var base_dir = (player.global_position - global_position).normalized()
	
	for i in range(orb_count):
		var orb = SCENE_THUNDER_ORB.instantiate()
		orb.global_position = global_position + Vector2(0, -14)
		var angle_offset = (i - (orb_count - 1) / 2.0) * 0.22
		orb.direction = base_dir.rotated(angle_offset)
		get_parent().add_child(orb)
		
	await get_tree().create_timer(0.35).timeout
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

func _cast_sky_lightning(player: Node2D) -> void:
	if not player or player.is_dead or is_dead:
		return
	SoundManager.play_sfx("lightning")
	var ls = SCENE_LIGHTNING.instantiate()
	ls.global_position = player.global_position + Vector2(0, 16)
	get_parent().add_child(ls)

func take_damage(amount: float, type: String = "magic") -> void:
	super.take_damage(amount, type)
	GameManager.boss_health_changed.emit(hp, max_hp)

func die() -> void:
	is_active = false
	GameManager.boss_defeated.emit()
	boss_died.emit()
	super.die()
