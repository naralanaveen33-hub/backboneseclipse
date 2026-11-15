extends EnemyBase
class_name BossUltimateOverlord

## ==============================================================================
## PRIMORDIAL VOID EMPEROR MALAKOR - ULTIMATE BOSS (GODOT 4 2D ACTION GAME)
## CharacterBody2D Boss System with 50,000 HP, 4 Formidable Phases, and 8 Core Ability Trees.
## ==============================================================================

# ------------------------------------------------------------------------------
# 1. EXPORTED PROPERTIES & BOSS IDENTITY
# ------------------------------------------------------------------------------
@export var boss_name: String = "PRIMORDIAL VOID EMPEROR MALAKOR"
@export var arena_bounds_min_x: float = 80.0
@export var arena_bounds_max_x: float = 1200.0
@export var ground_y: float = 460.0

# ------------------------------------------------------------------------------
# 2. STATE MACHINE & PHASE SYSTEM
# ------------------------------------------------------------------------------
enum BossState {
	IDLE,
	CHASE,
	DASHING,
	CASTING,
	BEAMING,
	TELEPORTING,
	GROUND_SLAM,
	REGENERATING,
	STUNNED,
	DEATH
}

var current_state: BossState = BossState.IDLE
var is_active: bool = false
var phase: int = 1

# Phase thresholds (10,000 Max HP)
const PHASE_2_HP: float = 7500.0 # 75%
const PHASE_3_HP: float = 5000.0 # 50%
const PHASE_4_HP: float = 2500.0 # 25%

# ------------------------------------------------------------------------------
# 3. MOVEMENT & STAT ATTRIBUTES
# ------------------------------------------------------------------------------
var base_move_speed: float = 220.0
var current_speed: float = 220.0
var dash_speed: float = 850.0
var acceleration: float = 2800.0
var gravity: float = 980.0

var facing_direction: float = -1.0
var is_dashing: bool = false
var dash_target_dir: Vector2 = Vector2.ZERO
var dash_timer: float = 0.0

# Motion trail emission interval
var trail_timer: float = 0.0
const TRAIL_INTERVAL: float = 0.045

# ------------------------------------------------------------------------------
# 4. ABILITY COOLDOWNS & TIMERS
# ------------------------------------------------------------------------------
var cd_teleport: float = 3.5
var cd_dash: float = 4.0
var cd_dark_orbs: float = 2.0
var cd_electric_shockwave: float = 5.0
var cd_void_explosion: float = 6.0
var cd_energy_beam: float = 7.5
var cd_shield: float = 14.0
var cd_minion_summon: float = 12.0
var cd_ground_slam: float = 6.5
var cd_regen: float = 22.0

var ai_decision_timer: float = 0.5
var active_shield_instance: Area2D = null

# ------------------------------------------------------------------------------
# 5. PRELOADED ABILITY & ENEMY SCENES
# ------------------------------------------------------------------------------
const SCENE_DARK_ORB = preload("res://scenes/enemies/dark_energy_orb.tscn")
const SCENE_ENERGY_WAVE = preload("res://scenes/enemies/energy_wave.tscn")
const SCENE_SHOCKWAVE = preload("res://scenes/enemies/electric_shockwave.tscn")
const SCENE_VOID_EXPLOSION = preload("res://scenes/enemies/void_explosion.tscn")
const SCENE_ENERGY_BEAM = preload("res://scenes/enemies/dark_energy_beam.tscn")
const SCENE_SHIELD = preload("res://scenes/enemies/boss_shield.tscn")
const SCENE_BAT = preload("res://scenes/enemies/flying_bat.tscn")
const SCENE_SHADOW = preload("res://scenes/enemies/shadow_monster.tscn")
const SCENE_DEMON = preload("res://scenes/enemies/fire_demon.tscn")
const SCENE_HEALTH_BAR_UI = preload("res://scenes/ui/boss_health_bar.tscn")

# ------------------------------------------------------------------------------
# 6. ONREADY NODE REFERENCES
# ------------------------------------------------------------------------------
@onready var cast_point: Marker2D = $CastPoint
@onready var beam_point: Marker2D = $BeamPoint
@onready var hitbox: Area2D = $Hitbox
@onready var aura_particles: CPUParticles2D = $AuraParticles
@onready var rage_particles: CPUParticles2D = $RageParticles

