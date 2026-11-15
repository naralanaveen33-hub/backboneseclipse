extends Node3D

@onready var camera: Camera3D = $Camera3D
@onready var core_node: Node3D = $CentralCore
@onready var ring1: MeshInstance3D = $CentralCore/Ring1
@onready var ring2: MeshInstance3D = $CentralCore/Ring2
@onready var crystal_orbit: Node3D = $CentralCore/CrystalOrbit
@onready var light_pulse: OmniLight3D = $OmniLightPulsing

@onready var stage: Node3D = $Stage
@onready var player_anim: AnimatedSprite3D = $Stage/PlayerSprite
@onready var wand_light: OmniLight3D = $Stage/WandLight
@onready var projectile_container: Node3D = $Projectiles

@onready var title_label: Label3D = $Labels/TitleLabel3D
@onready var credit_label: Label3D = $Labels/CreditLabel3D
@onready var subtitle_label: Label3D = $Labels/SubtitleLabel3D
@onready var feature_label: Label3D = $Labels/FeatureLabel3D
@onready var prompt_label: Label3D = $Labels/PromptLabel3D

@onready var fade_rect: ColorRect = $Overlay/FadeRect

var is_transitioning: bool = false
var elapsed_time: float = 0.0
var total_duration: float = 20.0

# 3D spell projectile template
var active_projectiles = []

func _ready() -> void:
	SoundManager.play_music("dark_dream")
	
	# Initial visibility & transformations for smooth reveals
	title_label.scale = Vector3.ZERO
	title_label.modulate.a = 0.0
	credit_label.scale = Vector3.ZERO
	credit_label.modulate.a = 0.0
	subtitle_label.modulate.a = 0.0
	feature_label.modulate.a = 0.0
	prompt_label.modulate.a = 0.0
	
	# Initial camera staging
	camera.position = Vector3(0.0, 1.6, 6.8)
	camera.rotation_degrees = Vector3(-4.0, 0.0, 0.0)
	
	# Fade-in from black
	fade_rect.modulate.a = 1.0
	var f_tween = create_tween()
	f_tween.tween_property(fade_rect, "modulate:a", 0.0, 1.0)
	
	# Start 20-second Choreography & Showcase
	_run_20s_choreography()

func _process(delta: float) -> void:
	elapsed_time += delta
	
	# 3D core & celestial rings rotations
	if core_node:
		core_node.rotation_degrees.y += delta * 15.0
	if ring1:
		ring1.rotation_degrees.x += delta * 30.0
		ring1.rotation_degrees.y += delta * 20.0
	if ring2:
		ring2.rotation_degrees.x -= delta * 25.0
		ring2.rotation_degrees.z += delta * 35.0
	if crystal_orbit:
		crystal_orbit.rotation_degrees.y += delta * 45.0
		
	# Wand glowing orb pulse
	if wand_light:
		wand_light.light_energy = 1.8 + sin(elapsed_time * 6.0) * 0.7
		wand_light.position.y = 0.95 + sin(elapsed_time * 4.0) * 0.08
		
	# Pulsing central omni light
	if light_pulse:
		light_pulse.light_energy = 1.4 + sin(elapsed_time * 2.5) * 0.5
		
	# Update active ricocheting 3D spell projectiles
	_update_3d_projectiles(delta)

