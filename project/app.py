from flask import Flask, render_template, redirect, url_for, request, session
from games.dice_game import (
    new_game,
    play_turn,
    random_roll,
    state_to_dict,
    dict_to_state,
)

app = Flask(__name__, template_folder="templates")
app.secret_key = "dev-secret-key"


def _get_state():
    data = session.get("dice_state")
    if not data:
        state = new_game()
        session["dice_state"] = state_to_dict(state)
        return state
    return dict_to_state(data)


def _save_state(state):
    session["dice_state"] = state_to_dict(state)


@app.route("/")
def index():
    state = _get_state()
    return render_template(
        "dice.html",
        turn=state.turn,
        point=state.point,
        finished=state.finished,
        result=state.result,
        last_roll=session.get("last_roll"),
    )


@app.route("/roll", methods=["POST"])
def roll():
    state = _get_state()
    if state.finished:
        return redirect(url_for("index"))

    value = request.form.get("roll", "").strip()
    try:
        # play_turn() will validate (2–12) and raise ValueError if invalid
        state = play_turn(state, value)
        _save_state(state)

        # If it was valid, store last_roll as an int for display
        session["last_roll"] = int(value)
    except ValueError as e:
        # Keep state, just show error message
        state.result = f"Error: {e}"
        _save_state(state)

    return redirect(url_for("index"))


@app.route("/roll_random")
def roll_random():
    state = _get_state()
    if state.finished:
        return redirect(url_for("index"))

    roll_val = random_roll()  # 2..12
    session["last_roll"] = roll_val

    state = play_turn(state, roll_val)
    _save_state(state)

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