var boss_ui: BossHealthBarUI = null

# ------------------------------------------------------------------------------
# 7. INITIALIZATION & SETUP
# ------------------------------------------------------------------------------
func _ready() -> void:
	max_hp = 10000.0
	hp = 10000.0
	damage = 35.0
	speed = base_move_speed
	crystals_dropped = 200
	
	super._ready()
	add_to_group("enemies")
	add_to_group("bosses")
	
	_setup_boss_ui()
	_update_phase_appearance(1)
	anim.play("idle")

func _setup_boss_ui() -> void:
	boss_ui = SCENE_HEALTH_BAR_UI.instantiate() as BossHealthBarUI
	add_child(boss_ui)
	boss_ui.setup(boss_name, max_hp)

func activate_boss() -> void:
	if is_active:
		return
	is_active = true
	current_state = BossState.CHASE
	
	SoundManager.play_sfx("boss_roar")
	SoundManager.play_music("dark_dream")
	GameManager.boss_spawned.emit(boss_name, max_hp)
	GameManager.post_notification("⚡ THE PRIMORDIAL VOID EMPEROR HAS AWAKENED! 10,000 HP ⚡")

# ------------------------------------------------------------------------------
# 8. MAIN PHYSICS PROCESS & INTELLIGENT AI LOOP
# ------------------------------------------------------------------------------
func _physics_process(delta: float) -> void:
	var player = get_tree().get_first_node_in_group("player") as CharacterBody2D
	
	# Auto-activation check when player approaches arena
	if not is_active and player and not player.is_dead:
		if global_position.distance_to(player.global_position) < 550.0:
			activate_boss()
			
	if not is_active or is_dead or is_frozen:
		return

	# Handle cooldown timers
	_update_cooldowns(delta)
	
	# Handle motion trail generator
	_handle_motion_trail(delta)

	# State execution
	match current_state:
		BossState.CHASE:
			_process_chase_state(player, delta)
		BossState.DASHING:
			_process_dash_state(delta)
		BossState.GROUND_SLAM:
			_process_ground_slam_state(delta)
		BossState.IDLE:
			velocity.x = move_toward(velocity.x, 0.0, acceleration * delta)
			if not is_on_floor():
				velocity.y += gravity * delta
			move_and_slide()

	# Face towards player when not locked in dash/beam
	if player and not player.is_dead and current_state != BossState.DASHING and current_state != BossState.BEAMING:
		var dir = signf(player.global_position.x - global_position.x)
		if dir != 0.0:
			facing_direction = dir
			anim.flip_h = (facing_direction < 0)
			cast_point.position.x = 24.0 * facing_direction
			beam_point.position.x = 30.0 * facing_direction

	# AI Decision Evaluation Loop
	ai_decision_timer -= delta
	if ai_decision_timer <= 0.0 and current_state == BossState.CHASE:
		_evaluate_ai_decisions(player)
		ai_decision_timer = 0.35 if phase < 3 else (0.22 if phase == 3 else 0.14)

# ------------------------------------------------------------------------------
# 9. ABILITY COOLDOWNS & PROGRESSION
# ------------------------------------------------------------------------------
func _update_cooldowns(delta: float) -> void:
	if cd_teleport > 0.0: cd_teleport -= delta
	if cd_dash > 0.0: cd_dash -= delta
	if cd_dark_orbs > 0.0: cd_dark_orbs -= delta
	if cd_electric_shockwave > 0.0: cd_electric_shockwave -= delta
	if cd_void_explosion > 0.0: cd_void_explosion -= delta
	if cd_energy_beam > 0.0: cd_energy_beam -= delta
	if cd_shield > 0.0: cd_shield -= delta
	if cd_minion_summon > 0.0: cd_minion_summon -= delta
	if cd_ground_slam > 0.0: cd_ground_slam -= delta
	if cd_regen > 0.0: cd_regen -= delta

