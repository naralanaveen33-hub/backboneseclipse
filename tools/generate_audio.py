import math
import struct
import wave
import os
import random

SAMPLE_RATE = 22050

def note_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def clamp(val, min_val=-1.0, max_val=1.0):
    return max(min_val, min(max_val, val))

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        # Normalize slightly if peak exceeds 0.95
        peak = max(abs(s) for s in samples) if samples else 1.0
        scale = 30000.0 / peak if peak > 0.95 else 30000.0
        frames = bytearray()
        for s in samples:
            val = int(clamp(s) * scale)
            frames.extend(struct.pack('<h', val))
        w.writeframes(frames)
    print(f"Generated: {filename} ({len(samples)/sample_rate:.2f}s)")

def env_adsr(t, duration, a=0.02, d=0.08, s=0.7, r=0.1):
    if t < 0: return 0.0
    if t > duration: return 0.0
    if t < a:
        return t / a
    t2 = t - a
    if t2 < d:
        return 1.0 - (1.0 - s) * (t2 / d)
    t3 = duration - t
    if t3 < r:
        return s * (t3 / r)
    return s

def synth_sfx(name, duration, func):
    n_samples = int(duration * SAMPLE_RATE)
    samples = [func(i / SAMPLE_RATE, duration) for i in range(n_samples)]
    save_wav(f"assets/sounds/{name}.wav", samples)

