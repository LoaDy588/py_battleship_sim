from core import display, field_utils, player
from core import hunt_ai, probabilistic_ai
import time


def game_example():
    """
    Simple simulation of Probabilistic AI playing against a dummy.

    Displays the game field of dummy.
    """
    # create players
    dummy = player.Player()
    ai = probabilistic_ai.Probabilistic_AI()

    # game loop
    while not dummy.has_lost():
        ai.turn(dummy)
        display.display_field(dummy.get_field())  # display game field
        time.sleep(0.3)


def cheat_example():
    """
    Simple simulation of Target/Hunt AI cheating against a dummy.

    Displays the game field of dummy.
    """
    # create dummy
    dummy = player.Player()

    # create cheat_list for Hunt AI, create AI
    cheat_list = field_utils.generate_cheat_list(dummy.get_field(), 3)
    ai = hunt_ai.Hunt_AI(cheat=True, cheat_input=cheat_list)

    # game loop
    while not dummy.has_lost():
        ai.turn(dummy)
        display.display_field(dummy.get_field())  # display game field
        time.sleep(0.3)
