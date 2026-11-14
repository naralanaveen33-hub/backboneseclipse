extends Node2D

class_name BossGhostTrail

static func spawn_ghost(parent: Node2D, sprite: AnimatedSprite2D, tint: Color = Color(0.8, 0.2, 0.6, 0.6), fade_time: float = 0.28) -> void:
	if not parent or not sprite:
		return
		
	var ghost = Sprite2D.new()
	var cur_frame_tex = sprite.sprite_frames.get_frame_texture(sprite.animation, sprite.frame)
	if not cur_frame_tex:
		return
		
	ghost.texture = cur_frame_tex
	ghost.global_position = sprite.global_position
	ghost.scale = sprite.scale * sprite.global_scale
	ghost.flip_h = sprite.flip_h
	ghost.flip_v = sprite.flip_v
	ghost.rotation = sprite.global_rotation
	ghost.modulate = tint
	ghost.top_level = true
	
	parent.get_parent().add_child(ghost)
	
	var tween = ghost.create_tween()
	tween.tween_property(ghost, "modulate:a", 0.0, fade_time)
	tween.tween_callback(ghost.queue_free)
