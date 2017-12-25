from core import display, player, probabilistic_ai
import time

dummy = player.Player()
ai = probabilistic_ai.Probabilistic_AI()
k = 0
while not dummy.has_lost():
    k += 1
    ai.turn(dummy)
    display.display_field(dummy.get_field())
    time.sleep(0.3)