func _handle_motion_trail(delta: float) -> void:
	# Motion trail generated during high-speed run or dash
	if current_state == BossState.DASHING or (current_state == BossState.CHASE and abs(velocity.x) > 280.0):
		trail_timer -= delta
		if trail_timer <= 0.0:
			trail_timer = TRAIL_INTERVAL
			var ghost_tint = Color(0.7, 0.2, 0.9, 0.55)
			if phase == 2:
				ghost_tint = Color(1.0, 0.2, 0.3, 0.6)
			elif phase == 3:
				ghost_tint = Color(0.2, 0.8, 1.0, 0.65)
			elif phase == 4:
				ghost_tint = Color(1.5, 0.9, 0.2, 0.75)
			BossGhostTrail.spawn_ghost(self, anim, ghost_tint, 0.22)

# ------------------------------------------------------------------------------
# 10. AI DECISION-MAKING ENGINE
# ------------------------------------------------------------------------------
func _evaluate_ai_decisions(player: CharacterBody2D) -> void:
	if not player or player.is_dead or is_dead or current_state != BossState.CHASE:
		return

	var dist = global_position.distance_to(player.global_position)
	var hp_ratio = hp / max_hp

	# Priority 1: Emergency Shield when health drops in Phase 3 or 4
	if phase >= 3 and cd_shield <= 0.0 and active_shield_instance == null:
		create_protective_shield()
		return

	# Priority 2: Health Regeneration channeling if damaged below 45% HP in Phase 3+
	if phase >= 3 and hp < max_hp * 0.45 and cd_regen <= 0.0:
		regenerate_health()
		return

	# Priority 3: Ultimate Rage Beam in Phase 4 or Full Beam in Phase 3
	if (phase == 4 and cd_energy_beam <= 0.0) or (phase == 3 and dist > 320.0 and cd_energy_beam <= 0.0):
		launch_energy_beam(player)
		return

	# Priority 4: Teleport behind player for ambush combo
	if phase >= 3 and cd_teleport <= 0.0 and (dist > 400.0 or randf() < 0.35):
		teleport_behind_player(player)
		return

	# Priority 5: High-speed Dash Attack (Close to mid range)
	if phase >= 2 and cd_dash <= 0.0 and dist > 140.0 and dist < 520.0:
		perform_dash_attack(player)
		return

	# Priority 6: Electric Shockwave Stun Attack (When player gets close)
	if phase >= 2 and cd_electric_shockwave <= 0.0 and dist < 220.0:
		cast_electric_shockwave()
		return

	# Priority 7: Ground Slam + Dangerous Energy Waves
	if cd_ground_slam <= 0.0 and (dist < 260.0 or randf() < 0.28):
		perform_ground_slam(player)
		return

	# Priority 8: Massive Void Explosion
	if phase >= 2 and cd_void_explosion <= 0.0:
		create_massive_explosion(player.global_position)
		return

	# Priority 9: Minion Summoning
	if cd_minion_summon <= 0.0 and phase >= 2:
		summon_minions()
		return

	# Priority 10: Dark Energy Orb Barrage (Ranged harassment)
	if cd_dark_orbs <= 0.0:
		shoot_dark_energy_balls(player)

# ------------------------------------------------------------------------------
# 11. ABILITY 1: TELEPORTATION
# ------------------------------------------------------------------------------
func teleport_behind_player(player: CharacterBody2D) -> void:
	if not player or is_dead:
		return
		
	current_state = BossState.TELEPORTING
	velocity = Vector2.ZERO
	anim.play("teleporting")
	SoundManager.play_sfx("freeze")
	spawn_teleport_effect(global_position)
	
	await anim.animation_finished
	if is_dead: return
	
	# Destination: Behind the player clamped inside the arena bounds
	var p_facing = 1.0
	if "facing" in player:
		p_facing = player.facing
	var dest_x = clampf(player.global_position.x - (p_facing * 55.0), arena_bounds_min_x, arena_bounds_max_x)
	var dest_y = player.global_position.y - 12.0
	
	global_position = Vector2(dest_x, dest_y)
	spawn_teleport_effect(global_position)
	SoundManager.play_sfx("freeze")
	
	anim.play_backwards("teleporting")
	await anim.animation_finished
	
	cd_teleport = 3.2 if phase == 1 else (2.4 if phase == 2 else (1.6 if phase == 3 else 1.0))
	current_state = BossState.CHASE
	anim.play("idle")
	
	# Immediate follow-up combo in Phase 3 and 4!
	if phase >= 3 and randf() < 0.65:
		perform_dash_attack(player)

