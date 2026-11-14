extends Area2D

@export var max_shield_hp: float = 2500.0
var shield_hp: float = 2500.0
var duration: float = 8.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D

signal shield_broken()

func _ready() -> void:
	add_to_group("boss_shield")
	shield_hp = max_shield_hp
	SoundManager.play_sfx("shield")
	sprite.scale = Vector2(0.2, 0.2)
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.2, 1.2), 0.3)
	area_entered.connect(_on_area_entered)

func _process(delta: float) -> void:
	sprite.rotation += delta * 1.5
	duration -= delta
	if duration <= 0.0:
		break_shield()

var is_broken: bool = false

func take_damage(amount: float, _type: String = "magic") -> void:
	if is_broken:
		return
	shield_hp -= amount
	SoundManager.play_sfx("shield")
	GameManager.pop_floating_text("SHIELD -%d" % int(amount), global_position + Vector2(0, -40), Color(0.4, 0.9, 1.0))
	
	if shield_hp <= 0.0:
		break_shield()
		return

	# Flash white/blue
	var orig_color = sprite.modulate
	sprite.modulate = Color(2.0, 2.0, 2.5)
	var tween = create_tween()
	tween.tween_property(sprite, "modulate", orig_color, 0.08)

func break_shield() -> void:
	if is_broken:
		return
	is_broken = true
	set_process(false)
	col_shape.set_deferred("disabled", true)
	SoundManager.play_sfx("shield_break")
	GameManager.pop_floating_text("SHIELD SHATTERED!", global_position + Vector2(0, -45), Color(1.0, 0.4, 0.4))
	shield_broken.emit()
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.8, 1.8), 0.15)
	tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.15)
	tween.tween_callback(queue_free)

func _on_area_entered(area: Area2D) -> void:
	if area.is_in_group("player_projectiles"):
		var dmg = 45.0
		if "damage" in area:
			dmg = area.damage
		take_damage(dmg)
		if area.has_method("_explode"):
			area._explode()
		elif area.has_method("queue_free"):
			area.queue_free()
