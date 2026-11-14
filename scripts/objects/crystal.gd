extends Area2D

var bob_time: float = 0.0
var base_y: float = 0.0
var collected: bool = false

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
	base_y = position.y
	bob_time = randf_range(0.0, 3.0)
	anim.play("spin")

func _process(delta: float) -> void:
	if not collected:
		bob_time += delta
		position.y = base_y + sin(bob_time * 3.5) * 4.0

func _on_body_entered(body: Node2D) -> void:
	if collected:
		return
	if body.is_in_group("player"):
		collected = true
		GameManager.add_crystals(1)
		
		# Collect float up & fade
		var tween = create_tween()
		tween.tween_property(self, "position:y", position.y - 24.0, 0.25)
		tween.parallel().tween_property(self, "modulate:a", 0.0, 0.25)
		await tween.finished
		queue_free()
