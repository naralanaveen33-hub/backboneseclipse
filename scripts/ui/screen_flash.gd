extends ColorRect

# Screen Flash - flashes the screen white/red on damage, gold on victory, etc.
var flash_duration: float = 0.0
var flash_color: Color = Color.WHITE
var flash_intensity: float = 1.0

func _process(delta: float) -> void:
	if flash_duration > 0.0:
		flash_duration -= delta
		var t = clamp(flash_duration / 0.2, 0.0, 1.0)
		modulate = flash_color.lerp(Color(1, 1, 1, 0), t)
		modulate.a *= flash_intensity

func trigger_flash(color: Color = Color.WHITE, duration: float = 0.15, intensity: float = 1.0) -> void:
	flash_color = color
	flash_duration = duration
	flash_intensity = intensity
	modulate = color
	modulate.a = intensity
	visible = true