# Sound Effects Synthesis
def gen_sfx():
    # 1. Jump
    synth_sfx("jump", 0.22, lambda t, dur: 
        math.sin(2 * math.pi * (160 + 340 * (t/dur)**0.7) * t) * (1.0 - t/dur)**1.2 * 0.7
    )
    
    # 2. Land
    synth_sfx("land", 0.15, lambda t, dur:
        (math.sin(2 * math.pi * 85 * (1.0 - t/dur) * t) * 0.6 + (random.random()*2-1)*0.2) * (1.0 - t/dur)**2.0
    )
    
    # 3. Fireball cast
    synth_sfx("fireball", 0.35, lambda t, dur:
        (math.sin(2 * math.pi * (320 - 180 * (t/dur)) * t) * 0.4 +
         (random.random()*2-1) * (0.6 - 0.4 * (t/dur))) * (1.0 - t/dur)**0.8
    )
    
    # 4. Explosion
    synth_sfx("explosion", 0.55, lambda t, dur:
        (math.sin(2 * math.pi * (120 * (1.0 - t/dur)**2 + 35) * t) * 0.6 +
         (random.random()*2-1) * (0.8 * (1.0 - t/dur)**1.5)) * (1.0 - t/dur)
    )
    
    # 5. Ice blast
    synth_sfx("ice_blast", 0.3, lambda t, dur:
        (math.sin(2 * math.pi * (800 + 400 * math.sin(t * 30)) * t) * 0.4 +
         math.sin(2 * math.pi * (1200 + 300 * (t/dur)) * t) * 0.3 +
         (random.random()*2-1) * 0.2) * (1.0 - t/dur)**0.7
    )
    
    # 6. Freeze
    synth_sfx("freeze", 0.45, lambda t, dur:
        ((random.random()*2-1) * (0.5 if (int(t*60)%2==0) else 0.1) +
         math.sin(2 * math.pi * 1800 * t) * 0.3 * math.exp(-t * 8) +
         math.sin(2 * math.pi * 2400 * t) * 0.3 * math.exp(-t * 12)) * (1.0 - t/dur)
    )
    
    # 7. Lightning
    synth_sfx("lightning", 0.6, lambda t, dur:
        ((random.random()*2-1) * (1.0 if t < 0.12 else 0.4 * (1.0 - t/dur)**2) +
         (1.0 if math.sin(2*math.pi*90*t) > 0 else -1.0) * 0.3 * math.exp(-t*3) +
         math.sin(2 * math.pi * 60 * t) * 0.5 * (1.0 - t/dur)) * min(1.0, t*50)
    )
    
    # 8. Shield activate
    synth_sfx("shield", 0.5, lambda t, dur:
        (math.sin(2 * math.pi * (350 + 20 * math.sin(t * 25)) * t) * 0.4 +
         math.sin(2 * math.pi * (525 + 20 * math.sin(t * 25)) * t) * 0.3 +
         math.sin(2 * math.pi * (700 + 20 * math.sin(t * 25)) * t) * 0.2) * env_adsr(t, dur, 0.05, 0.1, 0.8, 0.2)
    )
    
    # 9. Shield break
    synth_sfx("shield_break", 0.4, lambda t, dur:
        ((random.random()*2-1) * 0.6 * math.exp(-t*10) +
         math.sin(2 * math.pi * 1200 * (1.0 - t/dur) * t) * 0.3) * (1.0 - t/dur)
    )
    
    # 10. Player hurt
    synth_sfx("hurt", 0.25, lambda t, dur:
        (math.sin(2 * math.pi * (260 - 160 * (t/dur)) * t) * 0.7 +
         (random.random()*2-1) * 0.3 * (1.0 - t/dur)) * (1.0 - t/dur)**1.2
    )
    
    # 11. Death
    synth_sfx("death", 0.8, lambda t, dur:
        (math.sin(2 * math.pi * (240 - 140 * (t/dur)**0.5) * t) * 0.5 +
         math.sin(2 * math.pi * (180 - 100 * (t/dur)**0.5) * t) * 0.3 +
         (random.random()*2-1) * 0.2 * (1.0 - t/dur)) * (1.0 - t/dur)**0.8
    )
    
    # 12. Respawn
    synth_sfx("respawn", 0.7, lambda t, dur:
        (math.sin(2 * math.pi * (261.63 if t < 0.14 else (329.63 if t < 0.28 else (392.0 if t < 0.42 else 523.25))) * t) * 0.5 +
         math.sin(2 * math.pi * 1046.5 * t) * 0.2 * math.sin(t * 20)) * env_adsr(t, dur, 0.04, 0.1, 0.7, 0.2)
    )
    
    # 13. Enemy hurt
    synth_sfx("enemy_hurt", 0.18, lambda t, dur:
        (math.sin(2 * math.pi * (380 - 220 * (t/dur)) * t) * 0.5 +
         (random.random()*2-1) * 0.4) * (1.0 - t/dur)**1.5
    )
    
    # 14. Enemy death
    synth_sfx("enemy_death", 0.35, lambda t, dur:
        ((random.random()*2-1) * 0.6 * (1.0 - t/dur)**1.3 +
         math.sin(2 * math.pi * (190 - 110 * (t/dur)) * t) * 0.4) * (1.0 - t/dur)
    )
    
    # 15. Crystal pickup
    synth_sfx("crystal", 0.35, lambda t, dur:
        (math.sin(2 * math.pi * (1318.51 if t < 0.12 else 1760.0) * t) * 0.5 +
         math.sin(2 * math.pi * (2637.0 if t < 0.12 else 3520.0) * t) * 0.2) * math.exp(-t * 6)
    )
    
    # 16. Checkpoint activated
    synth_sfx("checkpoint", 0.65, lambda t, dur:
        (math.sin(2 * math.pi * 440.0 * t) * 0.3 +
         math.sin(2 * math.pi * 554.37 * t) * 0.3 +
         math.sin(2 * math.pi * 659.25 * t) * 0.25 +
         math.sin(2 * math.pi * 880.0 * t) * 0.2) * env_adsr(t, dur, 0.05, 0.1, 0.7, 0.25)
    )
    
    # 17. Click
    synth_sfx("click", 0.06, lambda t, dur:
        math.sin(2 * math.pi * 1200 * t) * (1.0 - t/dur)**2 * 0.6
    )
    
    # 18. Boss roar
    synth_sfx("boss_roar", 0.9, lambda t, dur:
        ((1.0 if math.sin(2 * math.pi * (65 + 15 * math.sin(t * 30)) * t) > 0 else -1.0) * 0.5 +
         (random.random()*2-1) * 0.4) * env_adsr(t, dur, 0.15, 0.2, 0.8, 0.3)
    )
    
    # 19. Victory
    synth_sfx("victory", 1.2, lambda t, dur:
        (math.sin(2 * math.pi * (523.25 if t < 0.25 else (659.25 if t < 0.5 else (783.99 if t < 0.75 else 1046.5))) * t) * 0.5 +
         math.sin(2 * math.pi * 261.63 * t) * 0.3) * env_adsr(t, dur, 0.05, 0.1, 0.8, 0.3)
    )

def render_sequence(bpm, bars, beats_per_bar, tracks):
    beat_dur = 60.0 / bpm
    total_dur = bars * beats_per_bar * beat_dur
    n_samples = int(total_dur * SAMPLE_RATE)
    mix = [0.0] * n_samples
    
    for track in tracks:
        wave_type = track.get("wave", "sine")
        vol = track.get("vol", 0.3)
        events = track.get("events", []) # list of (beat_start, beat_len, midi_note)
        for b_start, b_len, note in events:
            t_start = b_start * beat_dur
            dur = b_len * beat_dur
            start_idx = int(t_start * SAMPLE_RATE)
            event_samples = int(dur * SAMPLE_RATE)
            freq = note_freq(note)
            
            for i in range(event_samples):
                idx = start_idx + i
                if idx >= n_samples: break
                t = i / SAMPLE_RATE
                env = env_adsr(t, dur, a=0.03, d=0.1, s=0.6, r=0.08)
                phase = 2 * math.pi * freq * t
                if wave_type == "sine":
                    w_val = math.sin(phase)
                elif wave_type == "square":
                    w_val = 0.8 if math.sin(phase) > 0 else -0.8
                elif wave_type == "triangle":
                    w_val = 2.0 * abs(2.0 * ((freq * t) % 1.0) - 1.0) - 1.0
                elif wave_type == "saw":
                    w_val = 2.0 * ((freq * t) % 1.0) - 1.0
                else:
                    w_val = math.sin(phase)
                mix[idx] += w_val * env * vol
    return mix

