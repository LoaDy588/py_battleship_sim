from core import player, hunt_ai, random_ai, field_utils
from multiprocessing import Queue, Process
import sys


def hunt_child(name, q, samples, parameters):
    print("starting:", name)
    for i in range(samples):
        dummy = player.Player()
        cheat_list = []
        if parameters[1]:
            cheat_list = field_utils.generate_cheat_list(dummy.get_field(),
                                                         parameters[2])

        ai = hunt_ai.Hunt_AI(parity=parameters[0], cheat=parameters[1],
                             cheat_input=cheat_list)
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)

        if i % 1000 == 0:
            print(name + ": " + str(i*100/samples) + "%")
        if k <= 100:
            q.put([name, k, i])
    print(name, " exiting")
    sys.exit()


def random_child(name, q, samples):
    ("starting:", name)
    for i in range(samples):
        dummy = player.Player()
        ai = random_ai.Random_AI()
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)
        if i % 1000 == 0:
            print(name + ": " + str(i*100/samples) + "%")
        if k <= 100:
            q.put([name, k, i])
    print(name, " exiting")
    sys.exit()


def supervisor(name, q, samples, threads):
    print("Starting:", name)
    results_dict = {}
    current = []
    while not sum(current) == threads:
        while not q.empty():
            data = q.get()
            if data[2] == samples-1:
                current.append(True)

            if data[0] in list(results_dict.keys()):
                results_dict[data[0]][data[1]] += 1
            else:
                results_dict[data[0]] = [0 for x in range(101)]
                results_dict[data[0]][data[1]] += 1

    print(name, " saving to files")
    for key in list(results_dict.keys()):
        f = open("results/"+str(key)+".txt", "w")
        for number in results_dict[key]:
            f.write(str(number)+"\n")
        f.close()
    print(name, " exiting")
    sys.exit()


def main():
    samples = 100000
    q = Queue(maxsize=0)
    threads_each = 1
    parameters = ((False, False, 0), (False, True, 1), (False, True, 2),
                  (False, True, 3), (False, True, 4), (False, True, 5),
                  (True, False, 0), (True, True, 1), (True, True, 2),
                  (True, True, 3), (True, True, 4), (True, True, 5))
    for parameter in parameters:
        for x in range(threads_each):
            name = "h-"+str(parameter[0])+"-"+str(parameter[1])+"-"+str(parameter[2])
            thread = Process(target=hunt_child, args=(name, q, samples, parameter))
            thread.start()
    for y in range(threads_each):
        thread = Process(target=random_child, args=("r", q, samples))
        thread.start()
    thread = Process(target=supervisor, args=("Supervisor", q, samples,
                                              len(parameters)*threads_each))
    thread.start()


if __name__ == "__main__":
    main()
