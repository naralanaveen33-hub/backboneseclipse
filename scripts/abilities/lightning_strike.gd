extends Area2D

@export var damage: float = 95.0
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
	top_level = true
	SoundManager.play_sfx("lightning")
	anim.play("strike")
	# Check immediately for enemies in the strike zone
	await get_tree().physics_frame
	var bodies = get_overlapping_bodies()
	for b in bodies:
		if b.is_in_group("enemies") or b.has_method("take_damage"):
			b.take_damage(damage, "lightning")
	var areas = get_overlapping_areas()
	for a in areas:
		var p = a.get_parent()
		if p and (p.is_in_group("enemies") or p.has_method("take_damage")):
			p.take_damage(damage, "lightning")
			
	await anim.animation_finished
	# Fade out
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.2)
	await tween.finished
	queue_free()

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("enemies") or body.has_method("take_damage"):
		body.take_damage(damage, "lightning")

func _on_area_entered(area: Area2D) -> void:
	var parent = area.get_parent()
	if parent and (parent.is_in_group("enemies") or parent.has_method("take_damage")):
		parent.take_damage(damage, "lightning")
