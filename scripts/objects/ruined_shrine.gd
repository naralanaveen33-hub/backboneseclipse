extends Area2D

@export var stat_buff: String = "hp" # "hp", "speed", or "rebound"
var is_active: bool = false

@onready var sprite: Sprite2D = $Sprite2D
const TEX_DORMANT = preload("res://assets/tiles/shrine_dormant.png")
const TEX_ACTIVE = preload("res://assets/tiles/shrine_active.png")

func _ready() -> void:
	add_to_group("shrines")
	sprite.texture = TEX_DORMANT
	
	# Color tint the base runes according to the buff type
	match stat_buff:
		"hp":
			modulate = Color(0.9, 1.0, 0.9)
		"speed":
			modulate = Color(0.9, 0.95, 1.0)
		"rebound":
			modulate = Color(1.0, 1.0, 0.85)

func activate_shrine() -> void:
	if is_active:
		return
	is_active = true
	sprite.texture = TEX_ACTIVE
	
	# Scale punch animation
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.35, 1.35), 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(sprite, "scale", Vector2(1.0, 1.0), 0.20).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	SoundManager.play_sfx_pitched("crystal", 1.4)
	SoundManager.play_sfx("victory")
	GameManager.apply_shrine_buff(stat_buff, global_position)

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and not is_active:
		GameManager.post_notification("A Dormant Ruined Shrine... Hit it with a Ricocheted Spell to awaken it!")

func _on_area_entered(area: Area2D) -> void:
	# Also allow fireball area to trigger it
	if area.is_in_group("player_projectiles") or area.name.begins_with("Fireball"):
		activate_shrine()
