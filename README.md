# 🧙‍♂️ MYSTIC REALMS: BOUNCE BACK
### The Power of Magic — 8 Levels & 8 Bosses Ultimate Edition

A complete, polished 2D fantasy action adventure platformer built in **Godot 4.x**, deeply integrating the Game Jam theme **"BOUNCE BACK"** across combat, platforming mobility, risk-reward loop, and progression. Features the epic anthem **"Lord of the Mysteries - Dark Dream" by Curley Gao**, 8 full playable levels, and 8 formidable boss encounters including the 50,000 HP Primordial Void Emperor with active multi-phase attacks!

---

## 🎵 Featured Soundtrack
- **Main Anthem:** *"Curley Gao - Lord Of Mysteries - Dark Dream"* (`assets/music/dark_dream.mp3`)
  - Loops continuously and seamlessly across the Main Menu, Level Select, all 7 Levels, and all 7 Boss Battles!

---

## ⚡ 5 "BOUNCE BACK" SYSTEMS INTEGRATED ACROSS ALL 7 LEVELS

### 1. 🔄 Ricochet & Deflection Combat (Core Offense)
- **Wall & Floor Ricochet:** Player fireballs and frost blasts bounce off walls, floors, ceilings, and obstacles up to 3 times (5 times during Overdrive).
- **Multiplier Damage Scaling:** Each bounce multiplies projectile damage ($1\times \to 2\times \to 3\times$) and accelerates speed (+15% per bounce).
- **Dynamic Visuals & Audio:** Each consecutive wall bounce shifts color glow (Amber $\to$ Electric Cyan $\to$ Prismatic Magenta $\to$ Solar Gold) with pitch-escalating crystalline pings and floating combo feedback (`"2x BOUNCE!"`, `"3x BOUNCE!"`).
- **Timed Parry & Deflect:** Press **Right-Click** or **[Shift] / [I]** right before an enemy projectile strikes to parry it away! Bounces enemy shots right back at them with **$3\times$ speed**, **$3\times$ damage**, stun/freeze, screen hit-stop, and +35% Rebound energy.

### 2. 🚀 Magical Recoil Movement (Platforming Mobility)
- **Rocket-Jumping / Boost Impulse:** Aiming downward with the mouse or holding **[S]** while firing applies a vertical impulse force (`velocity.y <= -420 px/s`), allowing wizards to rocket-jump across wide bottomless chasms and leap up to high secret ledges.
- **Horizontal Recoil:** Firing horizontally pushes the player backward to evade enemy charges or quickly kite away from danger.

### 3. 💥 Damage-to-Power "Rebound" Meter (Risk-Reward Loop)
- **Rebound Fueling:** Taking damage (+25%) or surviving near-misses (+12%) fills the glowing HUD Rebound Meter.
- **Overdrive Shockwave:** When the meter reaches 100%, pressing **[Q]** triggers **Rebound Overdrive**:
  - Unleashes a radial magical shockwave dealing 60 damage and knocking back all nearby enemies (220px).
  - Enters a **5-second Overdrive state** with radiant golden aura, rapid-fire casting (0.10s cooldown), **5-bounce mega ricochets**, and free mana casting.

### 4. 🏛️ "From Ashes to Power" Progression Hook
- **Starting Banners in Every Level:** Every level opens with an atmospheric **BOUNCE BACK** intro banner with mission briefings and theme tips.
- **Ruined Shrines:** Dormant ancient stone shrines scattered throughout all 7 levels "bounce back" to life when struck by ricocheted spells, granting permanent stat buffs (+Max HP, +Movement Speed, +Rebound Rate).

### 5. ✨ Game Jam Juice & Feedback
- **Hit-Stop Freeze Frames:** Deflections, high-bounce critical hits, and Overdrive shockwaves trigger crisp micro freeze frames (0.05x time scale for 0.06s).
- **Pitch-Escalating Audio:** Wall bounces escalate in pitch dynamically with each bounce.
- **Floating Combo Text:** In-world rising combo popups (`"2x BOUNCE!"`, `"DEFLECTED 3x!"`, `"REBOUND OVERDRIVE!"`, `"BOOST!"`, `"SHRINE RESTORED!"`).

---

## 🗺️ 7 PLAYABLE REALMS & FORMISTABLE BOSSES

### 🌲 Level 1: The Enchanted Forest
- **Atmosphere:** Twilight purple skies, glowing mushrooms, floating mossy platforms.
- **Boss:** **Corrupted Shadow Behemoth** (500 HP)
- **Attacks:** Deflectable Shadow Spores (parry back for 3x damage!), Ground Slam Shockwave, Ferocious Trample Charge.

