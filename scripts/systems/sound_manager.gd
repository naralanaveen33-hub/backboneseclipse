extends Node

var sfx_streams = {}
var music_streams = {}

var music_player: AudioStreamPlayer
var current_music_track: String = ""

# SFX player pool to allow concurrent sounds without cutting off
var sfx_players: Array[AudioStreamPlayer] = []
const SFX_POOL_SIZE = 16
var sfx_pool_index: int = 0

var sfx_volume: float = 1.0
var music_volume: float = 0.9

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_setup_audio_players()
	_load_audio_resources()
	# Start Dark Dream as the main anthem for the entire game
	play_music("dark_dream")

func _setup_audio_players() -> void:
	# Music Player
	music_player = AudioStreamPlayer.new()
	music_player.bus = "Master"
	music_player.volume_db = linear_to_db(music_volume)
	add_child(music_player)
	
	# SFX Pool
	for i in range(SFX_POOL_SIZE):
		var p = AudioStreamPlayer.new()
		p.bus = "Master"
		p.volume_db = linear_to_db(sfx_volume)
		add_child(p)
		sfx_players.append(p)

func _load_audio_resources() -> void:
	var sfx_names = [
		"jump", "land", "fireball", "explosion", "ice_blast", "freeze",
		"lightning", "shield", "shield_break", "hurt", "death", "respawn",
		"enemy_hurt", "enemy_death", "crystal", "checkpoint", "click",
		"boss_roar", "victory"
	]
	for sname in sfx_names:
		var path = "res://assets/sounds/%s.wav" % sname
		if ResourceLoader.exists(path):
			var stream = load(path)
			if stream is AudioStreamWAV:
				stream.loop_mode = AudioStreamWAV.LOOP_DISABLED
			sfx_streams[sname] = stream
			
	# Music streams
	var music_names = ["menu_theme", "forest_theme", "castle_theme", "boss_theme"]
	for mname in music_names:
		var path = "res://assets/music/%s.wav" % mname
		if ResourceLoader.exists(path):
			var stream = load(path)
			if stream is AudioStreamWAV:
				stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
			music_streams[mname] = stream

	# Load Lord of the Mysteries - Dark Dream MP3
	var dark_dream_path = "res://assets/music/dark_dream.mp3"
	if ResourceLoader.exists(dark_dream_path):
		var stream = load(dark_dream_path)
		if stream is AudioStreamMP3:
			stream.loop = true
		music_streams["dark_dream"] = stream

func play_sfx(sfx_name: String, pitch_range: float = 0.05) -> void:
	if not sfx_streams.has(sfx_name):
		return
	var stream = sfx_streams[sfx_name]
	var player = sfx_players[sfx_pool_index]
	sfx_pool_index = (sfx_pool_index + 1) % SFX_POOL_SIZE
	
	player.stream = stream
	player.volume_db = linear_to_db(sfx_volume)
	if pitch_range > 0:
		player.pitch_scale = randf_range(1.0 - pitch_range, 1.0 + pitch_range)
	else:
		player.pitch_scale = 1.0
	player.play()

func play_sfx_pitched(sfx_name: String, pitch: float = 1.0) -> void:
	if not sfx_streams.has(sfx_name):
		return
	var stream = sfx_streams[sfx_name]
	var player = sfx_players[sfx_pool_index]
	sfx_pool_index = (sfx_pool_index + 1) % SFX_POOL_SIZE
	
	player.stream = stream
	player.volume_db = linear_to_db(sfx_volume)
	player.pitch_scale = clampf(pitch, 0.4, 3.0)
	player.play()

func play_music(music_name: String = "dark_dream", _fade_in_time: float = 0.5) -> void:
	# If already playing this track, don't restart it
	if current_music_track == music_name and music_player.playing:
		return
		
	# Fallback to dark_dream if available
	var target = music_name
	if not music_streams.has(target):
		if music_streams.has("dark_dream"):
			target = "dark_dream"
		else:
			return

	current_music_track = target
	var stream = music_streams[target]
	music_player.stream = stream
	music_player.volume_db = linear_to_db(music_volume)
	music_player.play()

func stop_music() -> void:
	music_player.stop()
	current_music_track = ""

func set_sfx_volume(val: float) -> void:
	sfx_volume = clampf(val, 0.0, 1.0)
	for p in sfx_players:
		p.volume_db = linear_to_db(sfx_volume)

func set_music_volume(val: float) -> void:
	music_volume = clampf(val, 0.0, 1.0)
	music_player.volume_db = linear_to_db(music_volume)
