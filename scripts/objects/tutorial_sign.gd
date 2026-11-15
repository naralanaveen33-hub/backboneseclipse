extends Area2D

@export_multiline var message: String = "Press [A] / [D] to Move, [Space] to Jump!"
@onready var label: Label = $Label
@onready var panel: ColorRect = $Panel if has_node("Panel") else null

func _ready() -> void:
	label.text = message
	label.visible = false
	if panel:
		panel.visible = false

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		label.visible = true
		if panel:
			panel.visible = true
		GameManager.post_notification(message)
		GameManager.post_tutorial(message)

func _on_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		label.visible = false
		if panel:
			panel.visible = false
		GameManager.hide_tutorial()
