extends Area2D

@export var telegraph_time: float = 0.50
@export var beam_duration: float = 0.70
@export var damage_per_sec: float = 55.0
@export var beam_length: float = 900.0

var is_firing: bool = false
var facing: float = 1.0

@onready var beam_sprite: Sprite2D = $BeamSprite
@onready var col_shape: CollisionShape2D = $CollisionShape2D
@onready var telegraph_line: Line2D = $TelegraphLine

func _ready() -> void:
	add_to_group("enemy_projectiles")
	top_level = true
	col_shape.disabled = true
	beam_sprite.visible = false
	
	# Configure telegraph
	telegraph_line.clear_points()
	telegraph_line.add_point(Vector2.ZERO)
	telegraph_line.add_point(Vector2(facing * beam_length, 0))
	telegraph_line.default_color = Color(1.0, 0.1, 0.3, 0.4)
	telegraph_line.width = 2.0
	
	_charge_and_fire()

func setup(origin_pos: Vector2, face_dir: float) -> void:
	global_position = origin_pos
	facing = face_dir

func _charge_and_fire() -> void:
	SoundManager.play_sfx_pitched("crystal", 0.6)
	
	# Telegraph flashes thinner to wider
	var tween = create_tween()
	tween.tween_property(telegraph_line, "width", 4.0, telegraph_time)
	tween.parallel().tween_property(telegraph_line, "default_color:a", 0.95, telegraph_time)
	await tween.finished
	
	telegraph_line.visible = false
	_fire_beam()

func _fire_beam() -> void:
	if not is_inside_tree():
		return
	is_firing = true
	col_shape.disabled = false
	beam_sprite.visible = true
	
	# Scale beam sprite to cover full arena width
	var tex_w = beam_sprite.texture.get_width() if beam_sprite.texture else 128.0
	var scale_x = (beam_length / tex_w) * facing
	beam_sprite.scale = Vector2(scale_x, 1.6)
	beam_sprite.position = Vector2(facing * (beam_length / 2.0), 0)
	
	# Align collision shape
	col_shape.position = Vector2(facing * (beam_length / 2.0), 0)
	if col_shape.shape is RectangleShape2D:
		col_shape.shape.size = Vector2(beam_length, 28.0)
		
	SoundManager.play_sfx("lightning")
	SoundManager.play_sfx("boss_roar", 0.1)
	GameManager.hit_stop(0.04)
	
	# Pulsing intensity
	var fire_tween = create_tween()
	fire_tween.tween_property(beam_sprite, "scale:y", 2.2, 0.15)
	fire_tween.tween_property(beam_sprite, "scale:y", 1.4, 0.20)
	fire_tween.tween_interval(beam_duration - 0.35)
	fire_tween.tween_property(beam_sprite, "scale:y", 0.1, 0.12)
	fire_tween.parallel().tween_property(beam_sprite, "modulate:a", 0.0, 0.12)
	
	await fire_tween.finished
	queue_free()

func _physics_process(delta: float) -> void:
	if is_firing:
		var bodies = get_overlapping_bodies()
		for b in bodies:
			if b.is_in_group("player") and b.has_method("take_damage"):
				b.take_damage(damage_per_sec * delta, global_position)
