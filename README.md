<!-- Top-level README moved from project/README.md -->
# Dice Game — Web (Flask)

A minimal Flask web UI for the Dice Game.

What the project is
- A small browser game that accepts a die total (2–12) or uses a server-generated random roll. State is stored in the session so you can play a short round.

How it works (brief)
- Turn 1: roll 2,3,12 → lose; 7,11 → win; otherwise that roll becomes your point and the game continues.
- Turns 2+: roll 7 → lose; roll equal to your point → win; otherwise continue (turn increments).

How to run
1. Install dependencies:
```bash
python3 -m pip install -r project/requirements.txt
```
2. Start the app:
```bash
python3 project/app.py
```
3. Open `http://127.0.0.1:5000` in your browser.

Files
- `project/app.py` — Flask app
- `project/games/dice_game.py` — game logic
- `project/templates/dice.html` — UI template

That's all — use "Start New Game" in the UI to reset and play again.

File structure
------------
The main files for this Flask app are:

- `project/app.py` — Flask application and route handlers.
- `project/games/dice_game.py` — game logic, validation, and state helpers.
- `project/templates/dice.html` — Jinja2 template for the web UI.
- `project/requirements.txt` — Python dependencies (Flask).

Use this as a quick reference when exploring the code.

Flask file structure
--------------------
project/
├── app.py                 # Flask application and route handlers
├── games/
│   ├── __init__.py        # package exports for the games module
│   └── dice_game.py       # game logic, validation, and state helpers
├── templates/
│   └── dice.html          # Jinja2 template for the web UI
└── requirements.txt       # Python dependencies (Flask)