func teleport_randomly() -> void:
	if is_dead: return
	current_state = BossState.TELEPORTING
	velocity = Vector2.ZERO
	anim.play("teleporting")
	SoundManager.play_sfx("freeze")
	spawn_teleport_effect(global_position)
	
	await anim.animation_finished
	if is_dead: return
	
	var rx = randf_range(arena_bounds_min_x + 60.0, arena_bounds_max_x - 60.0)
	var ry = ground_y - 20.0
	global_position = Vector2(rx, ry)
	spawn_teleport_effect(global_position)
	SoundManager.play_sfx("freeze")
	
	anim.play_backwards("teleporting")
	await anim.animation_finished
	
	cd_teleport = 2.5 if phase <= 2 else 1.2
	current_state = BossState.CHASE
	anim.play("idle")

func spawn_teleport_effect(pos: Vector2) -> void:
	var effect = Sprite2D.new()
	var tex = load("res://assets/effects/projectiles/teleport_vortex.png")
	if tex:
		effect.texture = tex
	effect.global_position = pos
	effect.top_level = true
	effect.scale = Vector2(0.3, 0.3)
	get_parent().add_child(effect)
	
	var tween = effect.create_tween()
	tween.tween_property(effect, "scale", Vector2(1.5, 1.5), 0.28)
	tween.parallel().tween_property(effect, "modulate:a", 0.0, 0.28)
	tween.tween_callback(effect.queue_free)

# ------------------------------------------------------------------------------
# 12. ABILITY 2: SUPER SPEED & DASH ATTACK
# ------------------------------------------------------------------------------
func _process_chase_state(player: CharacterBody2D, delta: float) -> void:
	if not is_on_floor():
		velocity.y += gravity * delta
	else:
		velocity.y = 0.0

	if player and not player.is_dead:
		var target_x = player.global_position.x
		var dist_x = target_x - global_position.x
		
		# Agility: Quick direction changing with high acceleration
		var target_vx = signf(dist_x) * current_speed
		velocity.x = move_toward(velocity.x, target_vx, acceleration * delta)
		
		if abs(velocity.x) > 20.0:
			anim.play("running")
		else:
			anim.play("idle")
	else:
		velocity.x = move_toward(velocity.x, 0.0, acceleration * delta)
		anim.play("idle")
		
	move_and_slide()

func perform_dash_attack(player: CharacterBody2D) -> void:
	if not player or is_dead:
		return
		
	current_state = BossState.DASHING
	is_dashing = true
	dash_timer = 0.45
	
	# Telegraph flare: pause and charge
	velocity = Vector2.ZERO
	anim.play("dashing")
	SoundManager.play_sfx("jump", 0.8)
	
	var charge_dir = signf(player.global_position.x - global_position.x)
	if charge_dir == 0.0: charge_dir = facing_direction
	facing_direction = charge_dir
	anim.flip_h = (facing_direction < 0)
	
	dash_target_dir = Vector2(facing_direction, 0.0).normalized()
	
	# Warning flash
	var orig_color = anim.modulate
	anim.modulate = Color(2.5, 0.5, 0.8)
	await get_tree().create_timer(0.28).timeout
	if is_dead: return
	anim.modulate = orig_color
	
	# Supersonic surge forward!
	SoundManager.play_sfx("fireball", 0.05)
	velocity = dash_target_dir * (dash_speed * (1.0 + float(phase - 1) * 0.15))
	cd_dash = 4.2 if phase == 2 else (3.0 if phase == 3 else 1.8)

func _process_dash_state(delta: float) -> void:
	dash_timer -= delta
	move_and_slide()
	
	if dash_timer <= 0.0 or is_on_wall():
		is_dashing = false
		current_state = BossState.CHASE
		anim.play("idle")

