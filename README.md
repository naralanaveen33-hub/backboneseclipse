# 🧙‍♂️ MYSTIC REALMS: BOUNCE BACK
### The Power of Magic — 7 Levels & 7 Bosses Game Jam Edition

A complete, polished 2D fantasy action adventure platformer built in **Godot 4.x**, deeply integrating the Game Jam theme **"BOUNCE BACK"** across combat, platforming mobility, risk-reward loop, and progression. Features the epic anthem **"Lord of the Mysteries - Dark Dream" by Curley Gao**, 7 full playable levels, and 7 formidable boss encounters with active multi-phase attacks!

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
- **Supreme Final Boss:** **Abyssal Overlord Malakor - Reclaimer of the Relics** (1800 HP)
- **Attacks:** 3 Climactic Phases!
  - **Phase 1:** Chaos Orb barrages (5 orbs, deflectable!), Teleport strikes.
  - **Phase 2:** Chaos & Magma Dual Barrages (8 orbs!), Minion portals, Sky meteor strikes.
  - **Phase 3 (Apocalyptic Overdrive):** 12-orb radial bullet hell! Chain Parry Deflections and Rebound Overdrive to defeat Malakor and reclaim your stolen glory!

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
| **Q** | Rebound Overdrive | Radial shockwave + 5s Rapid Fire & 5x Ricochet |
| **R** | Restart Checkpoint | Respawn at active checkpoint |
| **Esc** or **P** | Pause Menu | Resume, Restart, Level Select, Main Menu |

---

## 🚀 How to Run and Play

### Method 1: Launch Godot 4 Directly
```bash
# Launch the full game starting at Main Menu:
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot

# Or launch directly into Level 1:
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot scenes/levels/level_1.tscn

# Or jump to any level (level_1 through level_7):
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot scenes/levels/level_7.tscn
```

### Method 2: Run Automated In-Engine Test Suite (100% Pass)
```bash
/Users/naralanaveen/Downloads/Godot.app/Contents/MacOS/Godot --headless scenes/tests/test_runner.tscn
```
