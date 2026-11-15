extends Node3D

@onready var world_env: WorldEnvironment = $WorldEnvironment
@onready var dir_light: DirectionalLight3D = $DirectionalLight3D
@onready var overhead_spot: SpotLight3D = $OverheadSpotlight
@onready var omni_pulsing: OmniLight3D = $OmniLightPulsing
@onready var omni_gold: OmniLight3D = $OmniLightGold

@onready var camera: Camera3D = $Camera3D
@onready var core_node: Node3D = $CentralCore
@onready var ring1: MeshInstance3D = $CentralCore/Ring1
@onready var ring2: MeshInstance3D = $CentralCore/Ring2
@onready var crystal_orbit: Node3D = $CentralCore/CrystalOrbit

@onready var stage: Node3D = $Stage
@onready var player_anim: AnimatedSprite3D = $Stage/PlayerSprite
@onready var wand_light: OmniLight3D = $Stage/WandLight
@onready var projectile_container: Node3D = $Projectiles

@onready var title_label: Label3D = $Labels/TitleLabel3D
@onready var dev_header_label: Label3D = $Labels/DeveloperHeaderLabel3D
@onready var dev_name_label: Label3D = $Labels/DeveloperNameLabel3D
@onready var credit_label: Label3D = $Labels/CreditLabel3D
@onready var subtitle_label: Label3D = $Labels/SubtitleLabel3D
@onready var feature_label: Label3D = $Labels/FeatureLabel3D
@onready var prompt_label: Label3D = $Labels/PromptLabel3D

@onready var fade_rect: ColorRect = $Overlay/FadeRect

var is_transitioning: bool = false
var elapsed_time: float = 0.0
var total_duration: float = 30.0

var active_projectiles = []

func _ready() -> void:
	SoundManager.play_music("dark_dream")
	
	# Start in mysterious dark atmosphere: only wand orb is lit!
	if world_env and world_env.environment:
		world_env.environment.ambient_light_energy = 0.0
	dir_light.light_energy = 0.0
	overhead_spot.light_energy = 0.0
	omni_pulsing.light_energy = 0.0
	omni_gold.light_energy = 0.0
	wand_light.light_energy = 2.6
	
	# Initial label states
	title_label.scale = Vector3.ZERO
	title_label.modulate.a = 0.0
	dev_header_label.scale = Vector3.ZERO
	dev_header_label.modulate.a = 0.0
	dev_name_label.scale = Vector3.ZERO
	dev_name_label.modulate.a = 0.0
	credit_label.scale = Vector3.ZERO
	credit_label.modulate.a = 0.0
	subtitle_label.modulate.a = 0.0
	feature_label.modulate.a = 0.0
	prompt_label.modulate.a = 0.0
	
	# Camera initial framing
	camera.position = Vector3(0.0, 1.4, 6.4)
	camera.rotation_degrees = Vector3(-3.0, 0.0, 0.0)
	
	# Initial fade in
	fade_rect.modulate.a = 1.0
	var f_tween = create_tween()
	f_tween.tween_property(fade_rect, "modulate:a", 0.0, 1.2)
	
	# Start realistic 30-second choreographed showcase
	_run_30s_choreography()

func _process(delta: float) -> void:
	elapsed_time += delta
	
	# Rotate 3D core & rings
	if core_node:
		core_node.rotation_degrees.y += delta * 14.0
	if ring1:
		ring1.rotation_degrees.x += delta * 28.0
		ring1.rotation_degrees.y += delta * 18.0
	if ring2:
		ring2.rotation_degrees.x -= delta * 22.0
		ring2.rotation_degrees.z += delta * 30.0
	if crystal_orbit:
		crystal_orbit.rotation_degrees.y += delta * 40.0
		
	# Wand pulsing orb light
	if wand_light:
		wand_light.light_energy = 2.4 + sin(elapsed_time * 5.5) * 0.8
		wand_light.position.y = 0.95 + sin(elapsed_time * 3.5) * 0.08
		
	# Update ricocheting spell projectiles
	_update_3d_projectiles(delta)

