
# games/dice_game.py
import random
from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class DiceGameState:
    turn: int = 1
    point: Optional[int] = None
    finished: bool = False
    result: str = ""


def new_game() -> DiceGameState:
    """
    Start a new game:
    - turn = 1
    - no point
    - not finished
    - empty result
    """
    return DiceGameState(turn=1, point=None, finished=False, result="")


def validate_roll(value: Any) -> int:
    """
    Validate dice roll is an integer between 2 and 12.
    Raises ValueError with a user-friendly message if invalid.
    """
    if value is None or value == "":
        raise ValueError("Please enter a dice roll (2–12) or use Random Roll.")

    try:
        roll = int(value)
    except (TypeError, ValueError):
        raise ValueError("Invalid input: roll must be a whole number.")

    if roll < 2 or roll > 12:
        raise ValueError("Die roll must be between 2 and 12.")

    return roll


def random_roll() -> int:
    """
    Simulate a roll between 2 and 12 (matches assignment requirement).
    """
    return random.randint(2, 12)


def play_turn(state: DiceGameState, roll_value: Any) -> DiceGameState:
    """
    Play one turn:
    - If game finished, do nothing.
    - Validate roll in range 2..12.
    - Apply rules for turn 1 or later turns.
    - Update result and increment turn when appropriate.
    """
    if state.finished:
        return state

    roll = validate_roll(roll_value)

    # Turn 1 rules
    if state.turn == 1:
        if roll in (2, 3, 12):
            state.finished = True
            state.result = f"Turn {state.turn}: You rolled {roll}. You LOSE."
            return state

        if roll in (7, 11):
            state.finished = True
            state.result = f"Turn {state.turn}: You rolled {roll}. You WIN!"
            return state

        # Set point and continue
        state.point = roll
        state.result = f"Turn {state.turn}: You rolled {roll}. Point is set to {state.point}."
        state.turn += 1
        return state

    # Turn 2+ rules
    if roll == 7:
        state.finished = True
        state.result = f"Turn {state.turn}: You rolled {roll}. You LOSE."
        return state

    if state.point is not None and roll == state.point:
        state.finished = True
        state.result = f"Turn {state.turn}: You rolled {roll}. You WIN (hit the point)!"
        return state

    # No result, go next turn
    state.result = f"Turn {state.turn}: You rolled {roll}. No result—roll again."
    state.turn += 1
    return state


# Helpers for storing in Flask session (dict-only)
def state_to_dict(state: DiceGameState) -> Dict[str, Any]:
    return {
        "turn": state.turn,
        "point": state.point,
        "finished": state.finished,
        "result": state.result,
    }


def dict_to_state(data: Dict[str, Any]) -> DiceGameState:
    return DiceGameState(
        turn=int(data.get("turn", 1)),
        point=data.get("point", None),
        finished=bool(data.get("finished", False)),
        result=str(data.get("result", "")),
    )
