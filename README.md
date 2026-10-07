# Real-Time Reaction Time Tester

A Pygame-based reaction time testing game developed as part of the lab assignment. The project was enhanced using an iterative AI-assisted debugging and development process.

---

## Project Overview

The Reaction Time Tester challenges the player to react as quickly as possible when the screen changes from a waiting state to a green **GO** state.

The original project had issues with reaction-time measurement and early input handling. The game was enhanced to provide accurate timing, false-start detection, a results screen, difficulty selection, replay functionality, and sound feedback.

---

## Features Implemented

### Task 1: Refine Input Timing Detection

- Reaction time is measured from the exact moment the screen turns green.
- Clicking or pressing `Space` before the green signal is detected as a **False Start**.
- False starts are not recorded as valid reaction times.
- Valid reactions are displayed in milliseconds.

### Task 2: Game Over and Results Screen

After completing all rounds, the game displays a dedicated **Game Over** screen containing:

- Individual reaction time for every round
- Average reaction time
- Selected difficulty
- Replay option
- Difficulty-change option

The game no longer depends only on terminal output for final results.

### Task 3: Difficulty Selection and Replay

The player can select:

- **Easy** — 1500–3500 ms wait time
- **Medium** — 1000–3000 ms wait time
- **Hard** — 500–2000 ms wait time

Controls:

- `1` → Easy
- `2` → Medium
- `3` → Hard
- `R` → Replay using the same difficulty
- `D` → Return to difficulty selection
- Mouse click or `Space` → React during a round

### Task 4: Sound Feedback

Sound effects were added for important game events:

- **GO cue** when the screen turns green
- **Success sound** after a valid reaction
- **False-start warning**
- **Game-over sound** when the session ends

The sounds are generated programmatically using Pygame's mixer, so separate audio files are not required.

---

## Expected Game Flow

```text
Difficulty Selection
        ↓
Choose Easy / Medium / Hard
        ↓
Waiting Screen
        ↓
Screen turns Green + GO Sound
        ↓
Player Clicks / Presses Space
        ↓
 ┌───────────────────────┐
 │                       │
Valid Reaction       Early Input
 │                       │
 ↓                       ↓
Reaction Time        False Start
Recorded             Detected
 │                       │
 └───────────┬───────────┘
             ↓
        Next Round
             ↓
       All Rounds Done
             ↓
        Game Over
             ↓
    Replay / Change Difficulty