# ------------------------------------------------------------------------------
# 13. ABILITY 3: STUN ATTACK & ELECTRIC SHOCKWAVE
# ------------------------------------------------------------------------------
func cast_electric_shockwave() -> void:
	if is_dead: return
	current_state = BossState.CASTING
	velocity = Vector2.ZERO
	anim.play("attacking")
	SoundManager.play_sfx("lightning")
	
	await get_tree().create_timer(0.20).timeout
	if is_dead: return
	
	var shock = SCENE_SHOCKWAVE.instantiate()
	shock.global_position = global_position + Vector2(0, 10)
	shock.damage = 25.0 * (1.0 + float(phase - 1) * 0.25)
	shock.stun_duration = 1.6 + float(phase) * 0.2
	get_parent().add_child(shock)
	
	await get_tree().create_timer(0.25).timeout
	if not is_dead:
		anim.play("idle")
		current_state = BossState.CHASE
	cd_electric_shockwave = 5.5 if phase == 2 else (4.0 if phase == 3 else 2.5)

# ------------------------------------------------------------------------------
# 14. ABILITY 4: DARK ENERGY ATTACKS (BALLS, EXPLOSION, BEAM)
# ------------------------------------------------------------------------------
func shoot_dark_energy_balls(player: CharacterBody2D) -> void:
	if not player or is_dead: return
	current_state = BossState.CASTING
	velocity = Vector2.ZERO
	anim.play("attacking")
	SoundManager.play_sfx("fireball", 0.08)
	
	# Ball counts scale across phases: 5 -> 8 -> 10 -> 14
	var orb_count = 5 if phase == 1 else (8 if phase == 2 else (10 if phase == 3 else 14))
	var base_dir = (player.global_position - cast_point.global_position).normalized()
	var spread_angle = 0.22 if phase < 4 else 0.35
	
	for i in range(orb_count):
		var orb = SCENE_DARK_ORB.instantiate()
		orb.global_position = cast_point.global_position
		var angle_offset = (i - (orb_count - 1) / 2.0) * spread_angle
		orb.direction = base_dir.rotated(angle_offset)
		orb.speed = 380.0 + (phase * 35.0)
		orb.damage = 22.0 * (1.0 + float(phase - 1) * 0.3)
		orb.homing_strength = 0.35 if phase >= 3 else 0.0
		get_parent().add_child(orb)
		
	await get_tree().create_timer(0.32).timeout
	if not is_dead:
		anim.play("idle")
		current_state = BossState.CHASE
	cd_dark_orbs = 2.2 if phase == 1 else (1.6 if phase == 2 else (1.1 if phase == 3 else 0.75))

func create_massive_explosion(target_pos: Vector2) -> void:
	if is_dead: return
	SoundManager.play_sfx("boss_roar", 0.2)
	
	var exp_inst = SCENE_VOID_EXPLOSION.instantiate()
	exp_inst.global_position = target_pos
	exp_inst.damage = 45.0 * (1.0 + float(phase - 1) * 0.25)
	get_parent().add_child(exp_inst)
	
	# In Phase 4, trigger 3 explosions in rapid succession!
	if phase == 4:
		for offset_x in [-140.0, 140.0]:
			var extra = SCENE_VOID_EXPLOSION.instantiate()
			extra.global_position = target_pos + Vector2(offset_x, 0)
			extra.telegraph_duration = 0.75
			get_parent().add_child(extra)
			
	cd_void_explosion = 6.5 if phase == 2 else (4.8 if phase == 3 else 3.2)

func launch_energy_beam(player: CharacterBody2D) -> void:
	if not player or is_dead: return
	current_state = BossState.BEAMING
	velocity = Vector2.ZERO
	anim.play("ultimate_attack")
	
	var beam = SCENE_ENERGY_BEAM.instantiate()
	beam.setup(beam_point.global_position, facing_direction)
	beam.damage_per_sec = 60.0 * (1.0 + float(phase - 1) * 0.3)
	get_parent().add_child(beam)
	
	await get_tree().create_timer(1.25).timeout
	if not is_dead:
		anim.play("idle")
		current_state = BossState.CHASE
	cd_energy_beam = 8.0 if phase == 3 else 4.5