def gen_music():
    # 1. Menu Theme (Mystical, magical harp & flute arpeggios, 100 BPM, 8 bars)
    bpm = 100
    bars = 8
    # Melody: D minor / F major magical mode
    # Bass: D3, F3, G3, A3
    bass_notes = [50, 50, 53, 53, 55, 55, 57, 57]
    bass_events = []
    for bar in range(bars):
        note = bass_notes[bar % len(bass_notes)]
        bass_events.append((bar * 4, 3.5, note))
        bass_events.append((bar * 4 + 2, 1.5, note + 12))
    
    # Arp track
    arp_chords = [
        [62, 65, 69, 72], # Dm
        [65, 69, 72, 77], # F
        [67, 70, 74, 77], # Gm
        [69, 72, 76, 81], # Am
        [62, 65, 69, 74], # Dm
        [60, 64, 67, 72], # C
        [58, 62, 65, 70], # Bb
        [57, 61, 64, 69], # A
    ]
    arp_events = []
    for bar, chord in enumerate(arp_chords):
        for step in range(8):
            note = chord[step % 4]
            arp_events.append((bar * 4 + step * 0.5, 0.45, note))
            
    # Lead melody
    lead_events = [
        (0.0, 1.5, 74), (2.0, 1.0, 72), (3.0, 1.0, 69),
        (4.0, 2.0, 65), (6.5, 1.5, 67),
        (8.0, 1.5, 70), (10.0, 1.0, 69), (11.0, 1.0, 67),
        (12.0, 3.0, 69),
        (16.0, 1.5, 74), (18.0, 1.0, 76), (19.0, 1.0, 77),
        (20.0, 2.0, 72), (22.5, 1.5, 74),
        (24.0, 1.5, 70), (26.0, 1.0, 69), (27.0, 1.0, 67),
        (28.0, 3.5, 69)
    ]
    
    tracks_menu = [
        {"wave": "triangle", "vol": 0.28, "events": bass_events},
        {"wave": "sine", "vol": 0.25, "events": arp_events},
        {"wave": "sine", "vol": 0.35, "events": lead_events}
    ]
    menu_samples = render_sequence(bpm, bars, 4, tracks_menu)
    save_wav("assets/music/menu_theme.wav", menu_samples)

    # 2. Forest Theme (Adventure, lively 120 BPM, 8 bars)
    bpm = 120
    bars = 8
    bass_events = []
    # Groove bassline
    f_bass = [48, 51, 55, 58, 48, 51, 53, 55] # C minor / Eb vibes
    for bar in range(bars):
        root = f_bass[bar]
        bass_events.append((bar * 4 + 0.0, 0.8, root))
        bass_events.append((bar * 4 + 1.0, 0.8, root + 7))
        bass_events.append((bar * 4 + 2.0, 0.8, root))
        bass_events.append((bar * 4 + 3.0, 0.8, root + 12))
        
    pluck_events = []
    p_notes = [60, 63, 67, 70, 72, 75, 72, 67]
    for bar in range(bars):
        for beat in range(4):
            note = p_notes[(bar * 4 + beat) % len(p_notes)]
            pluck_events.append((bar * 4 + beat + 0.5, 0.4, note))
            
    lead_events = [
        (0.0, 1.0, 72), (1.0, 0.5, 75), (1.5, 0.5, 77), (2.0, 1.5, 79),
        (4.0, 1.0, 77), (5.0, 0.5, 75), (5.5, 0.5, 72), (6.0, 1.5, 70),
        (8.0, 1.0, 67), (9.0, 1.0, 70), (10.0, 1.0, 72), (11.0, 1.0, 75),
        (12.0, 3.0, 72),
        (16.0, 1.0, 79), (17.5, 0.5, 82), (18.0, 1.5, 84),
        (20.0, 1.0, 82), (21.0, 0.5, 79), (22.0, 1.5, 75),
        (24.0, 1.0, 72), (25.0, 1.0, 75), (26.0, 1.0, 77), (27.0, 1.0, 79),
        (28.0, 3.0, 72)
    ]
    tracks_forest = [
        {"wave": "triangle", "vol": 0.32, "events": bass_events},
        {"wave": "square", "vol": 0.15, "events": pluck_events},
        {"wave": "sine", "vol": 0.38, "events": lead_events}
    ]
    forest_samples = render_sequence(bpm, bars, 4, tracks_forest)
    save_wav("assets/music/forest_theme.wav", forest_samples)

    # 3. Castle Theme (Dark, gothic, tense, 110 BPM, 8 bars)
    bpm = 110
    bars = 8
    c_bass = [45, 45, 48, 48, 41, 41, 43, 44] # A minor / F / G / G#
    bass_events = []
    for bar in range(bars):
        root = c_bass[bar]
        bass_events.append((bar * 4 + 0.0, 1.8, root))
        bass_events.append((bar * 4 + 2.0, 0.8, root + 7))
        bass_events.append((bar * 4 + 3.0, 0.8, root + 12))
        
    organ_events = []
    chords = [
        [57, 60, 64], # Am
        [57, 60, 64],
        [60, 64, 67], # C
        [60, 64, 67],
        [53, 57, 60], # F
        [53, 57, 60],
        [55, 59, 62], # G
        [56, 59, 62], # G#dim
    ]
    for bar, chord in enumerate(chords):
        for note in chord:
            organ_events.append((bar * 4, 3.8, note))
            
    lead_events = [
        (0.0, 1.5, 69), (2.0, 1.0, 72), (3.0, 1.0, 71),
        (4.0, 2.5, 69), (7.0, 0.8, 67),
        (8.0, 1.5, 65), (10.0, 1.0, 64), (11.0, 1.0, 65),
        (12.0, 3.0, 64),
        (16.0, 1.5, 69), (18.0, 1.0, 72), (19.0, 1.0, 76),
        (20.0, 2.5, 77), (23.0, 0.8, 76),
        (24.0, 1.5, 74), (26.0, 1.0, 72), (27.0, 1.0, 71),
        (28.0, 3.5, 69)
    ]
    tracks_castle = [
        {"wave": "saw", "vol": 0.22, "events": bass_events},
        {"wave": "square", "vol": 0.16, "events": organ_events},
        {"wave": "sine", "vol": 0.38, "events": lead_events}
    ]
    castle_samples = render_sequence(bpm, bars, 4, tracks_castle)
    save_wav("assets/music/castle_theme.wav", castle_samples)

    # 4. Boss Theme (Fast, high stakes, 140 BPM, 8 bars)
    bpm = 140
    bars = 8
    bass_events = []
    # Driving 16th-like rhythmic bass
    for bar in range(bars):
        root = 40 if (bar < 4) else 43 # E / G
        for step in range(8):
            note = root if (step % 2 == 0) else root + 12
            bass_events.append((bar * 4 + step * 0.5, 0.4, note))
            
    stab_events = []
    for bar in range(bars):
        c = [52, 55, 59] if (bar < 4) else [55, 58, 62]
        for note in c:
            stab_events.append((bar * 4 + 0.0, 0.3, note))
            stab_events.append((bar * 4 + 1.5, 0.3, note))
            stab_events.append((bar * 4 + 2.5, 0.3, note))
            
    lead_events = [
        (0.0, 1.0, 64), (1.0, 0.5, 67), (1.5, 0.5, 71), (2.0, 1.0, 72), (3.0, 1.0, 71),
        (4.0, 1.0, 67), (5.0, 0.5, 64), (5.5, 0.5, 67), (6.0, 2.0, 69),
        (8.0, 1.0, 72), (9.0, 0.5, 74), (9.5, 0.5, 76), (10.0, 1.5, 79),
        (12.0, 0.5, 76), (12.5, 0.5, 74), (13.0, 0.5, 72), (13.5, 0.5, 71), (14.0, 2.0, 64),
        (16.0, 1.0, 76), (17.5, 0.5, 79), (18.0, 1.5, 83),
        (20.0, 1.0, 81), (21.0, 0.5, 79), (22.0, 1.5, 76),
        (24.0, 1.0, 74), (25.0, 1.0, 76), (26.0, 1.0, 79), (27.0, 1.0, 81),
        (28.0, 3.0, 83)
    ]
    tracks_boss = [
        {"wave": "saw", "vol": 0.28, "events": bass_events},
        {"wave": "square", "vol": 0.2, "events": stab_events},
        {"wave": "triangle", "vol": 0.42, "events": lead_events}
    ]
    boss_samples = render_sequence(bpm, bars, 4, tracks_boss)
    save_wav("assets/music/boss_theme.wav", boss_samples)

if __name__ == "__main__":
    print("Generating sound effects...")
    gen_sfx()
    print("Generating music tracks...")
    gen_music()
    print("Audio generation complete!")
