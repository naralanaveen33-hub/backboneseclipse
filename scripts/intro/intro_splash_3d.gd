extends Node3D

@onready var camera: Camera3D = $Camera3D
@onready var core_node: Node3D = $CentralCore
@onready var ring1: MeshInstance3D = $CentralCore/Ring1
@onready var ring2: MeshInstance3D = $CentralCore/Ring2
@onready var crystal_orbit: Node3D = $CentralCore/CrystalOrbit
@onready var light_pulse: OmniLight3D = $OmniLightPulsing

@onready var title_label: Label3D = $Labels/TitleLabel3D
@onready var credit_label: Label3D = $Labels/CreditLabel3D
@onready var subtitle_label: Label3D = $Labels/SubtitleLabel3D
@onready var prompt_label: Label3D = $Labels/PromptLabel3D

@onready var fade_rect: ColorRect = $Overlay/FadeRect

var is_transitioning: bool = false
var elapsed_time: float = 0.0

func _ready() -> void:
	SoundManager.play_music("dark_dream")
	
	# Initial states for 3D bounce-in animations
	title_label.scale = Vector3.ZERO
	credit_label.scale = Vector3.ZERO
	credit_label.modulate.a = 0.0
	subtitle_label.modulate.a = 0.0
	prompt_label.modulate.a = 0.0
	
	# Camera initial setup
	camera.position = Vector3(0.0, 1.8, 8.2)
	camera.rotation_degrees = Vector3(-6.0, 0.0, 0.0)
	
	# Fade-in from black
	fade_rect.modulate.a = 1.0
	var f_tween = create_tween()
	f_tween.tween_property(fade_rect, "modulate:a", 0.0, 0.8)
	
	# Camera Dolly-in Tween
	var cam_tween = create_tween().set_parallel(true)
	cam_tween.tween_property(camera, "position", Vector3(0.0, 0.1, 4.8), 4.2).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	cam_tween.tween_property(camera, "rotation_degrees", Vector3(0.0, 0.0, 0.0), 4.2).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# Timeline sequence for titles
	_play_intro_timeline()

func _play_intro_timeline() -> void:
	# 0.5s: Subtitle reveals
	await get_tree().create_timer(0.5).timeout
	if is_transitioning: return
	var sub_tween = create_tween()
	sub_tween.tween_property(subtitle_label, "modulate:a", 1.0, 0.7)
	
	# 1.1s: GAME: BOUNCE BACK Title Bounces in with high impact!
	await get_tree().create_timer(0.6).timeout
	if is_transitioning: return
	SoundManager.play_sfx_pitched("crystal", 0.85)
	SoundManager.play_sfx("jump")
	var title_tween = create_tween()
	title_tween.tween_property(title_label, "scale", Vector3(1.0, 1.0, 1.0), 0.85).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	
	# 2.2s: CREATED BY DHONI AND PRATHIK emerges with triumphant fanfare!
	await get_tree().create_timer(1.1).timeout
	if is_transitioning: return
	SoundManager.play_sfx("victory")
	credit_label.position.y = -0.9
	var cred_tween = create_tween().set_parallel(true)
	cred_tween.tween_property(credit_label, "scale", Vector3(1.0, 1.0, 1.0), 0.75).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	cred_tween.tween_property(credit_label, "modulate:a", 1.0, 0.75)
	cred_tween.tween_property(credit_label, "position:y", -0.62, 0.75).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# 3.4s: Prompt pulses
	await get_tree().create_timer(1.2).timeout
	if is_transitioning: return
	var p_tween = create_tween().set_loops()
	p_tween.tween_property(prompt_label, "modulate:a", 1.0, 0.6)
	p_tween.tween_property(prompt_label, "modulate:a", 0.25, 0.6)
	
	# Auto-proceed after 7.0 seconds of showcase
	await get_tree().create_timer(3.6).timeout
	if not is_transitioning:
		_transition_to_menu()

func _process(delta: float) -> void:
	elapsed_time += delta
	
	# 3D core & ring rotations
	if core_node:
		core_node.rotation_degrees.y += delta * 18.0
	if ring1:
		ring1.rotation_degrees.x += delta * 45.0
		ring1.rotation_degrees.y += delta * 25.0
	if ring2:
		ring2.rotation_degrees.x -= delta * 35.0
		ring2.rotation_degrees.z += delta * 40.0
	if crystal_orbit:
		crystal_orbit.rotation_degrees.y += delta * 50.0
		
	# Subtle floating camera breathing
	if not is_transitioning and camera:
		camera.position.y += sin(elapsed_time * 1.5) * (delta * 0.05)
		camera.position.x += cos(elapsed_time * 1.1) * (delta * 0.03)
		
	# Pulsing light intensity
	if light_pulse:
		light_pulse.light_energy = 1.2 + sin(elapsed_time * 3.0) * 0.45

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
