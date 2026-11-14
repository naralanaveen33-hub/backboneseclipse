extends CanvasLayer

class_name BossHealthBarUI

@onready var container: VBoxContainer = $VBoxContainer
@onready var title_label: Label = $VBoxContainer/TitleLabel
@onready var phase_label: Label = $VBoxContainer/PhaseLabel
@onready var hp_bar: TextureProgressBar = $VBoxContainer/BarContainer/HPBar
@onready var hp_text: Label = $VBoxContainer/BarContainer/HPText

var current_phase: int = 1

func setup(b_name: String, max_hp: float) -> void:
	title_label.text = b_name
	hp_bar.max_value = max_hp
	hp_bar.value = max_hp
	update_hp(max_hp, max_hp)
	set_phase(1)
	visible = true

func update_hp(cur_hp: float, max_hp: float) -> void:
	hp_bar.max_value = max_hp
	var tween = create_tween()
	tween.tween_property(hp_bar, "value", cur_hp, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	var pct = (cur_hp / max_hp) * 100.0
	hp_text.text = "%d / %d HP (%.1f%%)" % [int(cur_hp), int(max_hp), pct]

func set_phase(phase: int) -> void:
	current_phase = phase
	match phase:
		1:
			phase_label.text = "✦ PHASE 1: DORMANT SINGULARITY ✦"
			phase_label.modulate = Color(0.7, 0.5, 1.0)
			hp_bar.modulate = Color(0.65, 0.4, 0.95) # Deep Violet
		2:
			phase_label.text = "⚡ PHASE 2: SUPER SPEED & VOID SURGE ⚡"
			phase_label.modulate = Color(1.0, 0.4, 0.5)
			hp_bar.modulate = Color(0.95, 0.25, 0.4) # Crimson Void
		3:
			phase_label.text = "🌀 PHASE 3: TELEPORT AMBUSH & COMBOS 🌀"
			phase_label.modulate = Color(0.3, 0.9, 1.0)
			hp_bar.modulate = Color(0.2, 0.75, 1.0) # Astral Electric Cyan
		4:
			phase_label.text = "🔥 PHASE 4: ULTIMATE APOCALYPTIC RAGE 🔥"
			phase_label.modulate = Color(1.0, 0.85, 0.2)
			hp_bar.modulate = Color(1.5, 0.9, 0.2) # Solar Gold Overdrive

func hide_bar() -> void:
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 1.0)
	await tween.finished
	visible = false