# ------------------------------------------------------------------------------
# 15. ABILITY 5: SPECIAL ABILITIES (SUMMON, SHIELD, REGEN, SLAM, WAVES)
# ------------------------------------------------------------------------------
func summon_minions() -> void:
	if is_dead: return
	SoundManager.play_sfx("boss_roar")
	GameManager.pop_floating_text("MINIONS AWAKEN!", global_position + Vector2(0, -50), Color(0.8, 0.3, 1.0))
	
	# Spawn 2 bats and 1 shadow monster or demon
	for i in range(2):
		var bat = SCENE_BAT.instantiate()
		bat.global_position = global_position + Vector2(randf_range(-140, 140), randf_range(-120, -50))
		get_parent().add_child(bat)
		
	var monster = SCENE_DEMON.instantiate() if phase >= 3 else SCENE_SHADOW.instantiate()
	monster.global_position = global_position + Vector2(randf_range(-120, 120), 0)
	get_parent().add_child(monster)
	
	cd_minion_summon = 14.0 if phase == 2 else 9.0

func create_protective_shield() -> void:
	if is_dead or active_shield_instance != null: return
	
	var sh = SCENE_SHIELD.instantiate()
	sh.global_position = global_position
	active_shield_instance = sh
	add_child(sh)
	
	sh.shield_broken.connect(func():
		active_shield_instance = null
		cd_shield = 12.0
	)
	GameManager.pop_floating_text("PROTECTIVE SHIELD!", global_position + Vector2(0, -50), Color(0.3, 0.8, 1.0))

func regenerate_health() -> void:
	if is_dead: return
	current_state = BossState.REGENERATING
	velocity = Vector2.ZERO
	anim.play("ultimate_attack")
	SoundManager.play_sfx("freeze")
	GameManager.pop_floating_text("DARK REGENERATION!", global_position + Vector2(0, -55), Color(0.3, 1.0, 0.4))
	
	# Heal 350 HP x 3 ticks = 1,050 HP
	for i in range(3):
		await get_tree().create_timer(0.8).timeout
		if is_dead or current_state != BossState.REGENERATING: break
		var heal_amount = 350.0
		hp = minf(max_hp, hp + heal_amount)
		boss_ui.update_hp(hp, max_hp)
		GameManager.boss_health_changed.emit(hp, max_hp)
		GameManager.pop_floating_text("+%d HP" % int(heal_amount), global_position + Vector2(0, -40), Color(0.2, 1.0, 0.4))
		SoundManager.play_sfx("crystal")
		
	if not is_dead:
		anim.play("idle")
		current_state = BossState.CHASE
	cd_regen = 24.0

func perform_ground_slam(player: CharacterBody2D) -> void:
	if not player or is_dead: return
	current_state = BossState.GROUND_SLAM
	velocity = Vector2.ZERO
	anim.play("ultimate_attack")
	
	# Leap or hover high into the air
	var target_x = player.global_position.x
	global_position.y -= 140.0
	global_position.x = clampf(target_x, arena_bounds_min_x + 50, arena_bounds_max_x - 50)
	
	await get_tree().create_timer(0.38).timeout
	if is_dead: return
	
	# Plunge down violently
	velocity.y = 1250.0
	SoundManager.play_sfx("jump", 1.4)
	cd_ground_slam = 7.0 if phase == 1 else (5.0 if phase == 2 else 3.5)

func _process_ground_slam_state(delta: float) -> void:
	velocity.y += gravity * 2.0 * delta
	move_and_slide()
	
	if is_on_floor():
		_on_slam_impact()

func _on_slam_impact() -> void:
	SoundManager.play_sfx("explosion")
	GameManager.hit_stop(0.06)
	create_energy_waves()
	
	# Deal heavy contact damage to nearby player
	var p = get_tree().get_first_node_in_group("player")
	if p and not p.is_dead and global_position.distance_to(p.global_position) < 80.0:
		p.take_damage(40.0, global_position)
		
	anim.play("idle")
	current_state = BossState.CHASE

func create_energy_waves() -> void:
	# Wave surging left
	var wave_left = SCENE_ENERGY_WAVE.instantiate()
	wave_left.global_position = global_position + Vector2(-30, 24)
	wave_left.direction_x = -1.0
	wave_left.damage = 28.0 * (1.0 + float(phase - 1) * 0.25)
	get_parent().add_child(wave_left)
	
	# Wave surging right
	var wave_right = SCENE_ENERGY_WAVE.instantiate()
	wave_right.global_position = global_position + Vector2(30, 24)
	wave_right.direction_x = 1.0
	wave_right.damage = 28.0 * (1.0 + float(phase - 1) * 0.25)
	get_parent().add_child(wave_right)

