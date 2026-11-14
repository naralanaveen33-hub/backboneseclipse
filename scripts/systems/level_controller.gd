extends Node2D

@export var level_number: int = 1
@export var music_track: String = "dark_dream"
@export var death_y: float = 650.0

@onready var player: Player = $Player
var boss_barrier_left: StaticBody2D = null
var boss_barrier_right: StaticBody2D = null

func _ready() -> void:
	GameManager.current_level = level_number
	# Always ensure Curley Gao - Lord of Mysteries: Dark Dream is playing!
	SoundManager.play_music("dark_dream")
	
	# Show "BOUNCE BACK" starting intro banner for the level
	_show_bounce_back_intro()
	
	if has_node("BossArena/BarrierLeft"):
		boss_barrier_left = get_node("BossArena/BarrierLeft")
		boss_barrier_left.get_node("CollisionShape2D").set_deferred("disabled", true)
	if has_node("BossArena/BarrierRight"):
		boss_barrier_right = get_node("BossArena/BarrierRight")
		boss_barrier_right.get_node("CollisionShape2D").set_deferred("disabled", true)
		
	GameManager.boss_spawned.connect(_on_boss_started)
	GameManager.boss_defeated.connect(_on_boss_finished)

func _physics_process(_delta: float) -> void:
	if player and not player.is_dead:
		if player.global_position.y > death_y:
			player.take_damage(50.0, player.global_position)
			if not player.is_dead:
				player.global_position = GameManager.active_checkpoint_pos