func _run_20s_choreography() -> void:
	# -------------------------------------------------------------
	# PHASE 1 (0.0s - 5.0s): DANCE STEP & FIRST ROCKED SHOT
	# -------------------------------------------------------------
	player_anim.play("idle")
	
	# Camera slow dramatic orbital sweep
	var cam_tween = create_tween().set_parallel(true)
	cam_tween.tween_property(camera, "position", Vector3(1.2, 1.2, 5.2), 5.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	cam_tween.tween_property(camera, "rotation_degrees:y", -8.0, 5.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	
	# 0.8s: Player starts rhythmic dance footwork!
	await get_tree().create_timer(0.8).timeout
	if is_transitioning: return
	player_anim.play("run")
	_dance_step_left_right(3.2)
	
	# 1.4s: Subtitle reveals
	var sub_tween = create_tween()
	sub_tween.tween_property(subtitle_label, "modulate:a", 1.0, 0.8)
	
	# 2.2s: First wand flourish & shooting fireballs into the air!
	await get_tree().create_timer(1.4).timeout
	if is_transitioning: return
	_player_shoot_spell("fireball", Vector3(-1.4, 2.2, -1.0))
	_player_shoot_spell("fireball", Vector3(1.4, 2.2, -1.0))
	
	# 3.8s: Quick twirl and ice blast
	await get_tree().create_timer(1.6).timeout
	if is_transitioning: return
	_player_shoot_spell("ice", Vector3(0.0, 2.8, -1.5))

	# -------------------------------------------------------------
	# PHASE 2 (5.0s - 11.0s): JUMP PIRUETTE, BARRAGE & TITLE REVEAL
	# -------------------------------------------------------------
	await get_tree().create_timer(1.2).timeout
	if is_transitioning: return
	
	# Camera zooms closer, pans to center hero angle
	var cam_tween2 = create_tween().set_parallel(true)
	cam_tween2.tween_property(camera, "position", Vector3(0.0, 0.5, 4.4), 3.5).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	cam_tween2.tween_property(camera, "rotation_degrees", Vector3(2.0, 0.0, 0.0), 3.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# High jump & air-dancing staff spin!
	player_anim.play("jump")
	var jump_tween = create_tween()
	jump_tween.tween_property(player_anim, "position:y", 1.8, 0.7).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	jump_tween.tween_property(player_anim, "position:y", 0.75, 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	SoundManager.play_sfx("jump")
	
	await get_tree().create_timer(0.7).timeout
	if is_transitioning: return
	
	# Rapid wand attack shooting a 4-way cross volley of ricocheting spells!
	player_anim.play("attack")
	_player_shoot_spell("gold", Vector3(-2.2, 1.4, -0.8))
	_player_shoot_spell("gold", Vector3(2.2, 1.4, -0.8))
	_player_shoot_spell("cyan", Vector3(-1.0, 3.2, -1.2))
	_player_shoot_spell("cyan", Vector3(1.0, 3.2, -1.2))
	SoundManager.play_sfx_pitched("crystal", 1.2)
	
	# 7.2s: TITLE "GAME: BOUNCE BACK" BOUNCES IN MASSIVELY!
	await get_tree().create_timer(1.5).timeout
	if is_transitioning: return
	SoundManager.play_sfx("lightning")
	SoundManager.play_sfx_pitched("fireball", 0.7)
	
	title_label.scale = Vector3(0.05, 0.05, 0.05)
	title_label.modulate.a = 1.0
	var title_tween = create_tween()
	title_tween.tween_property(title_label, "scale", Vector3(1.0, 1.0, 1.0), 0.95).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

	# -------------------------------------------------------------
	# PHASE 3 (11.0s - 16.5s): ASTRAL BEAM & DHONI + PRATHIK CREDITS
	# -------------------------------------------------------------
	await get_tree().create_timer(3.8).timeout
	if is_transitioning: return
	
	# Camera shifts into low epic heroic angle
	var cam_tween3 = create_tween().set_parallel(true)
	cam_tween3.tween_property(camera, "position", Vector3(-0.8, -0.2, 3.8), 4.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	cam_tween3.tween_property(camera, "rotation_degrees", Vector3(7.0, 10.0, 0.0), 4.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	
	# Power dance flourish: wand twirls behind back and shoots skyward beam!
	player_anim.play("attack")
	_player_shoot_spell("void", Vector3(0.0, 4.5, -0.5))
	SoundManager.play_sfx("teleport")
	
	await get_tree().create_timer(0.6).timeout
	if is_transitioning: return
	
	# CREATED BY DHONI AND PRATHIK emerges with triumphant victory sound!
	SoundManager.play_sfx("victory")
	credit_label.position.y = -0.95
	var cred_tween = create_tween().set_parallel(true)
	cred_tween.tween_property(credit_label, "scale", Vector3(1.0, 1.0, 1.0), 0.85).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	cred_tween.tween_property(credit_label, "modulate:a", 1.0, 0.85)
	cred_tween.tween_property(credit_label, "position:y", -0.65, 0.85).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# Feature badge reveals
	var feat_tween = create_tween()
	feat_tween.tween_property(feature_label, "modulate:a", 1.0, 0.7)

	# -------------------------------------------------------------
	# PHASE 4 (16.5s - 20.0s): GRAND FINALE DANCE POSE & PROMPT
	# -------------------------------------------------------------
	await get_tree().create_timer(2.6).timeout
	if is_transitioning: return
	
	# Camera pulls back smoothly to full cinematic view
	var cam_tween4 = create_tween().set_parallel(true)
	cam_tween4.tween_property(camera, "position", Vector3(0.0, 0.35, 4.8), 2.5).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	cam_tween4.tween_property(camera, "rotation_degrees", Vector3(0.0, 0.0, 0.0), 2.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# Player strikes glowing victory pose with radiant staff!
	player_anim.play("respawn")
	_player_shoot_spell("fireball", Vector3(-2.8, 1.8, -1.0))
	_player_shoot_spell("fireball", Vector3(2.8, 1.8, -1.0))
	_player_shoot_spell("cyan", Vector3(0.0, 3.5, -1.0))
	SoundManager.play_sfx_pitched("crystal", 1.5)
	
	# Prompt label pulses clearly
	var p_tween = create_tween().set_loops()
	p_tween.tween_property(prompt_label, "modulate:a", 1.0, 0.5)
	p_tween.tween_property(prompt_label, "modulate:a", 0.3, 0.5)
	
	# At 20.0s mark, auto-transition smoothly to Main Menu
	await get_tree().create_timer(3.2).timeout
	if not is_transitioning:
		_transition_to_menu()

func _dance_step_left_right(duration: float) -> void:
	var steps = int(duration / 0.4)
	for i in range(steps):
		if is_transitioning: break
		player_anim.flip_h = (i % 2 == 1)
		var target_x = -0.3 if (i % 2 == 1) else 0.3
		var step_tween = create_tween()
		step_tween.tween_property(player_anim, "position:x", target_x, 0.35).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		await get_tree().create_timer(0.4).timeout
	player_anim.position.x = 0.0

func _player_shoot_spell(type: String, target_dir: Vector3) -> void:
	# Instantiate a glowing 3D ricocheting spell sphere
	var mesh_inst = MeshInstance3D.new()
	var sphere = SphereMesh.new()
	sphere.radius = 0.12
	sphere.height = 0.24
	mesh_inst.mesh = sphere
	
	var mat = StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	if type == "fireball":
		mat.albedo_color = Color(1.0, 0.65, 0.2)
	elif type == "ice" or type == "cyan":
		mat.albedo_color = Color(0.2, 0.9, 1.0)
	elif type == "gold":
		mat.albedo_color = Color(1.0, 0.9, 0.3)
	else:
		mat.albedo_color = Color(0.8, 0.3, 1.0)
	mesh_inst.material_override = mat
	
	# Position at wand tip
	mesh_inst.position = stage.position + player_anim.position + Vector3(0.25, 0.2, 0.0)
	projectile_container.add_child(mesh_inst)
	
	var p_data = {
		"node": mesh_inst,
		"velocity": target_dir.normalized() * 4.8,
		"life": 3.8,
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
		
		# Ricochet bounce off 3D boundaries (X: [-3.5, 3.5], Y: [-0.5, 3.5], Z: [-2.5, 2.0])
		if abs(node.position.x) > 3.2 and p["bounces"] < p["max_bounces"]:
			p["velocity"].x *= -1.0
			p["bounces"] += 1
			SoundManager.play_sfx_pitched("crystal", 1.0 + float(p["bounces"]) * 0.2)
		if node.position.y > 3.2 and p["bounces"] < p["max_bounces"]:
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
	tween.tween_property(fade_rect, "modulate:a", 1.0, 0.45)
	await tween.finished
	get_tree().change_scene_to_file("res://scenes/menus/main_menu.tscn")