# ------------------------------------------------------------------------------
# 16. DAMAGE RECEPTION & PHASE TRANSITIONS
# ------------------------------------------------------------------------------
func take_damage(amount: float, type: String = "magic") -> void:
	# If protective shield is active, the shield absorbs it!
	if active_shield_instance and is_instance_valid(active_shield_instance):
		active_shield_instance.take_damage(amount, type)
		return
		
	super.take_damage(amount, type)
	
	if boss_ui:
		boss_ui.update_hp(hp, max_hp)
	GameManager.boss_health_changed.emit(hp, max_hp)
	
	# Dynamic Phase Transitions
	if hp <= PHASE_4_HP and phase < 4:
		_transition_to_phase(4)
	elif hp <= PHASE_3_HP and phase < 3:
		_transition_to_phase(3)
	elif hp <= PHASE_2_HP and phase < 2:
		_transition_to_phase(2)

func _transition_to_phase(new_phase: int) -> void:
	phase = new_phase
	SoundManager.play_sfx("boss_roar")
	GameManager.hit_stop(0.12)
	
	_update_phase_appearance(phase)
	if boss_ui:
		boss_ui.set_phase(phase)
		
	match phase:
		2:
			current_speed = base_move_speed * 1.45 # 320 px/s
			damage = 45.0
			GameManager.post_notification("🔥 PHASE 2: SUPER SPEED & VOID SURGE ACTIVATED! 🔥")
			summon_minions()
		3:
			current_speed = base_move_speed * 1.90 # 420 px/s
			damage = 56.0
			GameManager.post_notification("🌀 PHASE 3: ASTRAL COMBOS & TELEPORT AMBUSH! 🌀")
			create_protective_shield()
		4:
			current_speed = base_move_speed * 2.50 # 550 px/s (Ultimate Speed!)
			damage = 70.0
			rage_particles.emitting = true
			GameManager.post_notification("⚡ PHASE 4: ULTIMATE APOCALYPTIC RAGE MODE! ⚡")
			create_massive_explosion(global_position)

func _update_phase_appearance(p: int) -> void:
	match p:
		1:
			anim.modulate = Color(0.9, 0.75, 1.15)
			scale = Vector2(1.1, 1.1)
			aura_particles.color = Color(0.65, 0.2, 0.9, 0.7)
		2:
			anim.modulate = Color(1.3, 0.45, 0.55) # Crimson Void Surge
			scale = Vector2(1.2, 1.2)
			aura_particles.color = Color(1.0, 0.15, 0.35, 0.8)
		3:
			anim.modulate = Color(0.6, 1.2, 1.6) # Astral Electric Cyan
			scale = Vector2(1.3, 1.3)
			aura_particles.color = Color(0.2, 0.85, 1.0, 0.85)
		4:
			anim.modulate = Color(1.6, 1.3, 0.4) # Solar Overdrive Blazing Gold
			scale = Vector2(1.45, 1.45)
			aura_particles.color = Color(1.5, 0.8, 0.15, 1.0)

# ------------------------------------------------------------------------------
# 17. CONTACT DAMAGE HITBOX & DEATH
# ------------------------------------------------------------------------------
func _on_hitbox_body_entered(body: Node2D) -> void:
	if not is_active or is_dead: return
	if body.is_in_group("player") and body.has_method("take_damage"):
		var contact_dmg = damage * (1.3 if is_dashing else 1.0)
		body.take_damage(contact_dmg, global_position)
		if is_dashing and body.has_method("stun"):
			body.stun(1.2)

func die() -> void:
	if is_dead: return
	is_active = false
	current_state = BossState.DEATH
	velocity = Vector2.ZERO
	
	if active_shield_instance and is_instance_valid(active_shield_instance):
		active_shield_instance.queue_free()
		
	if boss_ui:
		boss_ui.hide_bar()
		
	GameManager.boss_defeated.emit()
	GameManager.post_notification("👑 THE ULTIMATE BOSS HAS FALLEN! SUPREME GLORY! 👑")
	SoundManager.play_sfx("victory")
	
	anim.play("death")
	super.die()
