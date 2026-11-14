extends CharacterBody2D
class_name EnemyBase

@export var max_hp: float = 50.0
var hp: float = 50.0
@export var damage: float = 15.0
@export var speed: float = 70.0
@export var crystals_dropped: int = 2

var is_dead: bool = false
var is_frozen: bool = false
var freeze_timer: float = 0.0

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
var ice_overlay: Sprite2D = null

const SCENE_CRYSTAL = preload("res://scenes/objects/crystal.tscn")

func _ready() -> void:
	add_to_group("enemies")
	hp = max_hp
	_setup_ice_overlay()

func _setup_ice_overlay() -> void:
	ice_overlay = Sprite2D.new()
	var tex = load("res://assets/effects/projectiles/ice_freeze.png")
	if tex:
		ice_overlay.texture = tex
	ice_overlay.visible = false
	add_child(ice_overlay)

func _process(delta: float) -> void:
	if is_frozen:
		freeze_timer -= delta
		if freeze_timer <= 0.0:
			unfreeze()

func take_damage(amount: float, type: String = "magic") -> void:
	if is_dead:
		return
	hp -= amount
	SoundManager.play_sfx("enemy_hurt")
	_play_hurt_anim()
	
	if hp <= 0.0:
		die()

func freeze_enemy(duration: float) -> void:
	if is_dead:
		return
	is_frozen = true
	freeze_timer = duration
	if ice_overlay:
		ice_overlay.visible = true
	anim.modulate = Color(0.6, 0.8, 1.0, 1.0)
	anim.pause()

func unfreeze() -> void:
	is_frozen = false
	if ice_overlay:
		ice_overlay.visible = false
	anim.modulate = Color.WHITE
	anim.play()

func _play_hurt_anim() -> void:
	var orig_color = anim.modulate
	anim.modulate = Color(1.0, 0.3, 0.3, 1.0)
	await get_tree().create_timer(0.12).timeout
	if not is_frozen and not is_dead:
		anim.modulate = orig_color

func die() -> void:
	if is_dead:
		return
	is_dead = true
	SoundManager.play_sfx("enemy_death")
	unfreeze()
	set_physics_process(false)
	
	# Disable collision
	$CollisionShape2D.set_deferred("disabled", true)
	if has_node("Hitbox"):
		$Hitbox/CollisionShape2D.set_deferred("disabled", true)
		
	# Drop crystals
	for i in range(crystals_dropped):
		var c = SCENE_CRYSTAL.instantiate()
		c.global_position = global_position + Vector2(randf_range(-12, 12), randf_range(-8, 8))
		get_parent().call_deferred("add_child", c)
		
	if anim and anim.sprite_frames.has_animation("death"):
		anim.play("death")
		await anim.animation_finished
	else:
		var tween = create_tween()
		tween.tween_property(self, "modulate:a", 0.0, 0.3)
		await tween.finished
	queue_free()

func _on_hitbox_body_entered(body: Node2D) -> void:
	if not is_dead and not is_frozen and body.has_method("take_damage"):
		body.take_damage(damage, global_position)
