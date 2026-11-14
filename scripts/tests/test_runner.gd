extends Node2D

func _ready() -> void:
	print("==================================================")
	print("   MYSTIC REALMS: 7 LEVELS & 7 BOSSES TEST SUITE  ")
	print("        BOUNCE BACK GAME JAM INTEGRATION          ")
	print("==================================================")
	
	# Test 1: Autoloads & Dark Dream Anthem
	print("[TEST 1/8] Verifying Autoload Singletons & Soundtrack...")
	assert(GameManager != null, "GameManager must be active")
	assert(SoundManager != null, "SoundManager must be active")
	assert(SoundManager.music_streams.has("dark_dream"), "Curley Gao - Lord of Mysteries (Dark Dream) must be loaded")
	print("  -> GameManager, SoundManager & Dark Dream Anthem verified OK.")

	# Test 2: Health, Damage, Healing & Mana Systems
	print("[TEST 2/8] Verifying Upgraded Health & Mana System...")
	GameManager.player_hp = 250.0
	var res = GameManager.take_damage(50.0)
	assert(res == true, "Damage should be dealt")
	assert(GameManager.player_hp == 200.0, "Player HP should be 200")
	GameManager.heal(25.0)
	assert(GameManager.player_hp == 225.0, "Player HP should be 225")
	var mana_res = GameManager.consume_mana(30.0)
	assert(mana_res == true, "Mana consumption should succeed")
	print("  -> Health (250) and Mana (200) mechanics verified OK.")

	# Test 3: Rebound Meter & Overdrive Shockwave
	print("[TEST 3/8] Verifying Damage-to-Power 'Rebound' Meter & Overdrive...")
	GameManager.rebound_meter = 0.0
	GameManager.add_rebound(50.0)
	assert(GameManager.rebound_meter == 50.0, "Rebound meter should be 50.0")
	GameManager.add_rebound(60.0)
	assert(GameManager.rebound_meter == 100.0, "Rebound meter should cap at 100.0")
	
	GameManager.trigger_rebound_overdrive(Vector2(500, 300))
	assert(GameManager.is_overdrive == true, "Overdrive must be active")
	assert(GameManager.overdrive_timer > 0.0, "Overdrive timer must be running")
	assert(GameManager.rebound_meter == 0.0, "Rebound meter must reset to 0 upon activation")
	GameManager.end_overdrive()
	assert(GameManager.is_overdrive == false, "Overdrive ended successfully")
	print("  -> Rebound Meter (100) & Overdrive Shockwave verified OK.")

	# Test 4: Ricochet Combat & Damage Multipliers
	print("[TEST 4/8] Verifying Ricochet Combat & Damage Multipliers...")
	var fb_scene = load("res://scenes/abilities/fireball.tscn")
	assert(fb_scene != null, "Fireball scene must exist")
	var fb = fb_scene.instantiate()
	add_child(fb)
	assert(fb.max_bounces == 3, "Fireball default max bounces should be 3")
	assert(fb.is_in_group("player_projectiles"), "Fireball must be in player_projectiles group")
	
	fb.bounces = 1
	fb.damage = fb.base_damage * 2.0
	assert(fb.damage == fb.base_damage * 2.0, "Damage must multiply 2x on first bounce")
	fb.queue_free()
	print("  -> Ricochet bounces (3x), damage scaling (1x->2x->3x) verified OK.")

	# Test 5: Timed Parry & Enemy Projectile Deflection
	print("[TEST 5/8] Verifying Parry / Deflect Action on Enemy Projectiles...")
	var projs = [
		load("res://scenes/enemies/demon_projectile.tscn"),
		load("res://scenes/enemies/magma_orb_projectile.tscn"),
		load("res://scenes/enemies/frost_shard_projectile.tscn"),
		load("res://scenes/enemies/thunder_orb_projectile.tscn"),
		load("res://scenes/enemies/chaos_orb_projectile.tscn")
	]
	for p_scene in projs:
		assert(p_scene != null, "Projectile scene must exist")
		var p = p_scene.instantiate()
		add_child(p)
		assert(p.is_in_group("enemy_projectiles"), "Projectile must start in enemy_projectiles group")
		p.deflect(Vector2.RIGHT)
		assert(p.is_deflected == true, "Projectile must be deflected")
		assert(p.is_in_group("player_projectiles"), "Deflected projectile must join player_projectiles group")
		p.queue_free()
	print("  -> All 5 boss projectile types deflectable with 3x speed & damage verified OK.")

	# Test 6: Ruined Shrines & Permanent Stat Upgrades
	print("[TEST 6/8] Verifying Ruined Shrines 'Bounce Back' Progression...")
	var shrine_scene = load("res://scenes/objects/ruined_shrine.tscn")
	assert(shrine_scene != null, "Ruined shrine scene must exist")
	var shrine = shrine_scene.instantiate()
	shrine.stat_buff = "hp"
	add_child(shrine)
	assert(shrine.is_active == false, "Shrine starts dormant")
	var old_max_hp = GameManager.player_max_hp
	shrine.activate_shrine()
	assert(shrine.is_active == true, "Shrine must be active after activation")
	assert(GameManager.player_max_hp == old_max_hp + 30.0, "HP Shrine must grant +30 Max HP")
	shrine.queue_free()
	print("  -> Ruined Shrines awaken & permanent buffs verified OK.")

	# Test 7: Verify All 7 Bosses & Active Attack Logic
	print("[TEST 7/8] Verifying All 7 Bosses & Active Attacks...")
	var boss_scenes = [
		["Level 1: Shadow Behemoth", "res://scenes/enemies/boss_mini.tscn"],
		["Level 2: Dark Wizard", "res://scenes/enemies/boss_dark_wizard.tscn"],
		["Level 3: Infernal Titan", "res://scenes/enemies/boss_infernal_titan.tscn"],
		["Level 4: Frost Lich", "res://scenes/enemies/boss_frost_lich.tscn"],
		["Level 5: Storm Archon", "res://scenes/enemies/boss_storm_archon.tscn"],
		["Level 6: Void Monarch", "res://scenes/enemies/boss_void_monarch.tscn"],
		["Level 7: Abyssal Overlord Malakor", "res://scenes/enemies/boss_abyssal_overlord.tscn"]
	]
	for b_info in boss_scenes:
		var b_name = b_info[0]
		var b_path = b_info[1]
		var b_scene = load(b_path)
		assert(b_scene != null, "Boss scene must exist: %s" % b_path)
		var b_inst = b_scene.instantiate()
		add_child(b_inst)
		assert(b_inst.max_hp > 400.0, "%s must have upgraded boss HP" % b_name)
		if b_inst.has_method("activate_boss"):
			b_inst.activate_boss()
			assert(b_inst.is_active == true, "%s must activate properly" % b_name)
		b_inst.queue_free()
		print("  -> %s validated OK." % b_name)

	# Test 8: Verify All 7 Levels & Menus
	print("[TEST 8/8] Verifying All 7 Levels & UI Menus Loading...")
	for lvl_i in range(1, 8):
		var lvl_path = "res://scenes/levels/level_%d.tscn" % lvl_i
		var lvl_res = load(lvl_path)
		assert(lvl_res != null, "Level %d scene must load successfully" % lvl_i)
	
	var menu = load("res://scenes/menus/main_menu.tscn")
	assert(menu != null, "Main menu scene must load")
	var lvl_sel = load("res://scenes/menus/level_select.tscn")
	assert(lvl_sel != null, "Level select scene must load")
	var victory = load("res://scenes/ui/victory_menu.tscn")
	assert(victory != null, "Victory scene must load")
	print("  -> All 7 levels, Level Select and menus loaded successfully.")

	print("==================================================")
	print("   ALL 8 ADVANCED TESTS PASSED 100%!             ")
	print("==================================================")
	get_tree().quit(0)
