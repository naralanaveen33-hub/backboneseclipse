extends StaticBody2D

class_name SecretWall

@export var is_revealed: bool = false
@onready var sprite: Sprite2D = $Sprite2D
@onready var col_shape: CollisionShape2D = $CollisionShape2D
@onready var trigger_area: Area2D = $TriggerArea

func _ready() -> void:
	add_to_group("shrines") # Allows ricocheting spells to hit and trigger it
	if trigger_area:
		trigger_area.body_entered.connect(_on_trigger_body_entered)
		trigger_area.area_entered.connect(_on_trigger_area_entered)

func reveal_secret() -> void:
	if is_revealed:
		return
	is_revealed = true
	col_shape.set_deferred("disabled", true)
	SoundManager.play_sfx("explosion", 0.08)
	SoundManager.play_sfx("checkpoint")
	GameManager.pop_floating_text("✦ SECRET PASSAGE OPENED! ✦", global_position + Vector2(0, -30), Color(0.3, 0.9, 1.0))
	
	var tween = create_tween()
	tween.tween_property(sprite, "modulate:a", 0.15, 0.4)

func activate_shrine() -> void:
	reveal_secret()

func take_damage(_amount: float, _type: String = "") -> void:
	reveal_secret()

func _on_trigger_body_entered(body: Node2D) -> void:
	if not is_revealed and body.is_in_group("player"):
		reveal_secret()

func _on_trigger_area_entered(area: Area2D) -> void:
	if not is_revealed and area.is_in_group("player_projectiles"):
		reveal_secret()
