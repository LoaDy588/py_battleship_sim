"""
Simulate large amount of games with hunt/target and random AI, multithreaded.
"""
from core import player, hunt_ai, random_ai, field_utils
from multiprocessing import Queue, Process
import sys


def hunt_child(name, q, samples, parameters):
    """
    thread for running  target/hunt AI simulations
    """
    print("starting:", name)

    for i in range(samples):
        # create dummy player and dummy cheat_list
        dummy = player.Player()
        cheat_list = []

        # if cheating simulation, create proper cheat_list
        if parameters[1]:
            cheat_list = field_utils.generate_cheat_list(dummy.get_field(),
                                                         parameters[2])

        # setup AI
        ai = hunt_ai.Hunt_AI(parity=parameters[0], cheat=parameters[1],
                             cheat_input=cheat_list)

        # simulate game and send results to supervisor thread
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)

        if i % 1000 == 0:
            print(name + ": " + str(i*100/samples) + "%")  # progress display
        if k <= 100:
            q.put([name, k, i])
    print(name, " exiting")
    sys.exit()


def random_child(name, q, samples):
    """
    thread for running random AI simulations
    """
    ("starting:", name)

    for i in range(samples):
        # setup game
        dummy = player.Player()
        ai = random_ai.Random_AI()

        # play game and send results to supervisor thread
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)
        if i % 1000 == 0:
            print(name + ": " + str(i*100/samples) + "%")  # progress display
        if k <= 100:
            q.put([name, k, i])
    print(name, " exiting")
    sys.exit()


def supervisor(name, q, samples, threads):
    """
    Supervisor thread.

    Stores results, after simulations are done, saves them to .txt files.
    """
    print("Starting:", name)

    # prepare dict for storing results and status watching list
    results_dict = {}
    current = []

    # while any simulation still running, check queue for results
    while not sum(current) == threads:
        while not q.empty():
            data = q.get()

            # if simulation finished, add that information to "current" list
            if data[2] == samples-1:
                current.append(True)

            # sort results by parameters of the simulation
            if data[0] in list(results_dict.keys()):
                results_dict[data[0]][data[1]] += 1
            else:
                results_dict[data[0]] = [0 for x in range(101)]
                results_dict[data[0]][data[1]] += 1

    # save results to individual files, named by parameters of simulation
    print(name, " saving to files")
    for key in list(results_dict.keys()):
        f = open("results/"+str(key)+".txt", "w")
        for number in results_dict[key]:
            f.write(str(number)+"\n")
        f.close()
    print(name, " exiting")
    sys.exit()


def main():
    samples = 1000000  # number of games simulated per thread
    q = Queue(maxsize=0)
    threads_each = 1  # number of threads for every parameter variant

    # parameter variants of target/hunt AI to run
    parameters = ((False, False, 0), (False, True, 1), (False, True, 2),
                  (False, True, 3), (False, True, 4), (False, True, 5),
                  (True, False, 0), (True, True, 1), (True, True, 2),
                  (True, True, 3), (True, True, 4), (True, True, 5))

    # run every parameter variant on defined amount of threads
    for parameter in parameters:
        for x in range(threads_each):
            # name the thread by parameters, for easy sorting in supervisor thread
            name = "h-"+str(parameter[0])+"-"+str(parameter[1])+"-"+str(parameter[2])
            thread = Process(target=hunt_child, args=(name, q, samples, parameter))
            thread.start()

    # also start the random AI threads
    for y in range(threads_each):
        thread = Process(target=random_child, args=("r", q, samples))
        thread.start()

    # start the supervisor thread, only need one
    thread = Process(target=supervisor, args=("Supervisor", q, samples,
                                              len(parameters)+1*threads_each))
    thread.start()


if __name__ == "__main__":
    main()