func _show_bounce_back_intro() -> void:
	var canvas = CanvasLayer.new()
	canvas.layer = 90
	add_child(canvas)
	
	var bg = ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.04, 0.03, 0.08, 0.90)
	canvas.add_child(bg)
	
	var vbox = VBoxContainer.new()
	vbox.set_anchors_preset(Control.PRESET_CENTER)
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 12)
	canvas.add_child(vbox)
	
	var titles = {
		1: "⚡ BOUNCE BACK: FROM ASHES TO POWER (LEVEL 1) ⚡",
		2: "⚡ BOUNCE BACK: THE DARK CASTLE (LEVEL 2) ⚡",
		3: "⚡ BOUNCE BACK: THE MOLTEN CAVERNS (LEVEL 3) ⚡",
		4: "⚡ BOUNCE BACK: THE FROZEN CRYPTS (LEVEL 4) ⚡",
		5: "⚡ BOUNCE BACK: THE TEMPEST SPIRE (LEVEL 5) ⚡",
		6: "⚡ BOUNCE BACK: THE ASTRAL VOID (LEVEL 6) ⚡",
		7: "⚡ BOUNCE BACK: THE ABYSSAL THRONE — FINAL BATTLE (LEVEL 7) ⚡",
		8: "👑 BOUNCE BACK: PRIMORDIAL SINGULARITY CORE — ULTIMATE BOSS (LEVEL 8) 👑"
	}
	
	var missions = {
		1: "Stripped of your legendary relics by the Abyssal Overlord...\nAwaken from the lowest abyss and fight back to the surface!",
		2: "Infiltrate the Dark Castle and confront the Dark Wizard - Lord of Shadows!\nBeware of molten lava pits and hidden spike traps.",
		3: "Descend into the Molten Inferno and defeat the Infernal Magma Titan!\nSurvive deadly lava geysers and burning magma orbs.",
		4: "Brave the permafrost of the Frozen Crypts to slay the Frost Lich Sovereign!\nFreezing winds slow your advance.",
		5: "Ascend the electric heights of the Tempest Spire and conquer the Storm Thunder Archon!\nRide the thunder gale.",
		6: "Enter the cosmic Sanctum of the Mysteries and defeat the Celestial Void Monarch!\nDimensions unravel around you.",
		7: "THE SUPREME FINAL SHOWDOWN! Defeat Abyssal Overlord Malakor\nand reclaim the Stolen Celestial Relic once and for all!",
		8: "THE TRUE COSMIC APOCALYPSE! Confront Primordial Void Emperor Malakor!\n50,000 HP • 4 Multi-Phase Transformations • Supersonic Dashes • Stun Waves • Ultimate Rage Mode!"
	}
	
	var tips = {
		1: "THEME TIP: Fireballs ricochet off walls (1x->2x->3x DMG)! Right-Click / [Shift] to Parry!",
		2: "THEME TIP: Timed Parry deflects dark orbs at 3x speed & stun! Awaken Ruined Shrines for buffs!",
		3: "THEME TIP: Aim downward with mouse or hold [S] to Rocket-Jump over bottomless lava pits!",
		4: "THEME TIP: Deflect the Frost Lich's shards back into him to freeze him in place!",
		5: "THEME TIP: Near-misses charge your Rebound Meter! Press [Q] at 100% for 5s Overdrive!",
		6: "THEME TIP: Overdrive gives 5-bounce mega ricochets and machine-gun cast rates!",
		7: "THEME TIP: Chain Parry Deflections and Rebound Shockwaves to conquer the Overlord!",
		8: "THEME TIP: Timed Parry deflects Dark Orbs for 3x damage! Jump over Ground Waves! Crack his Shield with Ricochet Spells!"
	}
	
	var title = Label.new()
	title.text = titles.get(level_number, "⚡ BOUNCE BACK: THE MYSTIC REALMS ⚡")
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var t_set = LabelSettings.new()
	t_set.font_size = 20
	t_set.font_color = Color(1.0, 0.85, 0.2)
	t_set.outline_size = 4
	t_set.outline_color = Color(0.1, 0.05, 0.15)
	title.label_settings = t_set
	vbox.add_child(title)
	
	var desc = Label.new()
	desc.text = missions.get(level_number, "Explore the level, fight enemies, and bounce back to victory!")
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var d_set = LabelSettings.new()
	d_set.font_size = 14
	d_set.font_color = Color(0.85, 0.9, 1.0)
	d_set.outline_size = 2
	d_set.outline_color = Color(0, 0, 0)
	desc.label_settings = d_set
	vbox.add_child(desc)
	
	var tip = Label.new()
	tip.text = tips.get(level_number, "BOUNCE BACK: Ricochet spells and parry enemy attacks!")
	tip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var tip_set = LabelSettings.new()
	tip_set.font_size = 14
	tip_set.font_color = Color(0.3, 1.0, 0.5)
	tip_set.outline_size = 3
	tip_set.outline_color = Color(0, 0, 0)
	tip.label_settings = tip_set
	vbox.add_child(tip)
	
	var hint = Label.new()
	hint.text = "[Press Space or Click to continue]"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var h_set = LabelSettings.new()
	h_set.font_size = 12
	h_set.font_color = Color(0.7, 0.7, 0.8)
	hint.label_settings = h_set
	vbox.add_child(hint)
	
	SoundManager.play_sfx("checkpoint")
	
	# Auto fade out after 2.6 seconds or skip on click
	var tween = create_tween()
	tween.tween_interval(2.2)
	tween.tween_property(bg, "modulate:a", 0.0, 0.5)
	tween.parallel().tween_property(vbox, "modulate:a", 0.0, 0.5)
	tween.tween_callback(canvas.queue_free)
	
	bg.gui_input.connect(func(ev):
		if ev is InputEventMouseButton and ev.pressed:
			if is_instance_valid(canvas):
				canvas.queue_free()
	)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("jump") or event.is_action_pressed("fireball"):
		for c in get_children():
			if c is CanvasLayer and c.layer == 90:
				c.queue_free()

func _on_boss_started(_name: String, _max_hp: float) -> void:
	if boss_barrier_left:
		boss_barrier_left.get_node("CollisionShape2D").set_deferred("disabled", false)
	if boss_barrier_right:
		boss_barrier_right.get_node("CollisionShape2D").set_deferred("disabled", false)

func _on_boss_finished() -> void:
	if boss_barrier_left:
		boss_barrier_left.get_node("CollisionShape2D").set_deferred("disabled", true)
	if boss_barrier_right:
		boss_barrier_right.get_node("CollisionShape2D").set_deferred("disabled", true)
