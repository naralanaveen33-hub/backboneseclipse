extends CanvasLayer

@onready var hp_bar: TextureProgressBar = $HUDPanel/VBoxBars/HPBar
@onready var hp_label: Label = $HUDPanel/VBoxBars/HPBar/HPLabel
@onready var mp_bar: TextureProgressBar = $HUDPanel/VBoxBars/MPBar
@onready var mp_label: Label = $HUDPanel/VBoxBars/MPBar/MPLabel
@onready var rebound_bar: TextureProgressBar = $HUDPanel/VBoxBars/ReboundBar
@onready var rebound_label: Label = $HUDPanel/VBoxBars/ReboundBar/ReboundLabel
@onready var crystal_label: Label = $HUDPanel/HBoxCrystals/CrystalLabel

# Abilities
@onready var cd_fireball: TextureProgressBar = $AbilitiesBar/SlotFireball/CDProgress
@onready var cd_ice: TextureProgressBar = $AbilitiesBar/SlotIce/CDProgress
@onready var cd_lightning: TextureProgressBar = $AbilitiesBar/SlotLightning/CDProgress
@onready var cd_shield: TextureProgressBar = $AbilitiesBar/SlotShield/CDProgress

@onready var lock_lightning: TextureRect = $AbilitiesBar/SlotLightning/LockOverlay
@onready var lock_shield: TextureRect = $AbilitiesBar/SlotShield/LockOverlay

# Boss bar
@onready var boss_container: VBoxContainer = $BossContainer
@onready var boss_name_label: Label = $BossContainer/BossNameLabel
@onready var boss_bar: TextureProgressBar = $BossContainer/BossBar

# Toast
@onready var toast_label: Label = $ToastLabel

var player_ref: Player = null

func _ready() -> void:
	GameManager.player_health_changed.connect(_on_hp_changed)
	GameManager.player_mana_changed.connect(_on_mp_changed)
	GameManager.rebound_changed.connect(_on_rebound_changed)
	GameManager.overdrive_started.connect(_on_overdrive_started)
	GameManager.overdrive_ended.connect(_on_overdrive_ended)
	GameManager.crystals_changed.connect(_on_crystals_changed)
	GameManager.power_unlocked.connect(_on_power_unlocked)
	GameManager.notification_posted.connect(_on_notification)
	GameManager.boss_spawned.connect(_on_boss_spawned)
	GameManager.boss_health_changed.connect(_on_boss_hp_changed)
	GameManager.boss_defeated.connect(_on_boss_defeated)

	boss_container.visible = false
	toast_label.visible = false
	
	_on_hp_changed(GameManager.player_hp, GameManager.player_max_hp)
	_on_mp_changed(GameManager.player_mp, GameManager.player_max_mp)
	_on_rebound_changed(GameManager.rebound_meter, GameManager.MAX_REBOUND)
	_on_crystals_changed(GameManager.crystals)
	_update_locks()

func _process(_delta: float) -> void:
	if not player_ref:
		player_ref = get_tree().get_first_node_in_group("player") as Player
	if player_ref:
		_update_cooldown_visuals()
		
	if GameManager.is_overdrive:
		rebound_bar.value = (GameManager.overdrive_timer / 5.0) * 100.0
		rebound_label.text = "OVERDRIVE: %.1fs (5x)" % GameManager.overdrive_timer

func _update_locks() -> void:
	lock_lightning.visible = not GameManager.unlocked_powers.get("lightning", false)
	lock_shield.visible = not GameManager.unlocked_powers.get("shield", false)

func _update_cooldown_visuals() -> void:
	var fb_cd = player_ref.cooldowns["fireball"]
	var fb_max = 0.10 if GameManager.is_overdrive else GameManager.ABILITY_DATA["fireball"]["cooldown"]
	cd_fireball.value = (fb_cd / fb_max) * 100.0 if fb_cd > 0 else 0.0

	var ice_cd = player_ref.cooldowns["ice_blast"]
	var ice_max = GameManager.ABILITY_DATA["ice_blast"]["cooldown"]
	cd_ice.value = (ice_cd / ice_max) * 100.0 if ice_cd > 0 else 0.0

	var light_cd = player_ref.cooldowns["lightning"]
	var light_max = GameManager.ABILITY_DATA["lightning"]["cooldown"]
	cd_lightning.value = (light_cd / light_max) * 100.0 if light_cd > 0 else 0.0

	var sh_cd = player_ref.cooldowns["shield"]
	var sh_max = GameManager.ABILITY_DATA["shield"]["cooldown"]
	cd_shield.value = (sh_cd / sh_max) * 100.0 if sh_cd > 0 else 0.0

func _on_hp_changed(hp: float, max_hp: float) -> void:
	hp_bar.max_value = max_hp
	hp_bar.value = hp
	hp_label.text = "HP: %d / %d" % [int(hp), int(max_hp)]

func _on_mp_changed(mp: float, max_mp: float) -> void:
	mp_bar.max_value = max_mp
	mp_bar.value = mp
	mp_label.text = "MP: %d / %d" % [int(mp), int(max_mp)]

func _on_rebound_changed(current_val: float, max_val: float) -> void:
	if GameManager.is_overdrive:
		return
	rebound_bar.max_value = max_val
	rebound_bar.value = current_val
	if current_val >= max_val:
		rebound_label.text = "REBOUND READY! [Q]"
		rebound_bar.modulate = Color(1.3, 1.2, 0.4)
	else:
		rebound_label.text = "REBOUND: %d%%" % int((current_val / max_val) * 100.0)
		rebound_bar.modulate = Color.WHITE

func _on_overdrive_started() -> void:
	rebound_bar.modulate = Color(1.4, 1.2, 0.3)

func _on_overdrive_ended() -> void:
	rebound_bar.modulate = Color.WHITE
	_on_rebound_changed(GameManager.rebound_meter, GameManager.MAX_REBOUND)

func _on_crystals_changed(count: int) -> void:
	crystal_label.text = "x %d" % count

func _on_power_unlocked(_p_name: String) -> void:
	_update_locks()

func _on_boss_spawned(b_name: String, max_hp: float) -> void:
	boss_container.visible = true
	boss_name_label.text = b_name
	boss_bar.max_value = max_hp
	boss_bar.value = max_hp

func _on_boss_hp_changed(cur_hp: float, max_hp: float) -> void:
	boss_bar.max_value = max_hp
	boss_bar.value = cur_hp

func _on_boss_defeated() -> void:
	boss_container.visible = false

func _on_notification(text: String) -> void:
	toast_label.text = text
	toast_label.visible = true
	toast_label.modulate.a = 1.0
	var tween = create_tween()
	tween.tween_interval(2.5)
	tween.tween_property(toast_label, "modulate:a", 0.0, 0.5)
	await tween.finished
	toast_label.visible = false
