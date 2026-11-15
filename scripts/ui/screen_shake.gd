extends Node

# Screen Shake Autoload - Heavy graphical feedback for hits, explosions, explosions
var shake_offset: Vector2 = Vector2.ZERO
var shake_duration: float = 0.0
var shake_magnitude: float = 0.0
var shake_fade: float = 1.0

# Camera reference (set by the main camera node)
var camera: Node2D = null
var original_camera_offset: Vector2 = Vector2.ZERO

func _process(delta: float) -> void:
	if shake_duration > 0.0:
		shake_duration -= delta
		# Decay magnitude over time
		var t = 1.0 - clamp(shake_duration / 0.5, 0.0, 1.0)
		var current_mag = shake_magnitude * (1.0 - t)
		
		# Generate random shake offset
		var rng = RandomNumberGenerator.new()
		rng.seed = Time.get_ticks_msec() + randi()
		shake_offset = Vector2(
			rng.randf_range(-current_mag, current_mag),
			rng.randf_range(-current_mag, current_mag)
		)
		
		if camera and is_instance_valid(camera):
			camera.global_position = original_camera_offset + shake_offset
	else:
		shake_offset = Vector2.ZERO
		if camera and is_instance_valid(camera):
			camera.global_position = original_camera_offset

func trigger_shake(duration: float = 0.2, magnitude: float = 8.0) -> void:
	shake_duration = max(shake_duration, duration)
	shake_magnitude = max(shake_magnitude, magnitude)

func bind_camera(cam_node: Node2D) -> void:
	camera = cam_node
	if camera:
		original_camera_offset = camera.global_position