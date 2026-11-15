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
@onready var cd_void_cannon: TextureProgressBar = $AbilitiesBar/SlotVoidCannon/CDProgress if has_node("AbilitiesBar/SlotVoidCannon/CDProgress") else null
@onready var cd_shadow_step: TextureProgressBar = $AbilitiesBar/SlotShadowStep/CDProgress if has_node("AbilitiesBar/SlotShadowStep/CDProgress") else null

@onready var lock_lightning: TextureRect = $AbilitiesBar/SlotLightning/LockOverlay
@onready var lock_shield: TextureRect = $AbilitiesBar/SlotShield/LockOverlay
@onready var lock_void_cannon: TextureRect = $AbilitiesBar/SlotVoidCannon/LockOverlay if has_node("AbilitiesBar/SlotVoidCannon/LockOverlay") else null
@onready var lock_shadow_step: TextureRect = $AbilitiesBar/SlotShadowStep/LockOverlay if has_node("AbilitiesBar/SlotShadowStep/LockOverlay") else null

# Boss bar
@onready var boss_container: VBoxContainer = $BossContainer
@onready var boss_name_label: Label = $BossContainer/BossNameLabel
@onready var boss_bar: TextureProgressBar = $BossContainer/BossBar

# Toast
@onready var toast_label: Label = $ToastLabel
@onready var tutorial_box: Control = $TutorialBox if has_node("TutorialBox") else null
@onready var tutorial_message: Label = $TutorialBox/VBox/Message if has_node("TutorialBox/VBox/Message") else null

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
	GameManager.tutorial_posted.connect(_on_tutorial_posted)
	GameManager.tutorial_cleared.connect(_on_tutorial_cleared)
	GameManager.boss_spawned.connect(_on_boss_spawned)
	GameManager.boss_health_changed.connect(_on_boss_hp_changed)
	GameManager.boss_defeated.connect(_on_boss_defeated)

	boss_container.visible = false
	toast_label.visible = false
	if tutorial_box:
		tutorial_box.visible = false
	
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
	if lock_void_cannon:
		lock_void_cannon.visible = not GameManager.unlocked_powers.get("void_cannon", false)
	if lock_shadow_step:
		lock_shadow_step.visible = not GameManager.unlocked_powers.get("shadow_step", false)

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

	if cd_void_cannon and player_ref.cooldowns.has("void_cannon"):
		var vc_cd = player_ref.cooldowns["void_cannon"]
		var vc_max = GameManager.ABILITY_DATA["void_cannon"]["cooldown"]
		cd_void_cannon.value = (vc_cd / vc_max) * 100.0 if vc_cd > 0 else 0.0

	if cd_shadow_step and player_ref.cooldowns.has("shadow_step"):
		var ss_cd = player_ref.cooldowns["shadow_step"]
		var ss_max = GameManager.ABILITY_DATA["shadow_step"]["cooldown"]
		cd_shadow_step.value = (ss_cd / ss_max) * 100.0 if ss_cd > 0 else 0.0

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

func _on_tutorial_posted(text: String) -> void:
	if tutorial_box and tutorial_message:
		tutorial_message.text = text
		tutorial_box.visible = true
		tutorial_box.modulate.a = 0.0
		var tween = create_tween()
		tween.tween_property(tutorial_box, "modulate:a", 1.0, 0.2)

func _on_tutorial_cleared() -> void:
	if tutorial_box and tutorial_box.visible:
		var tween = create_tween()
		tween.tween_property(tutorial_box, "modulate:a", 0.0, 0.2)
		await tween.finished
		if is_instance_valid(tutorial_box):
			tutorial_box.visible = false