### 🏰 Level 2: The Dark Castle
- **Atmosphere:** Blood moon, gothic castle spires, deadly spike traps, and lava pits.
- **Boss:** **Dark Wizard - Lord of Shadows** (750 HP)
- **Attacks:** 3-to-5 Dark Orb barrages (deflectable!), Teleport Ambush, Shadow Bat minions.

### 🌋 Level 3: The Molten Caverns
- **Atmosphere:** Deep subterranean magma caverns, boiling lava waterfalls, volcanic rock.
- **Boss:** **Infernal Magma Titan** (900 HP)
- **Attacks:** Bouncing Magma Orb barrages (deflectable!), Magma Eruption ground slams, Lava Leaps.

### ❄️ Level 4: The Frozen Crypts
- **Atmosphere:** Glacial aurora sky, icy stalactites, frost caverns, and slippery ledges.
- **Boss:** **Frost Lich Sovereign** (1050 HP)
- **Attacks:** Glacial Frost Shards (parry back to freeze the Lich for 3s!), Blizzard Nova, Teleportation.

### ⚡ Level 5: The Tempest Spire
- **Atmosphere:** Electrified storm clouds, thunder forks, floating gothic spires.
- **Boss:** **Storm Thunder Archon** (1200 HP)
- **Attacks:** High-speed Thunder Orbs (deflectable!), Sky Lightning strikes, Storm Dashes.

### 🌌 Level 6: The Astral Void Sanctum
- **Atmosphere:** Deep cosmic nebula, shattered celestial moon, cosmic constellations.
- **Boss:** **Celestial Void Monarch - Lord of the Mysteries** (1400 HP)
- **Attacks:** 7-to-9 Astral Starbursts, Dimensional Rift Phasing, Sky Lightning, Demon summons.

### 👑 Level 7: The Abyssal Throne (The Final Showdown)
- **Atmosphere:** Crimson eclipse void, colossal black hole, throne pillars of the ancient citadel.
- **Boss:** **Abyssal Overlord Malakor - Reclaimer of the Relics** (1800 HP)
- **Attacks:** 3 Climactic Phases!
  - **Phase 1:** Chaos Orb barrages (5 orbs, deflectable!), Teleport strikes.
  - **Phase 2:** Chaos & Magma Dual Barrages (8 orbs!), Minion portals, Sky meteor strikes.
  - **Phase 3 (Apocalyptic Overdrive):** 12-orb radial bullet hell! Chain Parry Deflections and Rebound Overdrive to defeat Malakor and reclaim your stolen glory!

### 🌌👑 Level 8: The Primordial Singularity Core (THE ULTIMATE BOSS REALM)
- **Atmosphere:** Cosmic Singularity with accretion disk, shattered galaxies, colossal dark monolith spires, floating obsidian ruin pillars with glowing runes.
- **Secret Room — The Ancient Astral Sanctum:**
  - Hidden behind a breakable cracked wall at high altitude ($X=1570, Y=180$).
  - Features floating astral crystals and the legendary **God Relic Shrine**.
  - Awakening the shrine bestows **$+1,500$ Max HP**, **$+500$ Max MP**, accelerated mana regeneration, **$+35\%$ movement speed**, **$+60\%$ damage**, **$+50\%$ Rebound meter rate**, and unlocks the player's ultimate abilities!
