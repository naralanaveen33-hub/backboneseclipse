extends SceneTree

func _init() -> void:
	print("--- STARTING MYSTIC REALMS AUTOMATED VERIFICATION ---")
	
	# Ensure Autoloads are attached if running via standalone script
	var gm_class = load("res://scripts/systems/game_manager.gd")
	var sm_class = load("res://scripts/systems/sound_manager.gd")
	
	var gm = root.get_node_or_null("GameManager")
	if not gm:
		gm = gm_class.new()
		gm.name = "GameManager"
		root.add_child(gm)
		
	var sm = root.get_node_or_null("SoundManager")
	if not sm:
		sm = sm_class.new()
		sm.name = "SoundManager"
		root.add_child(sm)

	# Test 1: GameManager
	print("[1/6] Testing GameManager Systems...")
	assert(gm != null, "GameManager singleton must exist")
	gm.player_hp = 100.0
	assert(gm.player_hp == 100.0, "Player HP should be 100")
	var damaged = gm.take_damage(20.0)
	assert(damaged == true, "Damage should be applied")
	assert(gm.player_hp == 80.0, "Player HP should be 80 after 20 damage")
	gm.heal(10.0)
	assert(gm.player_hp == 90.0, "Player HP should be 90 after heal")
	
	# Test Mana
	var mana_used = gm.consume_mana(25.0)
	assert(mana_used == true, "Should consume 25 mana")
	assert(gm.player_mp == 75.0, "Mana should be 75")
	
	# Test Crystals
	var initial_crys = gm.crystals
	gm.add_crystals(5)
	assert(gm.crystals == initial_crys + 5, "Crystals count should increase by 5")
	
	# Test Unlocking powers
	gm.unlock_power("lightning")
	assert(gm.unlocked_powers["lightning"] == true, "Lightning should be unlocked")
	gm.unlock_power("shield")
	assert(gm.unlocked_powers["shield"] == true, "Shield should be unlocked")
	
	# Test 2: SoundManager
	print("[2/6] Testing SoundManager...")
	assert(sm != null, "SoundManager singleton must exist")
	sm.play_sfx("jump")
	sm.play_sfx("fireball")
	sm.play_sfx("crystal")
	
	# Test 3: Player & Spells
	print("[3/6] Testing Player and Spells...")
	var player_scene = load("res://scenes/player/player.tscn")
	assert(player_scene != null, "Player scene must load")
	var player = player_scene.instantiate()
	root.add_child(player)
	player.global_position = Vector2(100, 100)
	assert(player.is_in_group("player"), "Player must be in 'player' group")
	
	# Test Taking damage
	player.take_damage(30.0, Vector2(50, 100))
	assert(gm.player_hp == 60.0, "Player HP should be 60 after 30 damage")
	
	# Test Fireball scene
	var fb_scene = load("res://scenes/abilities/fireball.tscn")
	var fb = fb_scene.instantiate()
	root.add_child(fb)
	assert(fb != null, "Fireball must instantiate")
	fb.queue_free()
	
	# Test Ice Blast scene
	var ib_scene = load("res://scenes/abilities/ice_blast.tscn")
	var ib = ib_scene.instantiate()
	root.add_child(ib)
	assert(ib != null, "Ice blast must instantiate")
	ib.queue_free()
	
	# Test Lightning Strike scene
	var lt_scene = load("res://scenes/abilities/lightning_strike.tscn")
	var lt = lt_scene.instantiate()
	root.add_child(lt)
	assert(lt != null, "Lightning strike must instantiate")
	lt.queue_free()
	
	# Test Magic Shield scene
	var sh_scene = load("res://scenes/abilities/magic_shield.tscn")
	var sh = sh_scene.instantiate()
	player.add_child(sh)
	assert(gm.shield_active == true, "Shield should be active")
	
	# Test damage absorption by shield
	var blocked = gm.take_damage(50.0)
	assert(blocked == false, "Shield must block damage completely")
	assert(gm.player_hp == 60.0, "Player HP should not change when shield is active")
	sh.queue_free()
	gm.shield_active = false
	
	# Test 4: Enemies & Freeze mechanics
	print("[4/6] Testing Enemies and AI...")
	var sm_scene = load("res://scenes/enemies/shadow_monster.tscn")
	var sm_inst = sm_scene.instantiate()
	root.add_child(sm_inst)
	assert(sm_inst.hp == sm_inst.max_hp, "Shadow monster should have full HP")
	sm_inst.take_damage(25.0)
	assert(sm_inst.hp == sm_inst.max_hp - 25.0, "Shadow monster HP should decrease by 25")
	sm_inst.freeze_enemy(3.0)
	assert(sm_inst.is_frozen == true, "Shadow monster should be frozen")
	sm_inst.unfreeze()
	assert(sm_inst.is_frozen == false, "Shadow monster should be unfrozen")
	sm_inst.queue_free()
	
	# Test Bat
	var bat_scene = load("res://scenes/enemies/flying_bat.tscn")
	var bat = bat_scene.instantiate()
	root.add_child(bat)
	assert(bat.is_in_group("enemies"), "Bat must be in enemies group")
	bat.queue_free()
	
	# Test Fire Demon
	var fd_scene = load("res://scenes/enemies/fire_demon.tscn")
	var fd = fd_scene.instantiate()
	root.add_child(fd)
	assert(fd.is_in_group("enemies"), "Fire Demon must be in enemies group")
	fd.queue_free()
	
	# Test Bosses
	var bm_scene = load("res://scenes/enemies/boss_mini.tscn")
	var bm = bm_scene.instantiate()
	root.add_child(bm)
	assert(bm.hp == 250.0, "Mini Boss must have 250 HP")
	bm.queue_free()
	
	var dw_scene = load("res://scenes/enemies/boss_dark_wizard.tscn")
	var dw = dw_scene.instantiate()
	root.add_child(dw)
	assert(dw.hp == 500.0, "Dark Wizard Boss must have 500 HP")
	dw.queue_free()
	
	# Test 5: Checkpoints & Respawn
	print("[5/6] Testing Checkpoint and Respawn System...")
	var chk_scene = load("res://scenes/objects/checkpoint.tscn")
	var chk = chk_scene.instantiate()
	root.add_child(chk)
	chk.global_position = Vector2(500, 300)
	gm.set_checkpoint(Vector2(500, 300))
	assert(gm.has_checkpoint == true, "Checkpoint should be set")
	assert(gm.active_checkpoint_pos == Vector2(500, 300), "Checkpoint pos should match")
	
	# Kill player
	gm.take_damage(100.0)
	assert(gm.is_game_over == true, "Game over should be true on death")
	
	# Respawn
	gm.respawn_player()
	assert(gm.is_game_over == false, "Game over should be false after respawn")
	assert(gm.player_hp == 100.0, "Player HP should be restored to 100")
	assert(gm.player_mp == 100.0, "Player MP should be restored to 100")
	assert(gm.unlocked_powers["lightning"] == true, "Unlocked powers must be preserved")
	
	player.queue_free()
	chk.queue_free()
	
	# Test 6: Levels
	print("[6/6] Testing Levels...")
	var lvl1 = load("res://scenes/levels/level_1.tscn")
	assert(lvl1 != null, "Level 1 scene must load successfully")
	var lvl2 = load("res://scenes/levels/level_2.tscn")
	assert(lvl2 != null, "Level 2 scene must load successfully")
	
	print("--- ALL 6 SYSTEM TESTS PASSED SUCCESSFULLY! ---")
	quit(0)
