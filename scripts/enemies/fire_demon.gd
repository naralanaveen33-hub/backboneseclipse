extends EnemyBase

@export var cast_range: float = 240.0
@export var cast_cooldown: float = 2.2
var cooldown_timer: float = 0.5
var is_casting: bool = false
var facing: float = 1.0

const SCENE_DEMON_PROJECTILE = preload("res://scenes/enemies/demon_projectile.tscn")

func _ready() -> void:
	max_hp = 70.0
	damage = 18.0
	speed = 45.0
	crystals_dropped = 3
	super._ready()
	anim.play("idle")

func _physics_process(delta: float) -> void:
	if is_dead or is_frozen:
		velocity = Vector2.ZERO
		return

	if not is_on_floor():
		velocity.y += 980.0 * delta

	cooldown_timer -= delta
	var player = get_tree().get_first_node_in_group("player")

	if player and not player.is_dead:
		var dist = global_position.distance_to(player.global_position)
		facing = signf(player.global_position.x - global_position.x)
		anim.flip_h = (facing < 0)
		
		if dist <= cast_range and cooldown_timer <= 0.0 and not is_casting:
			_cast_flame(player)
		elif not is_casting:
			velocity.x = facing * speed * 0.5
			anim.play("idle")
	else:
		velocity.x = 0.0
		anim.play("idle")

	move_and_slide()

func _cast_flame(player: Node2D) -> void:
	is_casting = true
	velocity.x = 0.0
	anim.play("attack")
	
	await anim.animation_finished
	if not is_dead and not is_frozen and player:
		var p = SCENE_DEMON_PROJECTILE.instantiate()
		p.global_position = global_position + Vector2(facing * 18.0, -4.0)
		p.direction = (player.global_position - global_position).normalized()
		get_parent().add_child(p)
		SoundManager.play_sfx("fireball", 0.1)
		
	is_casting = false
	cooldown_timer = cast_cooldown
	anim.play("idle")
