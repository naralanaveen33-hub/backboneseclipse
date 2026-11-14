extends Area2D

@export var boss_node: NodePath

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		var boss = get_node_or_null(boss_node)
		if boss and boss.has_method("activate_boss"):
			if boss.has_method("activate_boss"):
				if boss is CharacterBody2D and boss.get("teleport_anchors") != null:
					# Dark wizard boss with anchors
					var anchors: Array[Vector2] = []
					if has_node("Anchors"):
						for c in $Anchors.get_children():
							anchors.append(c.global_position)
					boss.activate_boss(anchors)
				else:
					boss.activate_boss()
		queue_free()