func _run_30s_choreography() -> void:
	# -------------------------------------------------------------------------
	# ACT 1 (0.0s - 6.0s): MYSTERIOUS DARK SILHOUETTE
	# Shrouded in darkness, only the purple wand orb casts dramatic light
	# -------------------------------------------------------------------------
	player_anim.play("idle")
	
	# Slow cinematic camera zoom tracking the wizard's silhouette in the dark
	var cam_tween1 = create_tween().set_parallel(true)
	cam_tween1.tween_property(camera, "position", Vector3(0.8, 1.1, 5.0), 6.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	cam_tween1.tween_property(camera, "rotation_degrees:y", -6.0, 6.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	
	# Wizard practices wand flourishes in the dark
	await get_tree().create_timer(1.2).timeout
	if is_transitioning: return
	player_anim.play("attack")
	SoundManager.play_sfx_pitched("crystal", 0.6)
	
	await get_tree().create_timer(1.8).timeout
	if is_transitioning: return
	player_anim.play("idle")
	player_anim.flip_h = true
	
	# -------------------------------------------------------------------------
	# ACT 2 (6.0s - 12.0s): LIGHT DAWNS & STAGE AWAKENING
	# Overhead spotlight powers up; ambient light lightly reveals the dais
	# -------------------------------------------------------------------------
	await get_tree().create_timer(3.0).timeout
	if is_transitioning: return
	
	# Staff strike awakens the stage lighting!
	SoundManager.play_sfx("jump")
	SoundManager.play_sfx("checkpoint")
	
	# Overhead spotlight and ambient lights power up smoothly!
	var light_tween = create_tween().set_parallel(true)
	light_tween.tween_property(overhead_spot, "light_energy", 1.8, 2.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	if world_env and world_env.environment:
		light_tween.tween_property(world_env.environment, "ambient_light_energy", 0.35, 3.0)
	light_tween.tween_property(omni_pulsing, "light_energy", 0.8, 3.0)
	
	# Wizard begins rhythmic dance footwork on the glowing dais!
	player_anim.play("run")
	_dance_step_left_right(4.5)
	
	# Subtitle reveals cleanly
	var sub_tween = create_tween()
	sub_tween.tween_property(subtitle_label, "modulate:a", 1.0, 1.2)
	
	# Shoot twin fireballs that bounce in 3D
	await get_tree().create_timer(2.2).timeout
	if is_transitioning: return
	_player_shoot_spell("fireball", Vector3(-1.6, 2.4, -0.8))
	_player_shoot_spell("fireball", Vector3(1.6, 2.4, -0.8))
	SoundManager.play_sfx("fireball")

	# -------------------------------------------------------------------------
	# ACT 3 (12.0s - 19.0s): FULL REALISTIC ILLUMINATION & TITLE DROP
	# Sun/nebula key lights and gold rim lights engage; celestial rings sparkle
	# -------------------------------------------------------------------------
	await get_tree().create_timer(3.8).timeout
	if is_transitioning: return
	
	# Full key illumination: Directional sunlight & golden rim lights rise to full brilliance!
	var full_light_tween = create_tween().set_parallel(true)
	full_light_tween.tween_property(dir_light, "light_energy", 0.95, 2.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	full_light_tween.tween_property(omni_gold, "light_energy", 1.4, 2.0)
	full_light_tween.tween_property(omni_pulsing, "light_energy", 1.6, 2.0)
	if world_env and world_env.environment:
		full_light_tween.tween_property(world_env.environment, "ambient_light_energy", 0.85, 2.0)
	
	# Camera centers into heroic viewpoint
	var cam_tween2 = create_tween().set_parallel(true)
	cam_tween2.tween_property(camera, "position", Vector3(0.0, 0.45, 4.2), 3.0).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	cam_tween2.tween_property(camera, "rotation_degrees", Vector3(1.5, 0.0, 0.0), 3.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# High air-dancing pirouette leap!
	player_anim.play("jump")
	var jump_tween = create_tween()
	jump_tween.tween_property(player_anim, "position:y", 1.9, 0.8).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	jump_tween.tween_property(player_anim, "position:y", 0.75, 0.7).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	SoundManager.play_sfx("jump")
	
	await get_tree().create_timer(0.8).timeout
	if is_transitioning: return
	
	# Wand rapid-fire 4-way cross volley of ricocheting spells!
	player_anim.play("attack")
	_player_shoot_spell("gold", Vector3(-2.4, 1.6, -0.6))
	_player_shoot_spell("gold", Vector3(2.4, 1.6, -0.6))
	_player_shoot_spell("cyan", Vector3(-1.2, 3.4, -1.0))
	_player_shoot_spell("cyan", Vector3(1.2, 3.4, -1.0))
	SoundManager.play_sfx_pitched("crystal", 1.3)
	
	# MAIN TITLE "GAME: BOUNCE BACK" BOUNCES IN MASSIVELY WITH GOLD RADIANCE!
	await get_tree().create_timer(1.2).timeout
	if is_transitioning: return
	SoundManager.play_sfx("lightning")
	SoundManager.play_sfx_pitched("fireball", 0.7)
	
	title_label.scale = Vector3(0.05, 0.05, 0.05)
	title_label.modulate.a = 1.0
	var title_tween = create_tween()
	title_tween.tween_property(title_label, "scale", Vector3(1.0, 1.0, 1.0), 1.0).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

	# -------------------------------------------------------------------------
	# ACT 4 (19.0s - 26.0s): ULTRA-PROMINENT GAME DEVELOPERS: DHONI & PRATHIK
	# Triumphant Astral Void beam, firework cascades, and massive developer spotlight
	# -------------------------------------------------------------------------
	await get_tree().create_timer(4.8).timeout
	if is_transitioning: return
	
	# Camera tracks into low-angle dramatic view
	var cam_tween3 = create_tween().set_parallel(true)
	cam_tween3.tween_property(camera, "position", Vector3(-0.5, -0.15, 3.9), 3.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	cam_tween3.tween_property(camera, "rotation_degrees", Vector3(6.0, 6.0, 0.0), 3.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	
	# Wand twirls behind back and shoots skyward Astral Void beam!
	player_anim.play("attack")
	_player_shoot_spell("void", Vector3(0.0, 4.6, -0.4))
	SoundManager.play_sfx("teleport")
	
	await get_tree().create_timer(0.8).timeout
	if is_transitioning: return
	
	# GAME DEVELOPERS: DHONI & PRATHIK EMERGE WITH TRIUMPHANT FANFARE!
	SoundManager.play_sfx("victory")
	
	# Developer Header Badge
	var dev_h_tween = create_tween().set_parallel(true)
	dev_h_tween.tween_property(dev_header_label, "scale", Vector3(1.0, 1.0, 1.0), 0.7).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	dev_h_tween.tween_property(dev_header_label, "modulate:a", 1.0, 0.7)
	
	# Giant Developer Names: DHONI & PRATHIK (Electric Cyan with Gold Outline!)
	await get_tree().create_timer(0.4).timeout
	if is_transitioning: return
	SoundManager.play_sfx_pitched("crystal", 1.6)
	var dev_n_tween = create_tween().set_parallel(true)
	dev_n_tween.tween_property(dev_name_label, "scale", Vector3(1.15, 1.15, 1.15), 0.85).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	dev_n_tween.tween_property(dev_name_label, "modulate:a", 1.0, 0.85)
	
	# Secondary credit and feature badges
	await get_tree().create_timer(0.8).timeout
	if is_transitioning: return
	var cred_tween = create_tween().set_parallel(true)
	cred_tween.tween_property(credit_label, "scale", Vector3(1.0, 1.0, 1.0), 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	cred_tween.tween_property(credit_label, "modulate:a", 1.0, 0.6)
	cred_tween.tween_property(feature_label, "modulate:a", 1.0, 0.6)

	# -------------------------------------------------------------------------
	# ACT 5 (26.0s - 30.0s): GRAND FINALE DANCE POSE & INTERACTIVE PROMPT
	# Radiant golden victory posture and prompt pulse until auto-transition
	# -------------------------------------------------------------------------
	await get_tree().create_timer(3.0).timeout
	if is_transitioning: return
	
	# Camera smoothly returns to panoramic wide angle
	var cam_tween4 = create_tween().set_parallel(true)
	cam_tween4.tween_property(camera, "position", Vector3(0.0, 0.25, 4.6), 2.5).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	cam_tween4.tween_property(camera, "rotation_degrees", Vector3(0.0, 0.0, 0.0), 2.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# Player strikes radiant golden staff victory pose!
	player_anim.play("respawn")
	_player_shoot_spell("fireball", Vector3(-2.6, 2.0, -0.8))
	_player_shoot_spell("fireball", Vector3(2.6, 2.0, -0.8))
	_player_shoot_spell("gold", Vector3(0.0, 3.6, -0.8))
	SoundManager.play_sfx_pitched("crystal", 1.4)
	
	# Prompt pulses cleanly
	var p_tween = create_tween().set_loops()
	p_tween.tween_property(prompt_label, "modulate:a", 1.0, 0.5)
	p_tween.tween_property(prompt_label, "modulate:a", 0.35, 0.5)
	
	# At 30.0s mark, auto-transition smoothly to Main Menu
	await get_tree().create_timer(4.0).timeout
	if not is_transitioning:
		_transition_to_menu()

func _dance_step_left_right(duration: float) -> void:
	var steps = int(duration / 0.45)
	for i in range(steps):
		if is_transitioning: break
		player_anim.flip_h = (i % 2 == 1)
		var target_x = -0.32 if (i % 2 == 1) else 0.32
		var step_tween = create_tween()
		step_tween.tween_property(player_anim, "position:x", target_x, 0.38).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		await get_tree().create_timer(0.45).timeout
	player_anim.position.x = 0.0

func _player_shoot_spell(type: String, target_dir: Vector3) -> void:
	var mesh_inst = MeshInstance3D.new()
	var sphere = SphereMesh.new()
	sphere.radius = 0.13
	sphere.height = 0.26
	mesh_inst.mesh = sphere
	
	var mat = StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	if type == "fireball":
		mat.albedo_color = Color(1.0, 0.6, 0.15)
	elif type == "ice" or type == "cyan":
		mat.albedo_color = Color(0.25, 0.95, 1.0)
	elif type == "gold":
		mat.albedo_color = Color(1.0, 0.88, 0.25)
	else:
		mat.albedo_color = Color(0.85, 0.3, 1.0)
	mesh_inst.material_override = mat
	
	mesh_inst.position = stage.position + player_anim.position + Vector3(0.25, 0.2, 0.0)
	projectile_container.add_child(mesh_inst)
	
	var p_data = {
		"node": mesh_inst,
		"velocity": target_dir.normalized() * 5.2,
		"life": 4.0,
		"bounces": 0,
		"max_bounces": 3
	}
	active_projectiles.append(p_data)

func _update_3d_projectiles(delta: float) -> void:
	var alive = []
	for p in active_projectiles:
		var node: MeshInstance3D = p["node"]
		if not is_instance_valid(node):
			continue
			
		node.position += p["velocity"] * delta
		p["life"] -= delta
		
		if abs(node.position.x) > 3.4 and p["bounces"] < p["max_bounces"]:
			p["velocity"].x *= -1.0
			p["bounces"] += 1
			SoundManager.play_sfx_pitched("crystal", 1.0 + float(p["bounces"]) * 0.2)
		if node.position.y > 3.4 and p["bounces"] < p["max_bounces"]:
			p["velocity"].y *= -1.0
			p["bounces"] += 1
			SoundManager.play_sfx_pitched("crystal", 1.0 + float(p["bounces"]) * 0.2)
			
		if p["life"] > 0.0:
			alive.append(p)
		else:
			node.queue_free()
	active_projectiles = alive

func _input(event: InputEvent) -> void:
	if is_transitioning:
		return
	if event is InputEventKey and event.pressed and not event.echo:
		_transition_to_menu()
	elif event is InputEventMouseButton and event.pressed:
		_transition_to_menu()

func _transition_to_menu() -> void:
	if is_transitioning:
		return
	is_transitioning = true
	SoundManager.play_sfx("click")
	
	var tween = create_tween()
	tween.tween_property(fade_rect, "modulate:a", 1.0, 0.5)
	await tween.finished
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
