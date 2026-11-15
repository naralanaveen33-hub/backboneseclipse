extends ColorRect

# CRT Overlay - scanlines and vignette for retro pixelated look
var scanline_intensity: float = 0.15
var vignette_intensity: float = 0.3

func _ready() -> void:
	# Full screen overlay
	set_anchors_preset(Control.PRESET_FULL_RECT)
	modulate = Color(0, 0, 0, 0.08)

func _process(_delta: float) -> void:
	# Subtle pulsing scanline intensity
	var time = Time.get_ticks_msec() / 1000.0
	scanline_intensity = 0.12 + 0.05 * sin(time * 3.0)
	modulate.a = 0.06 + 0.04 * sin(time * 2.0)