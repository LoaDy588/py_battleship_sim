"""
Simulate large amount of games with probabilistic ai, multithreaded.
"""
from core import player, probabilistic_ai, field_utils
from multiprocessing import Queue, Process
import sys


def child(name, q, samples, parameters):
    """
    thread for running  probabilistic AI simulations
    """
    print("starting:", name)

    for i in range(samples):
        # setup dummy player and dummy cheat_list
        dummy = player.Player()
        cheat_list = []

        # if cheating simulation, create proper cheat_list
        if parameters[0]:
            cheat_list = field_utils.generate_cheat_list(dummy.get_field(),
                                                         parameters[1])

        ai = probabilistic_ai.Probabilistic_AI(cheat=parameters[1],
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
    samples = 30000  # number of games simulated per thread
    q = Queue(maxsize=0)
    threads_each = 6  # number of threads for each parameter variant

    # parameter variants to run
    parameters = ((False, 0), (True, 2), (True, 5))

    # run every parameter variant on defined amount of threads
    for parameter in parameters:
        for x in range(threads_each):
            # name the thread by parameters, for easy sorting in supervisor thread
            name = "p-"+str(parameter[0])+"-"+str(parameter[1])
            thread = Process(target=child, args=(name, q, samples, parameter))
            thread.start()

    # start supervisor thread
    thread = Process(target=supervisor, args=("Supervisor", q, samples,
                                              len(parameters)*threads_each))
    thread.start()


if __name__ == "__main__":
    main()
