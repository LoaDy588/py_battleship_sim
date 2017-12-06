from core import display, player, hunt_ai, random_ai, hunt_ai
import matplotlib.pyplot as plt

samples = 5000


results_1 = [0 for x in range(101)]
for i in range(samples):
    dummy = player.Player()
    ai = hunt_ai.Hunt_AI(False)
    k = 0
    while not dummy.has_lost():
        k += 1
        ai.turn(dummy)
    if i % 500 == 0:
        print("hunt-no parity:" + str(i*100/samples) + "%")
    if k <= 100:
        results_1[k] += 1


results_2 = [0 for x in range(101)]
for i in range(samples):
    dummy = player.Player()
    ai = hunt_ai.Hunt_AI(True)
    k = 0
    while not dummy.has_lost():
        k += 1
        ai.turn(dummy)
    if i % 500 == 0:
        print("hunt-parity:" + str(i*100/samples) + "%")
    if k <= 100:
        results_2[k] += 1


results_3 = [0 for x in range(101)]
for i in range(samples):
    dummy = player.Player()
    ai = random_ai.Random_AI()
    k = 0
    while not dummy.has_lost():
        k += 1
        ai.turn(dummy)
    if i % 500 == 0:
        print("random:" + str(i*100/samples) + "%")
    if k <= 100:
        results_3[k] += 1


plt.plot(results_1)
plt.plot(results_2)
plt.plot(results_3)
plt.show()
