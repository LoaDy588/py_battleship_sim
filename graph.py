from core import display, player, hunt_ai, random_ai, hunt_ai
import matplotlib.pyplot as plt
from multiprocessing import Queue, Process
import sys
import signal


def Hunt_no_parity(name, q, samples):
    print("hello:", name)
    for i in range(samples):
        dummy = player.Player()
        ai = hunt_ai.Hunt_AI(False)
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)
        if i % 500 == 0:
            print(name + ": " + str(i*100/samples) + "%")
        if k <= 100:
            q.put(["hnp", k, i])
    print(name, " exiting")
    sys.exit()


def Hunt_parity(name, q, samples):
    print("hello:", name)
    for i in range(samples):
        dummy = player.Player()
        ai = hunt_ai.Hunt_AI(True)
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)
        if i % 500 == 0:
            print(name + ": " + str(i*100/samples) + "%")
        if k <= 100:
            q.put(["h_p", k, i])
    print(name, " exiting")
    sys.exit()

def Random_play(name, q, samples):
    ("hello:", name)
    for i in range(samples):
        dummy = player.Player()
        ai = random_ai.Random_AI()
        k = 0
        while not dummy.has_lost():
            k += 1
            ai.turn(dummy)
        if i % 500 == 0:
            print(name + ": " + str(i*100/samples) + "%")
        if k <= 100:
            q.put(["rnd", k, i])
    print(name, " exiting")
    sys.exit()

def Supervisor(name, q, samples, threads):
    print("hello:", name)
    results_1 = [0 for x in range(101)]
    results_2 = [0 for x in range(101)]
    results_3 = [0 for x in range(101)]
    current = []
    while not sum(current) == threads:
        while not q.empty():
            data = q.get()
            if data[2] == samples-1:
                current.append(True)
            if data[0] == "hnp":
                results_1[data[1]] += 1
            elif data[0] == "h_p":
                results_2[data[1]] += 1
            elif data[0] == "rnd":
                results_3[data[1]] += 1
    plt.plot(results_1)
    plt.plot(results_2)
    plt.plot(results_3)
    plt.show()
    sys.exit()

def main():
    samples = 2000000
    q = Queue(maxsize=0)
    thread1 = Process( target=Supervisor, args=("supervisor", q, samples, 15) )
    thread1.start()
    thread2 = Process( target=Random_play, args=("rnd1", q, samples) )
    thread2.start()
    thread3 = Process( target=Random_play, args=("rnd2", q, samples) )
    thread3.start()
    thread4 = Process( target=Random_play, args=("rnd3", q, samples) )
    thread4.start()
    thread5 = Process( target=Random_play, args=("rnd4", q, samples) )
    thread5.start()
    thread6 = Process( target=Hunt_parity, args=("h_p1", q, samples) )
    thread6.start()
    thread7 = Process( target=Hunt_parity, args=("h_p2", q, samples) )
    thread7.start()
    thread8 = Process( target=Hunt_parity, args=("h_p3", q, samples) )
    thread8.start()
    thread9 = Process( target=Hunt_parity, args=("h_p4", q, samples) )
    thread9.start()
    thread10 = Process( target=Hunt_no_parity, args=("hnp1", q, samples) )
    thread10.start()
    thread11 = Process( target=Hunt_no_parity, args=("hnp2", q, samples) )
    thread11.start()
    thread12 = Process( target=Hunt_no_parity, args=("hnp3", q, samples) )
    thread12.start()
    thread13 = Process( target=Hunt_no_parity, args=("hnp4", q, samples) )
    thread13.start()
    thread14 = Process( target=Random_play, args=("rnd5", q, samples) )
    thread14.start()
    thread15 = Process( target=Hunt_parity, args=("h_p5", q, samples) )
    thread15.start()
    thread16 = Process( target=Hunt_no_parity, args=("hnp5", q, samples) )
    thread16.start()

if __name__ == "__main__":
    main()
