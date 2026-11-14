extends AnimatableBody2D

@export var move_offset: Vector2 = Vector2(140.0, 0.0)
@export var speed: float = 50.0

var start_pos: Vector2 = Vector2.ZERO
var target_pos: Vector2 = Vector2.ZERO
var direction: float = 1.0

func _ready() -> void:
	sync_to_physics = true
	start_pos = global_position
	target_pos = start_pos + move_offset

func _physics_process(delta: float) -> void:
	var dest = target_pos if direction > 0 else start_pos
	global_position = global_position.move_toward(dest, speed * delta)
	
	if global_position.distance_to(dest) < 2.0:
		direction *= -1.0