- **The Ultimate Supreme Boss:** **PRIMORDIAL VOID EMPEROR MALAKOR** (**50,000 HP**)
- **Dedicated Systems & 8 Core Ability Trees:**
  1. **Teleportation:** Instantly phases behind player for ambush combos; teleports randomly across the arena; dark vortex rifts with audio/visual feedback; dynamic cooldowns (3.5s $\to$ 1.0s).
  2. **Super Speed:** Sprints at supersonic speeds (220 $\to$ 550 px/s) with rapid acceleration; high-speed dash attacks (850-1000 px/s); fading motion trail ghosts (`BossGhostTrail`); instant responsive turning.
  3. **Stun Attack:** Channels electric dark lightning, firing an expanding `ElectricShockwave` that deals damage and applies an active 1.8s stun lock to the player; visual orbiting stun sparks and electric flashing over player. Deflectable via Timed Parry!
  4. **Dark Energy Attack:** 
     - **Multi-Orb Barrage:** 5 to 14 dark energy balls with homing tendrils (deflectable by timed parry for $3\times$ speed & damage!).
     - **Massive Void Explosion:** Telegraph warning circle followed by colossal screen-shaking dark blast (50+ AoE dmg).
     - **Full-Screen Dark Energy Beam:** Red laser aim guide telegraph charging into a devastating full-screen destructive beam.
  5. **Special Abilities:**
     - **Minion Summoning:** Spawns flying bats, shadow monsters, and fire demons from void portals.
     - **Protective Shield:** Spawns a 2,500 HP glowing hexagonal void barrier absorbing all damage until shattered.
     - **Health Regeneration:** Channels dark siphon runes recovering 1,200 HP/tick (+3,600 HP total).
     - **Ground Slam & Energy Waves:** Leaps high, plunges violently at 1250 px/s, releasing twin high-speed ground-slicing energy waves left and right.
  6. **4-Phase System & Appearance Transformations:**
     - **Phase 1 (50,000 - 37,500 HP):** Obsidian Void Armor with Deep Violet Aura (Scale $1.1\times$, Speed 220 px/s).
     - **Phase 2 (37,500 - 25,000 HP):** Crimson Void Surge with glowing red eye flares & fire trail (Speed 320 px/s, contact damage +30%, dash attacks, stun shockwave, minion summons).
     - **Phase 3 (25,000 - 10,000 HP):** Astral Cosmic Electric Cyan with celestial wings (Speed 420 px/s, instant teleport behind player combos, protective shield, dark energy beam, health regen).
     - **Phase 4 (10,000 - 0 HP):** Supreme Apocalyptic Rage Mode (Solar Gold Overdrive glow, Speed 550 px/s, massive triple explosions, full-screen beams, 14-orb spiral bullet hell, relentless rage roaring!).
  7. **Dedicated Large Boss Health Bar UI:**
     - Displays title, active phase badges (`[PHASE 1]` to `[PHASE 4: ULTIMATE RAGE]`), numerical HP (`50,000 / 50,000 HP (100%)`), and smooth animated bar with phase-shifting glow colors.
  8. **All 9 Dedicated Animations:** `idle`, `running`, `teleporting`, `attacking`, `dashing`, `taking_damage`, `stunned`, `ultimate_attack`, `death`.

---

## 🧙‍♂️ Enhanced Player Archmage & Ultimate Powers

- **Custom Enhanced Sprite**: High-contrast, handcrafted dark hooded archmage character with ceremonial gold-trimmed robes and a wizard staff crowned by a glowing cosmic purple orb.
- **Complete 32 Animation Frames Across 8 Sets**: `idle` (4f), `run` (6f), `jump` (2f), `fall` (2f), `attack` (4f), `hurt` (2f), `death` (6f), and `respawn` (6f).
- **Astral Void Cannon `[E]`**: Fires a high-velocity celestial projectile dealing 650 base damage that pierces boss shields directly and ricochets up to 4 times ($+50\%$ damage per bounce). Features heavy rocket-jumping recoil.
- **Chronos Shadow Step `[F]`**: 220 px spatial dash with directional aiming. Leaves motion-trail ghost duplicates (`BossGhostTrail`), erupts with teleport vortex bursts, grants invulnerability frames, and breaks active stuns instantly.

---

## 🕹️ Controls

| Control | Action | Effect |
|---|---|---|
| **A / D** or **← / →** | Move Left / Right | Smooth physics movement |
| **Space** or **W** | Jump | Platformer jump with variable cut & coyote time |
| **Left-Click** or **J** | Fireball (Ricochet) | Bounces off walls ($1\times \to 2\times \to 3\times$ dmg). Rocket-jumps when aimed down |
| **Right-Click** or **Shift / I** | Parry / Deflect | Reflects enemy projectiles at $3\times$ speed & stun |
| **K** | Ice Blast | Bouncing frost bolt that freezes enemies solid |
| **L** | Lightning Strike | Thunder strike on forward enemies (95 dmg) |
| **I** | Magic Shield | Protective rune dome negating all damage |
| **E** | Astral Void Cannon | Celestial beam piercing shields with 4-wall ricochet ($+50\%$/bounce) |
| **F** | Chronos Shadow Step | 220px spatial dash with invulnerability, ghost trail, and stun cleanse |
| **Q** | Rebound Overdrive | Radial shockwave + 5s Rapid Fire & 5x Ricochet |
| **R** | Restart Checkpoint | Respawn at active checkpoint |
| **Esc** or **P** | Pause Menu | Resume, Restart, Level Select, Main Menu |

---

## 🚀 How to Run and Play

### Method 1: Launch Godot 4 Directly
```bash
# Launch the full game starting at Main Menu:
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot

# Or launch directly into Level 8 (Ultimate Boss):
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot scenes/levels/level_8.tscn

# Or jump to any level (level_1 through level_8):
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot scenes/levels/level_1.tscn
```

### Method 2: Run Automated In-Engine Test Suite (11/11 Suites 100% Pass)
```bash
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot --headless scenes/tests/test_runner.tscn
```
