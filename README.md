# Sudoku Game

An interactive Sudoku game built with Python and Flask. The application
generates solvable puzzles, provides helpful gameplay feedback, and stores
personal preferences and scores locally in the browser.

## Features

- **Three difficulty levels:** Easy (45 clues), Medium (35 clues), and Hard
  (25 clues).
- **Guaranteed unique solutions:** Every generated puzzle is checked to ensure
  it has exactly one solution.
- **Immediate validation:** Invalid moves are highlighted as soon as they are
  entered.
- **Hints:** Reveal a correct value and track the number of hints used.
- **Completion detection:** Correctly completed boards are detected
  automatically, with a completion message and score prompt.
- **Timer:** Track the elapsed solving time for each puzzle.
- **Top 10 leaderboard:** Completed scores include the player name, time,
  difficulty, and hints used. Scores are saved in browser `localStorage`.
- **Persistent dark mode:** The selected color theme is saved in browser
  `localStorage` and restored on the next visit.
- **Board styling:** Alternating 3x3 box backgrounds and stronger box borders
  make Sudoku regions easy to distinguish.
- **Responsive and accessible UI:** The layout works on desktop and mobile
  screens and includes keyboard focus styles, ARIA labels, and live status
  announcements.

## Installation and Setup

### Prerequisites

- Python 3
- A modern web browser

### Windows

Open PowerShell in the repository directory and run:

```powershell
cd starter
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents script activation, use the virtual environment's
interpreter directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Flask App

From the `starter` directory:

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

## Run Tests

From the `starter` directory, run the exact test command:

```powershell
python -m pytest
```

The current test suite contains **24 passing tests** covering Sudoku
generation, unique-solution behavior, difficulty handling, Flask routes, and
solution checking.

## How to Play

1. Select Easy, Medium, or Hard.
2. Enter numbers in the empty cells.
3. Watch for immediate feedback on invalid moves.
4. Use **Hint** to reveal a correct value when needed.
5. Use **Check Solution** to check the current board.
6. Complete the puzzle before the timer stops.
7. Enter your name when prompted to save a qualifying result to the local
   Top 10 leaderboard.
8. Use **Dark mode** to switch themes; the preference persists between visits.

## Technical Notes

- Flask serves the game page and provides endpoints for generating puzzles and
  checking submitted boards.
- `sudoku_logic.py` creates a complete valid board, removes values, and uses
  solution counting to guarantee uniqueness.
- The frontend uses JavaScript for board interaction, validation, hints,
  completion detection, timing, theme switching, and leaderboard rendering.
- Leaderboard entries and dark-mode preferences are stored only in the
  browser's `localStorage`; they are not shared between browsers or devices.

## Project Structure

```text
starter/
├── app.py
├── sudoku_logic.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── main.js
│   └── styles.css
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   └── test_sudoku_logic.py
└── Screenshots/
    └── Feature and milestone evidence images
```
